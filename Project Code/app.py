from flask import Flask, render_template, request, redirect, url_for
from model import *
from resources import *
from flask_cors import CORS

# ============================================== Configuration =========================================================================

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
CORS(app)
db.init_app(app)
api.init_app(app)
app.app_context().push()

# ============================================== Controllers ============================================================================


# ============================== Login ======================================================

# Welcome Page
@app.route("/", methods=["GET", "POST"])
def welcome():
    return render_template("welcome.html")



# Manager/Admin Login
@app.route("/manager_login", methods=["GET", "POST"])
def manager_login():

    if request.method == "GET":
        return render_template("manager_login.html")
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")


        managers = Manager.query.all()

        for manager in managers:
            if manager.mg_username == username and manager.mg_password == password:
                categories = Category.query.all()
                products = Product.query.all()
                return render_template("manager_dashboard.html",manager=manager, categories=categories, products = products)
            elif manager.mg_username == username and manager.mg_password != password:
                return render_template("incorrect_manager_login.html")
            elif manager.mg_username != username and manager.mg_password == password:
                return render_template("incorrect_manager_login.html")
            elif manager.mg_username != username and manager.mg_password != password:
                return render_template("access_restricted.html")
        

# New or Existing user redirection
@app.route("/existing_or_new", methods=["GET", "POST"])
def existing_or_new_customer():
    return render_template("existing_or_new.html")
        

# Customer Login
@app.route("/customer_login", methods=["GET", "POST"])
def customer_login():

    if request.method == "GET":
        return render_template("customer_login.html")
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        customers = Customer.query.all()

        for customer in customers:
            if customer.cm_username == username and customer.cm_password == password:
                categories = Category.query.all()
                products = Product.query.all()
                return render_template("customer_dashboard.html",customer=customer, categories=categories,products=products)
            elif customer.cm_username == username and customer.cm_password != password:
                return render_template("incorrect_user_login.html")
            elif customer.cm_username != username and customer.cm_password == password:
                return render_template("incorrect_user_login.html")
            
        return render_template("newuser_bridge.html")
        

# New Customer/User Signup
@app.route("/newuser_signup", methods=["GET", "POST"])
def new_customer():

    if request.method == "GET":
        return render_template("newuser_signup.html")
    
    if request.method == "POST":
        # Get details from the form
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        phonenumber = request.form.get("phonenumber")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if password1==password2 and len(phonenumber)==10:
            customers = db.session.query(Customer.cm_username).all()
            customer=[c for (c,) in customers]

            if username not in customer:
                # Create and add the object to db
                user = Customer(cm_username=username,cm_password=password1,cm_firstname=firstname,cm_lastname=lastname, cm_phonenumber=int(phonenumber))
                db.session.add(user)
                db.session.commit()
                return redirect("/customer_login")
            else:
                return render_template("existing_customer.html")
        else:
            return render_template("incorrect_user_signup.html")

#=================================================== Manager Dashboard ====================================================

# Redirect to Manager Dashboard
@app.route("/manager_dashboard", methods=["GET", "POST"])
def manager_dashboard():
    categories = Category.query.all()
    products = Product.query.all()
    manager = Manager.query.filter_by(mg_username='mg_101').first()
    return render_template("manager_dashboard.html", categories=categories, products=products, manager = manager)


# Search Categories or Products
@app.route("/search_manager", methods=["GET", "POST"])
def search_manager():
    categories = Category.query.all()
    products = Product.query.all()
    manager = Manager.query.filter_by(mg_username='mg_101').first()
    
    if request.method == "GET":
        return render_template("search_manager.html")
    
    if request.method == "POST":
        # Get details from the form

        cat = request.form.get("search_category").lower()
        prod = request.form.get("search_product").lower()

        for category in categories:
            if cat in category.category_name.lower():
                for product in products:
                    if prod in product.product_name.lower():
                        return render_template('search_manager_dashboard.html', cat=cat, prod=prod, categories=categories, products=products, manager=manager)
                return render_template('search_manager_cat_dashboard.html', cat=cat, categories=categories, products=products, manager=manager)
        return render_template('inaccurate_search_manager.html')

#========================= Category CRUD =================================

# Add Categories
@app.route("/add_categories", methods=["GET", "POST"])
def add_categories():

    if request.method == "GET":
        return render_template("add_categories.html")
    
    if request.method == "POST":
        # Get details from the form
        categoryname = request.form.get("category_name")

        category = db.session.query(Category.category_name).all()
        categories = [c for (c,) in category]

        if categoryname not in categories:
            # Create and add the object to db
            category = Category(category_name=categoryname)
            db.session.add(category)
            db.session.commit()

            # Render template
            return redirect("/manager_dashboard")
        else:
            return render_template("existing_section.html")

    
# Update Categories
@app.route("/update_categories/<int:category_id>", methods=["GET", "POST"])
def upd_categories(category_id):

    if request.method == "GET":
        c1 = Category.query.get(category_id)
        return render_template("update_categories.html",c1=c1)
    
    if request.method == "POST":
        # Get details from the form
        categoryname = request.form.get("category_name")

        category = db.session.query(Category.category_name).all()
        categories = [c for (c,) in category]

        if categoryname not in categories:
            # Update the object to db
            category = Category.query.get(category_id)
            category.category_name = categoryname
            db.session.commit()

            # Render template
            return redirect("/manager_dashboard")
        else:
            return render_template("existing_section.html")


# Delete Categories
@app.route("/delete_categories/<int:category_id>", methods=["GET", "POST"])
def del_categories(category_id):
    c1 = Category.query.get(category_id)
    products = c1.Products
    for product in products:
        db.session.delete(product)
    db.session.commit()
    db.session.delete(c1)
    db.session.commit()
    return redirect("/manager_dashboard")

#========================= Products CRUD ===============================

# Add Products to a Category
@app.route("/add_products/<int:category_id>", methods=["GET", "POST"])
def add_products(category_id):
    c1 = Category.query.get(category_id)

    if request.method == "GET":
        return render_template("add_products.html",category_id=category_id, c1=c1)
    
    if request.method == "POST":
        # Get details from the form
        product_name = request.form.get("product_name")
        unit = request.form.get("unit")
        price = int(request.form.get("price_unit"))
        stock = int(request.form.get("quantity"))
        ecategory_id = category_id

        product = db.session.query(Product.product_name).all()
        products = [c for (c,) in product]

        if product_name not in products:
            # Create and add the object to db
            product = Product(product_name=product_name, price = price,unit=unit, stock=stock, ecategory_id=ecategory_id)
            db.session.add(product)
            db.session.commit()

            # Render template
            return redirect("/manager_dashboard")
        else:
            return render_template("existing_section.html")
    
    
# Update Products of a Category
@app.route("/update_products/<int:category_id>/<int:product_id>", methods=["GET", "POST"])
def upd_products(category_id,product_id):

    if request.method == "GET":
        p1 = Product.query.get(product_id)
        c1 = Category.query.get(category_id)
        return render_template("update_products.html",category_id=category_id,p1=p1, c1=c1)
    
    if request.method == "POST":
        # Get details from the form
        category_name = request.form.get("category_name")
        product_name = request.form.get("product_name")
        unit = request.form.get("unit")
        price = int(request.form.get("price_unit"))
        stock = int(request.form.get("quantity"))

        category = db.session.query(Category.category_name).all()
        categories = [c for (c,) in category]

        if category_name in categories:
            # Update the object to db
            product = Product.query.get(product_id)
            product.product_name = product_name
            product.price = price
            product.unit = unit
            product.stock = stock
            cat = Category.query.filter_by(category_name=category_name).first()
            product.ecategory_id = cat.category_id
            db.session.commit()

            # Render template
            return redirect("/manager_dashboard")
        else:
            return render_template("existing_section_prod.html")
    

# Delete Products
@app.route("/delete_products/<int:category_id>/<int:product_id>", methods=["GET", "POST"])
def del_products(category_id,product_id):
    p1 = Product.query.get(product_id)
    db.session.delete(p1)
    db.session.commit()
    return redirect("/manager_dashboard")

#================================== Summary =====================================

# Summary
@app.route("/summary", methods=["GET", "POST"])
def summary():
    categories = Category.query.all()
    products = Product.query.all()
    orders = Order.query.all()
    customers = Customer.query.all()

    # Plotting Products count
    prod_list = []
    for product in products:
        prod_list.append((product.product_id,product.product_name))

    prod_dict = dict()
    for prod in prod_list:
        prod_dict[prod]=0
    
    for item in orders:
        for prod in prod_dict:
            if item.o_product_id == prod[0]:
                prod_dict[prod]+=1
                break


    # Plotting Categories count
    cat_list = []
    for category in categories:
        cat_list.append((category.category_id,category.category_name))
    
    cat_dict = dict()
    for cat in cat_list:
        cat_dict[cat]=0
    
    for item in orders:
        for cat in cat_dict:
            if item.o_category_id == cat[0]:
                cat_dict[cat]+=1
                break
        

    # Valuable customers
    cust_list = []
    for customer in customers:
        cust_list.append((customer.cm_id,customer.cm_firstname,customer.cm_lastname))
    
    cust_dict = dict()
    for cust in cust_list:
        cust_dict[cust]=0
    
    for item in orders:
        for cust in cust_dict:
            if item.o_user_id == cust[0]:
                cust_dict[cust]+=item.o_totalprice


    return render_template('summary.html', prod_dict=prod_dict, cat_dict=cat_dict, cust_dict=cust_dict)



#=================================================== User Dashboard ====================================================

#Show list of Categories
@app.route("/customer_dashboard/<int:cm_id>", methods=["GET", "POST"])
def customer_all_categories(cm_id):
    categories = Category.query.all()
    products = Product.query.all()
    customer = Customer.query.get(cm_id)
    return render_template("customer_dashboard.html", categories=categories, products=products, customer = customer)



# Search Categories or Products
@app.route("/search/<int:cm_id>", methods=["GET", "POST"])
def search(cm_id):
    categories = Category.query.all()
    products = Product.query.all()
    customer = Customer.query.get(cm_id)
    
    if request.method == "GET":
        return render_template("search.html", customer=customer)
    
    if request.method == "POST":
        # Get details from the form

        cat = request.form.get("search_category").lower()
        prod = request.form.get("search_product").lower()

        for category in categories:
            if cat in category.category_name.lower():
                for product in products:
                    if prod in product.product_name.lower():
                        return render_template('search_user_dashboard.html', cat=cat, prod=prod, categories=categories, products=products, customer=customer)
                return render_template('search_user_cat_dashboard.html', cat=cat, categories=categories, products=products, customer=customer)    
        return render_template('incorrect_search.html', customer=customer)


#================================== Purchase Related =====================================

# Purchase Products
@app.route("/customer_purchase/<int:cm_id>/<int:category_id>/<int:product_id>", methods=["GET", "POST"])
def customer_purchase(cm_id,category_id,product_id):

    c1 = Category.query.get(category_id)
    p1 = Product.query.get(product_id)
    u1 = Customer.query.get(cm_id)

    if request.method == "GET":
        return render_template("customer_purchase.html",c1=c1,p1=p1,u1=u1)
    
    if request.method == "POST":
        # Get details from the form
    
        quantity = int(request.form.get("quantity"))
        
        if quantity>p1.stock:
            return render_template("out_of_stock.html",c1=c1,p1=p1,u1=u1)
        else:
            totalprice = p1.price*quantity
            return render_template("customer_total.html",c1=c1,p1=p1,u1=u1,quantity=quantity,totalprice=totalprice)
        

# Purchase Products Total
@app.route("/customer_total/<int:cm_id>/<int:category_id>/<int:product_id>/<int:quantity>", methods=["GET", "POST"])
def customer_total(cm_id,category_id,product_id,quantity):
    c1 = Category.query.get(category_id)
    p1 = Product.query.get(product_id)
    u1 = Customer.query.get(cm_id)
    totalprice = p1.price*quantity

    if request.method == "POST":

        # Create and add the object to db
        cart = Cart(c_user_id=u1.cm_id, c_category_id=c1.category_id, c_product_id=p1.product_id, c_price = p1.price, c_quantity=quantity, c_totalprice=totalprice)
        db.session.add(cart)


        db.session.commit()
        return redirect(url_for('customer_all_categories', cm_id=cm_id))
    
#============================== Cart ========================================

#Show Cart
@app.route("/cart/<int:cm_id>", methods=["GET", "POST"])
def all_cart(cm_id):
    u1 = Customer.query.get(cm_id)
    cart = Cart.query.filter_by(c_user_id=u1.cm_id).all()
    categories = Category.query.all()
    products = Product.query.all()

    totalvalue=0
    for item in cart:
        totalvalue += item.c_price * item.c_quantity
    
    if request.method == "GET":
        return render_template("cart.html", u1=u1,cart=cart,totalvalue=totalvalue, categories=categories, products=products)
    
    if request.method == "POST":
        return redirect(url_for('orders',cm_id=cm_id))

# Update items in Cart
@app.route("/cart/<int:cm_id>/update/<int:cart_id>", methods=["GET", "POST"])
def update_cart(cm_id,cart_id):
    item = Cart.query.filter_by(cart_id=cart_id).first()
    c1 = Category.query.get(item.c_category_id)
    p1 = Product.query.get(item.c_product_id)
    u1 = Customer.query.get(cm_id)


    if request.method == "GET":
       return render_template("update_customer_purchase.html",item=item,p1=p1,c1=c1,u1=u1)
    
    if request.method == "POST":

        quantity = int(request.form.get("quantity"))
        if quantity>p1.stock:
            return render_template("update_out_of_stock.html",c1=c1,p1=p1,u1=u1,item=item)
        else:
            totalprice = p1.price*quantity
            return render_template("update_customer_total.html",c1=c1,p1=p1,u1=u1,quantity=quantity,totalprice=totalprice,item=item)
        

# Update items in Cart continued
@app.route("/cart/<int:cm_id>/update/<int:cart_id>/<int:quantity>", methods=["GET", "POST"])
def update_total_cart(cm_id,cart_id,quantity):

    item = Cart.query.filter_by(cart_id=cart_id).first()
    c1 = Category.query.get(item.c_category_id)
    p1 = Product.query.get(item.c_product_id)
    u1 = Customer.query.get(cm_id)
    totalprice = p1.price*quantity

    if request.method == "POST":
        item.c_quantity = quantity
        item.c_totalprice = totalprice
        db.session.commit()
        return redirect(url_for('all_cart',cm_id=cm_id))



# Delete items from Cart
@app.route("/cart/<int:cm_id>/delete/<int:cart_id>", methods=["GET", "POST"])
def delete_cart(cm_id,cart_id):
    item = Cart.query.filter_by(cart_id=cart_id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('all_cart',cm_id=cm_id))

#================================= Order =================================================

# Place Order
@app.route("/order/<int:cm_id>", methods=["GET", "POST"])
def orders(cm_id):
    items = Cart.query.filter_by(c_user_id=cm_id).all()
    categories = Category.query.all()
    products = Product.query.all()

    # Assigning order number
    orders = Order.query.all()
    if len(orders)==0:
        ord_no = 1
    else:
        ord_no=0
        for order in orders:
            if int(order.order_id) > ord_no:
                ord_no=int(order.order_id)
        ord_no+=1

    if request.method == "POST":
        for item in items:
            p1 = Product.query.get(item.c_product_id)
            c1 = Category.query.get(item.c_category_id)
            u1 = Customer.query.get(item.c_user_id)
            stock = p1.stock
            stock -= item.c_quantity
            if stock<0:
                return render_template("order_out_of_stock.html",p1=p1,c1=c1,item=item,u1=u1)
            else:
                p1.stock = stock
                order = Order(o_user_id=item.c_user_id, o_category_id = item.c_category_id, o_product_id = item.c_product_id, o_quantity=item.c_quantity, o_price=item.c_price, o_totalprice=item.c_totalprice, o_orderno=ord_no)
                db.session.add(order)
                db.session.commit()

        orders = Order.query.all()
        totalvalue=0
        for order in orders:
            if ord_no == order.o_orderno:
                totalvalue += order.o_totalprice
        
        for item in items:
            db.session.delete(item)
            db.session.commit()

        return render_template("order_placed.html",orders=orders,ord_no=ord_no, totalvalue=totalvalue, cm_id=cm_id, categories=categories, products=products)


# View Past Orders
@app.route("/orders_history/<int:cm_id>", methods=["GET", "POST"])
def orders_history(cm_id):
    orders = Order.query.filter_by(o_user_id=cm_id).order_by(Order.o_orderno.desc()).all()
    u1 = Customer.query.get(cm_id)
    categories = Category.query.all()
    products = Product.query.all()
    var=1

    return render_template("orders_history.html",u1=u1, orders=orders, categories=categories, products=products,var=var)


#================================= Profile =================================================

#Show Profile
@app.route("/profile/<int:cm_id>", methods=["GET", "POST"])
def profile(cm_id):
    u1 = Customer.query.get(cm_id)

    if request.method == "GET":
        return render_template("profile.html",u1=u1)
    
    if request.method == "POST":
        # Get details from the form
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        phonenumber = request.form.get("phonenumber")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if password1==password2 and len(phonenumber)==10:
            u1.cm_firstname = firstname
            u1.cm_lastname = lastname
            u1.cm_phonenumber = int(phonenumber)
            u1.cm_password = password1
            db.session.commit()
            return redirect(url_for('customer_all_categories', cm_id=cm_id))
        else:
            return render_template("incorrect_user_update.html",u1=u1)


#============================================== Running the App ===========================================================================

if __name__== '__main__':
    app.run(debug=True)