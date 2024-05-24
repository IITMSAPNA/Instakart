from flask_restful import Resource
from model import *
from flask import request


class Categoryapi(Resource):
    def get(self, id=None):
        if id:
            categories = postman.query(Category).filter(Category.id==id).first()
            if categories:
                return {
                "name": categories.name,
                "image": categories.image,
                }
            else:
                return {"message": "Category not found"}, 404
        else:
            categories = postman.query(Category).all()
            cat={}
            for category in categories:
                cat[category.id] = {
                    "name": category.name,
                    "image": category.image,
                }
               
            return cat
        
    def post(self):
        data = request.get_json()
        name = data.get("name")
        image = data.get("image")
        username = data.get("username")
        password = data.get("password")
        admin = (
            postman.query(Admin).filter(Admin.username == username).filter(Admin.password == password).first()
        )
        if admin :
            # add_category = postman.query(Category).filter(Category.name == name).first()
            add_category = Category(name=name, image=image)
            postman.add(add_category)
            postman.commit()
            return {"message": "Category created successfully"}, 201
        else:
            return {"message": "Admin not found"}, 404
        
    def put(self, id):
        category = postman.query(Category).filter(Category.id == id).first()
        data = request.get_json()
        name = data.get("name")
        image = data.get("image")
        username = data.get("username")
        password = data.get("password")
        admin = (
            postman.query(Admin).filter(Admin.username == username).filter(Admin.password == password).first()
        )
        if admin :
            category.name = name
            category.image = image
            postman.commit()
            return {"message": "Category updated successfully"}, 201
        else:
            return {"message": "Admin not found"}, 404
        
    def delete(self, id):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        admin = (
            postman.query(Admin).filter(Admin.username == username).filter(Admin.password == password).first()
        )
        if admin :
            category = postman.query(Category).filter(Category.id == id).first()
            if category:
                category.delete()
                postman.commit()
                return {"message": "Category deleted successfully"}, 201
            else:
                return {"message": "Category not found"}, 404
        else:
            return {"message": "Admin not found"}, 404
        


class Productapi(Resource):
    def get(self , id=None):
        if id:
            product = postman.query(Product).filter(Product.id == id).first()
            if product:
                return {
                    "name": product.name,
                    "image": "http://127.0.0.1:5000/static/" + product.image,
                    "quantity": product.quantity,
                    "price": product.price,
                    "cat": product.category,
                }, 200
            else:
                return {"message": "product not found"}, 404
        else:
            product = postman.query(Product).all()
        # return [i.serialize() for i in product], 200
            pro=dict()
            for i in product:
                pro[i.id]={
                    "name": i.name,
                    "image": "http://127.0.0.1.5000/static/" + i.image,
                    "quantity": i.quantity,
                    "price": i.price,
                    "cat": i.category
                }
            return pro
        
    def post(self):
        data = request.get_json()
        name = data.get("name")
        username = data.get("username")
        password = data.get("password")
        image = "/static/temp.jpg"
        quantity = data.get("quantity")
        price = data.get("price")
        category = data.get("category")
        is_available = data.get("is_available")
        description = data.get("desc")
        manufacturing_date = data.get("manufacturing_date")
        expiry_date = data.get("expiry_date")
        admin = (
            postman.query(Admin).filter(Admin.username == username).filter(Admin.password == password).first()
        )
        if admin:
            add_product = Product(
                name=name, image=image, quantity=quantity, price=price, category=category, is_available=is_available, description=description, manufacturing_date=manufacturing_date, expiry_date=expiry_date
            )
            postman.add(add_product)
            postman.commit()
            return {"message": "product created successfully"}, 201
        else:
            return {"message": "Admin not found"}, 404
        

    def put(self, id):
        product = Product.query.filter(id==id).first()
        data=request.get_json()
        username = data.get("username")
        password = data.get("password")
        product.name = data.get("name")
        product.image = data.get("image")
        product.quantity = data.get("quantity")
        product.price = data.get("price")
        product.category = data.get("category")
        product.is_available = data.get("is_available")
        product.description = data.get("desc")
        product.manufacturing_date = data.get("manufacturing_date")
        product.expiry_date = data.get("expiry_date")
        admin = (
            postman.query(Admin).filter(Admin.username == username).filter(Admin.password == password).first()
        )
        if admin:
            if product:
                product.name = "name"
                product.image = "image"
                product.quantity = "quantity"
                product.price = "price"
                product.category = "category"
                product.is_available = "is_available"
                product.description = "description"
                product.manufacturing_date = "manufacturing_date"
                product.expiry_date = "expiry_date"
                postman.commit()
                return {"message": "product updated successfully"}, 200
            else:
                return {"message": "product not found"}, 404
        else:
            return {"message": "Admin not found"}, 404
        

    def delete(self, id):
        data=request.get_json()
        username = data.get("username")
        password = data.get("password")
        admin = (
            postman.query(Admin).filter(Admin.username == username).filter(Admin.password == password).first()
        )
        if admin:
            product = Product.query.filter(Product.id==id).first()
            if product:
                product.delete()
                return {"message": "product deleted successfully"}, 200
            else:
                return {"message": "product not found"}, 404
        else:
            return {"message": "Admin not found"}, 404




        