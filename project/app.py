import os
import uuid
from flask import Flask, flash, request, render_template, redirect, session, send_from_directory
from werkzeug.utils import secure_filename
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL

from helpers import apology, login_required, usd, seller_apology

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///ecommerce.db")

    
# registeration
@app.route("/register",methods=["GET","POST"])
def register():
    session.clear()
    if request.method == "POST":
        type =request.form.get("type")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirm")

        if not username:
            return apology("missing username",400)
        if not password:
            return apology("missing password",400)
        if not confirmation:
            return apology("missing password confirmation",400)
        if password != confirmation:
            return apology("passwords not matched",400)
        hash = generate_password_hash(password)

        if type == "customer":
            session.clear()
            customers = db.execute("select username from customers")
            if {"username":username} in customers:
                return apology("username exsists",400)

            db.execute("insert into customers(username,hash) values(?,?)",username,hash)

            rows = db.execute("SELECT * FROM customers WHERE username = ?", username)
            session["user_id"] = rows[0]["id"]
            return redirect("/")

        elif type == "seller":
            session.clear()
            sellers = db.execute("select username from sellers")
            if {"username":username} in sellers:
                return apology("username exsists",400)

            db.execute("insert into sellers(username,hash) values(?,?)",username,hash)

            rows = db.execute("SELECT * FROM sellers WHERE username = ?", username)
            session["user_id"] = rows[0]["id"]
            return redirect("seller_home")

        else:
            return apology("Invalid",404)
    else:
        return render_template("register.html")


# login
@app.route("/login",methods=["GET","POST"])
def login():
    session.clear()
    if request.method=="POST":
        type =request.form.get("type")
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return apology("missing username",400)
        if not password:
            return apology("missing password",400)

        if type == "customer":
            session.clear()
            rows = db.execute("select * from customers where username = ?",username)
            if len(rows) != 1 or not check_password_hash(rows[0]["hash"],password):
                return apology("invalid username and/or password", 403)

            session["user_id"] = rows[0]["id"]
            return redirect("/")

        elif type == "seller":
            session.clear()
            rows = db.execute("select * from sellers where username = ?",username)
            if len(rows) != 1 or not check_password_hash(rows[0]["hash"],password):
                return apology("invalid username and/or password", 403)

            session["user_id"] = rows[0]["id"]
            return redirect("seller_home")
        else:
            return apology("Invalid",404)
    else:
        return render_template("login.html")


# logout
@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("login")


# home
@app.route("/")
@login_required
def home():
    products = db.execute("select * from products")
    return render_template("home.html", products=products)


# cart
@app.route("/cart",  methods=["GET","POST"])
@login_required
def cart():
    if request.method == "POST":
        prod_id = int(request.form.get("id"))
        type= request.form.get("type")
        if type == "customer":
            total = float(request.form.get("total"))
            db.execute("delete from orders where prod_id = ? and user_id = ?", prod_id, session["user_id"])
            db.execute("update customers set cash = cash + ? where id = ?",total,session["user_id"])
            return redirect("cart")
        elif type == "seller":
            orders = db.execute("select prod_id from orders")
            if {"prod_id":prod_id} in orders:
                db.execute("update customers set cash = cash + ((select price from products where id = ?)*(select count from orders where user_id = customers.id and prod_id=?)) where id in (select user_id from orders where prod_id = ?) ", prod_id,prod_id,prod_id)
                db.execute("delete from orders where prod_id = ?", prod_id)

            db.execute("delete from sellers_products where prod_id = ? and seller_id = ?",prod_id,session["user_id"])
            db.execute("delete from products where id = ?",prod_id)
            return redirect("seller_home")

    else:
        orders = db.execute("select * from orders join products on prod_id = products.id and user_id = ?",session["user_id"])
        cash = db.execute("select cash from customers where id = ? ", session["user_id"])
        return render_template("cart.html",orders = orders, cash = cash)


# product detials
@app.route("/details",methods=["GET","POST"])
@login_required
def details():
    if request.method == "POST":
        prod_id = int(request.form.get("id"))
        count = request.form.get("count")
        cash = db.execute("select cash from customers where id = ?",session["user_id"])
        price = db.execute("select price from products where id = ?",prod_id)
        total = int(count)*price[0]["price"]

        if not count:
            return apology("enter the count",400)
        if not count.isdigit() or int(count) < 1:
            return apology("invalid count",400)

        if cash[0]['cash']-total <  0:
            return apology("you have no cash",400)

        count = int(request.form.get("count"))
        orders = db.execute("select prod_id from orders where user_id = ?",session["user_id"])

        if {'prod_id': prod_id} in orders:
            db.execute("update orders set count = count + ?, total = total + ? where prod_id = ? and user_id = ?",count,total,prod_id,session["user_id"])
        else:
            db.execute("insert into orders(user_id,prod_id,count,total) values(?,?,?,?)",session["user_id"],prod_id,count,total)

        db.execute("update customers set cash = cash - ? where id = ? ",total,session["user_id"])
        product = db.execute("select * from products where id = ? ",prod_id)
        flash('successfuly item added to cart')
        return redirect("cart")
    else:
        product = db.execute("select * from products where id = ?",int(request.args.get("id")))
        return render_template("details.html",product=product)


# search page
@app.route("/search")
@login_required
def search():
    item = request.args.get("item")
    if not item:
        return apology("no item inserted",400)
    sql = "select * from products where prod_name LIKE ?"
    args=['%'+item+'%']
    results = db.execute(sql,args)
    if results:
        return render_template("search.html",results=results)
    return apology("no items",400)


# seller home page
@app.route("/seller_home", methods=["GET","POST"])
@login_required
def seller_home():
    if request.method == "POST":
        title = request.form.get("title")
        price = request.form.get("price")
        description = request.form.get("description")
        image = request.files['image']
        if not title or not price or not image:
            return seller_apology("missing input",400)

        price = float(request.form.get("price"))
        filename = str(uuid.uuid1())+os.path.splitext(image.filename)[1]
        image.save(os.path.join("static/images", filename))
        image_path = "/static/images/"+filename

        db.execute("insert into products(prod_name,price,description,image) values(?,?,?,?)",title,price,description,image_path)
        id = db.execute("select id from products order by id desc limit 1")
        db.execute("insert into sellers_products(seller_id,prod_id) values(?,?)",session["user_id"],id[0]["id"])
        return redirect("seller_home")
    else:
        products = db.execute("select * from sellers_products join products on prod_id = products.id and seller_id = ?", session["user_id"])
        return render_template("seller_home.html", products=products)