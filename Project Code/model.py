from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#=============================================== Products and Categories =======================================================

class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer(), primary_key = True, autoincrement=True)
    category_name = db.Column(db.String(), unique = True, nullable = False)

    Products = db.relationship("Product", back_populates = "Categories")


class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer(), primary_key = True, autoincrement=True)
    product_name = db.Column(db.String(), unique = True, nullable = False)
    unit = db.Column(db.String(), nullable = False)
    price = db.Column(db.Integer(), nullable = False)
    stock = db.Column(db.Integer(), nullable = False)
    ecategory_id = db.Column(db.Integer(), db.ForeignKey("category.category_id"), nullable = False)

    Categories = db.relationship("Category", back_populates = "Products")



#=============================================== Manager and Customers =======================================================

class Manager(db.Model):
    __tablename__ = 'manager'
    mg_id = db.Column(db.Integer(), primary_key = True, autoincrement=True)
    mg_username = db.Column(db.String(), unique = True, nullable = False)
    mg_password = db.Column(db.String(), nullable = False)

class Customer(db.Model):
    __tablename__ = 'customer'
    cm_id = db.Column(db.Integer(), primary_key = True, autoincrement=True)
    cm_firstname = db.Column(db.String(), nullable = False) 
    cm_lastname = db.Column(db.String(), nullable = False)
    cm_phonenumber = db.Column(db.Integer(), nullable = False)
    cm_username = db.Column(db.String(), unique = True, nullable = False)
    cm_password = db.Column(db.String(), nullable = False)


#=============================================== Cart and Orders =============================================================

class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer(), primary_key = True, autoincrement=True)
    c_user_id = db.Column(db.Integer(), db.ForeignKey("customer.cm_id"), nullable = False)
    c_category_id = db.Column(db.Integer(), db.ForeignKey("category.category_id"), nullable = False)
    c_product_id = db.Column(db.Integer(), db.ForeignKey("product.product_id"), nullable = False)
    c_quantity = db.Column(db.Integer(), nullable = False)
    c_price = db.Column(db.Integer(), db.ForeignKey("product.price"), nullable = False)
    c_totalprice = db.Column(db.Integer(), nullable = False)



class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer(), primary_key = True, autoincrement=True)
    o_user_id = db.Column(db.Integer(), db.ForeignKey("customer.cm_id"), nullable = False)
    o_category_id = db.Column(db.Integer(), db.ForeignKey("category.category_id"), nullable = False)
    o_product_id = db.Column(db.Integer(), db.ForeignKey("product.product_id"), nullable = False)
    o_quantity = db.Column(db.Integer(), nullable = False)
    o_price = db.Column(db.Integer(), db.ForeignKey("product.price"), nullable = False)
    o_totalprice = db.Column(db.Integer(), nullable = False)
    o_orderno = db.Column(db.Integer(), nullable = False)