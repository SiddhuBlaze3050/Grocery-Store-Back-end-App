from flask_restful import Api, Resource, reqparse
from model import *
from validation import *

api = Api()

#================================================ API Parsing Arguments ====================================================

# Update/PUT Parsers
update_category_parser = reqparse.RequestParser()
update_category_parser.add_argument("category_name")


update_product_parser = reqparse.RequestParser()
update_product_parser.add_argument("product_name")
update_product_parser.add_argument("unit")
update_product_parser.add_argument("price_unit")
update_product_parser.add_argument("quantity")


# Create/POST Parsers

create_category_parser = reqparse.RequestParser()
create_category_parser.add_argument("category_name")


create_product_parser = reqparse.RequestParser()
create_product_parser.add_argument("product_name")
create_product_parser.add_argument("unit")
create_product_parser.add_argument("price_unit")
create_product_parser.add_argument("quantity")


#=================================================== API Classes ===========================================================

#======================================= Categories CRUD ==============================================

class Api_categories(Resource):

    # Create Category details
    def post(self):
        cat_info = create_category_parser.parse_args()
        category_name = cat_info.get("category_name", None)

        category = db.session.query(Category.category_name).all()
        categories = [c for (c,) in category]
        
        if category_name is None or not category_name:
            return {
                        "error_code": "CATEGORY001",
                        "error_message": "Category Name is required"
                    }, 400
        
        if category_name in categories:
            raise NotFoundError(status_code=409)
        

        new_category = Category(category_name=category_name)
        db.session.add(new_category)
        db.session.commit()

        return {
                "category_id": new_category.category_id,
                "category_name": new_category.category_name
        }, 201
    


    # Get Category details
    def get(self):
        all_categories = []
        c1 = Category.query.all()
        
        if c1:
            for category in c1:
                all_categories.append(
                    {
                        "category_id": category.category_id,
                        "category_name": category.category_name
                    }
                )
            return all_categories        
        else:
            raise NotFoundError(status_code=404)
    

    # Update Category details
    def put(self,category_id):
        cat_info = update_category_parser.parse_args()
        category_name = cat_info.get("category_name", None)

        cat_update = Category.query.get(category_id)
        all_categories = Category.query.all()

        category = db.session.query(Category.category_name).all()
        categories = [c for (c,) in category]

        if cat_update not in all_categories:
            raise NotFoundError(status_code=404)
        
        if category_name is None or not category_name:
            return {
                        "error_code": "CATEGORY001",
                        "error_message": "Category Name is required"
                    }, 400

        if category_name in categories:
            raise NotFoundError(status_code=409)

        cat_update.category_name = category_name
        db.session.commit()

        return {
                "category_id": cat_update.category_id,
                "category_name": cat_update.category_name
        }, 201
    

    # Delete category details
    def delete(self, category_id):
        category =  Category.query.get(category_id)

        if category is None:
            raise NotFoundError(status_code=404)
        
        products = category.Products
        for product in products:
            db.session.delete(product)
        db.session.commit()        

        db.session.delete(category)
        db.session.commit()
        return "", 202

    
#======================================= Products CRUD ==================================================

class Api_products(Resource):

    # Create Product details
    def post(self,category_id):
        prod_info = create_product_parser.parse_args()
        product_name = prod_info.get("product_name", None)
        unit = prod_info.get("unit", None)
        price = prod_info.get("price_unit", None)
        stock = prod_info.get("quantity", None)
        ecategory_id = category_id

        product = db.session.query(Product.product_name).all()
        products = [c for (c,) in product]
        
        if product_name is None or not product_name:
            return {
                        "error_code": "PRODUCT001",
                        "error_message": "Product Name is required"
                    }, 400

        if unit is None or not unit:
            return {
                        "error_code": "PRODUCT002",
                        "error_message": "Units are required"
                    }, 400
        
        if price is None or not price:
            return {
                        "error_code": "PRODUCT003",
                        "error_message": "Price is required"
                    }, 400 
        
        if stock is None or not stock:
            return {
                        "error_code": "PRODUCT004",
                        "error_message": "Quantity is required"
                    }, 400
        
        if product_name in products:
            raise NotFoundError(status_code=409)

        new_product = Product(product_name=product_name, price = int(price),unit=unit, stock=int(stock), ecategory_id=ecategory_id)
        db.session.add(new_product)
        db.session.commit()

        return {
                "product_id": new_product.product_id,
                "product_name": new_product.product_name,
                "unit": new_product.unit,
                "price": new_product.price,
                "stock": new_product.stock,
                "ecategory_id": new_product.ecategory_id
        }, 201
    

    # Get Product Details
    def get(self):
        all_products = []
        p1 = Product.query.all()

        if p1:
            for product in p1:
                all_products.append(
                    {
                        "product_id": product.product_id,
                        "product_name": product.product_name,
                        "unit": product.unit,
                        "price": product.price,
                        "stock": product.stock,
                        "ecategory_id": product.ecategory_id
                    }
                )
            
            return all_products
        
        else:
            raise NotFoundError(status_code=404)
        
    # Update Product details
    def put(self,product_id):
        prod_info = update_product_parser.parse_args()
        product_name = prod_info.get("product_name", None)
        unit = prod_info.get("unit", None)
        price = prod_info.get("price_unit", None)
        stock = prod_info.get("quantity", None)

        prod_update = Product.query.get(product_id)
        all_products = Product.query.all()

        product = db.session.query(Product.product_name).all()
        products = [c for (c,) in product]
        prod_obj = Product.query.filter_by(product_name=product_name).first()
        

        if prod_update not in all_products:
            raise NotFoundError(status_code=404)
        
        if product_name is None or not product_name:
            return {
                        "error_code": "PRODUCT001",
                        "error_message": "Product Name is required"
                    }, 400

        if unit is None or not unit:
            return {
                        "error_code": "PRODUCT002",
                        "error_message": "Units are required"
                    }, 400
        
        if price is None or not price:
            return {
                        "error_code": "PRODUCT003",
                        "error_message": "Price is required"
                    }, 400 
        
        if stock is None or not stock:
            return {
                        "error_code": "PRODUCT004",
                        "error_message": "Quantity is required"
                    }, 400
        
        if product_name in products and prod_obj.product_id != product_id:
            raise NotFoundError(status_code=409)

        prod_update.product_name = product_name
        prod_update.unit = unit
        prod_update.price = int(price)
        prod_update.stock = int(stock)
        db.session.commit()

        return {
                "product_id": prod_update.product_id,
                "product_name": prod_update.product_name,
                "unit": prod_update.unit,
                "price": prod_update.price,
                "stock": prod_update.stock,
                "ecategory_id": prod_update.ecategory_id
        }, 201
    

    # Delete product details
    def delete(self, product_id):
        product =  Product.query.get(product_id)

        if product is None:
            raise NotFoundError(status_code=404)

        db.session.delete(product)
        db.session.commit()
        return "", 202



#================================================= API Endpoints ===========================================================

api.add_resource(Api_categories, "/api/category", "/api/category/<int:category_id>")
api.add_resource(Api_products, "/api/product", "/api/category/<int:category_id>/product", "/api/product/<int:product_id>")