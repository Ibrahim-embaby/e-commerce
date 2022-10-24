# E-commerce Web Application

## Table of Contents

* [Description](#description)
* [Screenshots](#screenshots)

## Description
This is an e-commerce web application that connects sellers and customers.

- the seller can add a product to sell by providing the product title, price, image, and optionally description.
and once the product is added he can remove it.
if the product that the seller removed is ordered by one or more customers, the total price of the order is returned to them.

- the customer can see the products added by the sellers and can search for a specific product.
also, the customer can buy a product at the number he wants but not exceeds the total cash he owns.
once the customer buys the product, the cart page is shown and he can see the list of the products he bought
- **Used Tools**:
    - <b><em>python, flask, html, css, bootstrap, jinja, sqlite3</em></b>
- **the project consists of:**
    - **app.py:**
        - contains the all backend functions that the system needs such as:
            - **register function:** stores the user in the database if it has not registered before
            - **login function:** let the user log in to the system if it has an account
            - **logout function:** let the user log out from the system
            - **home function:** shows the customer home page
            - **cart function:** shows the customer orders
            - **details function:** shows the details of a specific product to the customer
            - **search function:** let the customer search for a specific product
            - **seller_home function:** shows the home page of the seller

        - it also includes the database operations to handle the user's actions

    - **ecommerce.db:**
        - the database that contains all the data about the system users like accounts, products, and orders

    - **templates folder:**
        - **layout.html:** This is a layout used by other customer HTML pages to provide them with static elements such as the navbar, the search field, and the cart icon
        - **apology.html:** the HTML page that shows when the customer makes an error like entering an invalid username or password, etc...
        - **register.html:** contains the UI of the registration page that the user can register as a seller or as a customer
        - **login.html:** contains the UI of the login page that the user can log in as a seller or as a customer
        - **home.html:** contains the UI of the customer home page including the product cards.
        - **details.html:** contains the product details(title, price, image, and description) and a form (product count field, and Add to cart button) to buy this product
        - **cart.html:** contains the UI of the orders table(order number, order name, count, price, total) that the user bought, a remove button beside each product, and the cash he owns
        - **search.html:** contains the UI of the results of the user search input
        - **seller_layout.html:** This is a layout used by other seller HTML pages to provide them with static elements
        - **seller_apology.html:** the HTML page that shows when the customer makes an error like entering an invalid username or password, etc...
        - **seller_home.html:** contains the UI of the seller's home page including the dashboard and the products he added

    - **static folder:**
        - **CSS folder:** includes the CSS files for font awesome library
        - **images folder:** includes the image chosen by the sellers when they add the product
        - **webfonts folder:** contains some fonts files
        - **styles.css:** includes some style for the site pages

## Screenshots
- **Login Screen**
<img src='/screenshots/screenshot-1.png' width='640' height='324'>

- **Register Screen**
<img src='/screenshots/screenshot-2.png' width='640' height='324'>

- **Seller-Home Screen**
<img src='/screenshots/screenshot-3.png' width='640' height='324'>

- **Customer-Home Screen**
<img src='/screenshots/screenshot-4.png' width='640' height='324'>

- **Search-Result Screen**
<img src='/screenshots/screenshot-5.png' width='640' height='324'>

- **Product-Details Screen**
<img src='/screenshots/screenshot-6.png' width='640' height='324'>

- **Empty-Cart Screen**
<img src='/screenshots/screenshot-7.png' width='640' height='324'>

- **Non-Empty-Cart Screen**
<img src='/screenshots/screenshot-8.png' width='640' height='324'>
    
