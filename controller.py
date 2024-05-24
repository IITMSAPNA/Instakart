from flask import Flask , render_template, request, redirect, url_for, session
from app import app
from model import *
import os 
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from wtforms.validators import ValidationError
from flask_restful import Api
from werkzeug.utils import secure_filename
import seaborn as sns
import matplotlib.pyplot as plt


app.secret_key=os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'static/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','avif','webp'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def image(filename):
        file = filename
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if filename:
            image = '/static' + filename
        return filename 


@app.route("/")
def hello_world():
    if "user_id" in session:
        product_list = postman.query(Product).order_by(Product.id.desc()).all()
        categories_list = postman.query(Category).order_by(Category.id.desc()).all()
        return render_template('index.html', products = product_list, categories = categories_list)
    else:
        return redirect("/sign-in")
    

@app.route('/sign-in')
def sign_in():
    return render_template('signin.html')


@app.route('/admin-sign_in')
def adminSign_in():
    return render_template('admin-sign-in.html')


@app.route('/logout')
def logout():
    if "user_id" in session:
        session.pop("user_id")
        return redirect('/sign-in')
    return redirect('/sign_in')


@app.route("/cart", methods=['GET','POST'])
def cart():
    if "user_id" in session:
        if request.method=="POST":
            product_id = request.form['product_id']
            product_name = request.form['product_name']
            product_price = request.form['product_price']
            product_quantity = request.form['product_quantity']
            # TODO user_id add krna h cart m     Cart(user_id, product_id, product_quantity,product_price,product_name)
            cart=Cart(1, product_id, product_quantity,product_price,product_name)
            postman.add(cart)
            postman.commit()
        cart_list = postman.query(Cart).all()
        return render_template('cart.html', carts = cart_list)
    return redirect('/sign_in')


@app.route("/cart/delete/<int:id>", methods=['GET','POST'])
def cart_delete(id):
    if "user_id" in session:
        if request.method=="POST":
            print(postman.query(Cart).filter(Cart.id==id))
            postman.query(Cart).filter(Cart.id==id).delete()
            postman.commit()
        return redirect(url_for("cart"))
    return redirect('/sign_in')

@app.route('/place_order')
def place_order():
    return render_template('place_order.html')


@app.route("/search", methods=['POST'])
def searchbox():
    if request.method=="POST":
        search_value=request.form['searchbox']
        products=postman.query(Product).filter(Product.name.like("%"+search_value+"%"))
        categories=postman.query(Category).filter(Category.name.like("%"+search_value+"%"))

        return render_template('searchpage.html', products=products, categories=categories)
    

@app.route('/admin')
def adminpage():
    if "admin_id" in session:
        product_list = postman.query(Product).all()
        categories_list = postman.query(Category).all()
        return render_template('adminpage.html', products = product_list, categories = categories_list)
    return redirect('/admin-sign_in')


# id is of product
@app.route('/admin/edit_product/<int:product_id>', methods=['GET','POST'])
def editproductpage(product_id):
    if "admin_id" in session:
        if request.method == 'POST':
            
            edit_product = postman.query(Product).filter(Product.id==product_id).update({
                Product.name:request.form['pn'],
                Product.category:request.form['product_category'],
                Product.description:request.form['product_description'],
                Product.price:request.form['product_price'],
                Product.quantity:request.form['product_quantity'],
                Product.is_available:request.form['product_is_available'],
                Product.manufacturing_date:request.form['product_manufacturing_date'],
                Product.expiry_date:request.form['product_expiry_date']
            })
            postman.commit()
            return redirect('/admin')
        else:
            edit_product = postman.query(Product).filter(Product.id==product_id).first()
            return render_template('editproduct.html', product = edit_product)
    return redirect('/admin-sign_in')


@app.route('/admin/new_product', methods=['GET','POST'])
def newproductpage():
    if "admin_id" in session:
        if request.method == 'POST':           
            new_product = Product(
                name = request.form['pn'],
                category = request.form['product_category'],
                description = request.form['product_description'],
                price = request.form['product_price'],                
                quantity = request.form['product_quantity'],
                is_available = request.form['product_is_available'],
                manufacturing_date = request.form['product_manufacturing_date'],
                expiry_date = request.form['product_expiry_date'],
                image=image(request.files['file'])
                )
            postman.add(new_product)
            postman.commit()
            return redirect('/admin')
        else:
            return render_template('new_product.html')
    return redirect('/admin-sign_in')
    


@app.route("/admin/delete_product/<int:id>", methods=['POST'])
def admin_product_delete(id):
    if request.method=="POST":
        print(postman.query(Product).filter(Product.id==id))
        postman.query(Product).filter(Product.id==id).delete()
        postman.commit()
    return redirect('/admin') 



# id is of category
@app.route('/admin/edit_category', methods=['GET','POST'])
def editcategory():
    if "admin_id" in session:
        categories = postman.query(Category).all()
        categories = [category for category in categories]
        return render_template('edit_category.html', categories=categories)
    return redirect('/admin-sign_in')


@app.route('/admin/updatecategory/<int:id>', methods=["GET","POST"])
def updatecategory(id):
    if "admin_id" in session: 
        if request.method == "POST":
            New_category_name = request.form.get('Category_Name')
            file = request.files['file']
            filename = None
            #Check if uploaded image file has allowed extension
            if (file and allowed_file(file.filename)):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            current = postman.query(Category).filter_by(id=id).first()
            try:
                current.name = New_category_name
                if filename:
                    current.image = filename
                postman.commit()
                return redirect('/admin/edit_category')
            except Exception as e:
                postman.rollback()
                return f"{e}"
        category = postman.query(Category).filter_by(id=id).first()
        return render_template('update_category.html', category=category)
    return redirect('/admin-sign_in')


@app.route('/admin/UpdateNewCategory', methods=["GET","POST"])
def UpdateNewCategory():
    if "admin_id" in session:
        if request.method == "POST":
            New_category_name = request.form.get('Category_Name')
            file = request.files['file']
            filename = None
            #Check if uploaded image file has allowed extension
            if (file and allowed_file(file.filename)):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            try:
                new_category = Category(name=New_category_name, image=filename)
                postman.add(new_category)
                postman.commit()
                return redirect('/admin/edit_category')
            except Exception as e:
                postman.rollback()
                return f"{e}"
        return render_template('new_category.html')
    return redirect('/admin-sign_in')


@app.route("/admin/delete_category/<int:id>", methods=['POST'])
def admin_category_delete(id):
    if request.method=="POST":
        print(postman.query(Category).filter(Category.id==id))
        postman.query(Category).filter(Category.id==id).delete()
        postman.commit()
    return redirect('/admin/edit_category')     
    

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        # print("line_12")
        username = request.form['email']
        password = request.form['password']
        valid = postman.query(Customer).filter_by(email=username, password=password).first()
        if valid:
            session['user_id'] = valid.id
            return redirect('/')
    return redirect('/sign-in')
    


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        print("line_26")
        username = request.form['email']
        password = request.form['password']
        valid = postman.query(Admin).filter_by(email=username, password=password).first()
        if valid:
            session["admin_id"] = valid.id
            return redirect('/admin')
        else:
            return "You Are not admin"
    return redirect('/sign-in')


@app.route('/logout-admin')
def admin_logout():
    if "admin_id" in session:
        session.pop("admin_id")
        return redirect('/admin-sign_in')
    return redirect('/admin-sign_in')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print("line_40")
        email = request.form.get('email')
        password = request.form.get('password')
        fullname = request.form.get('fullname')
        address = request.form.get('address')
        phone_no = request.form.get('phone_no')
        def valid_username(self, username):
            excisting_user = postman.query(Customer).filter_by(user_name=username).first()
            if excisting_user:
                raise ValidationError('Username already exists')
            else:
                return True
        if valid_username:
            customer = Customer(fullname=fullname, email=email, password=password, address=address, phone_no=phone_no)
            postman.add(customer)
            postman.commit()
        return redirect(url_for('user_login'))
    else:
        return render_template('Sign-up.html')


from api import Productapi, Categoryapi
api=Api(app)
api.add_resource(Productapi, '/api/products', '/api/products/<int:id>')
api.add_resource(Categoryapi, '/api/categories', '/api/categories/<int:id>')




@app.route("/admin/summary")
def admin_summary():
    #Checks if "admin_id" key exists in the session
    if "admin_id" in session: 
        cat = postman.query(Product).all()
        # Sample data
        categories = list(filter(None, [item.category for item in cat]))
        values = list(filter(None, [item.quantity for item in cat]))
        
        # Create a bar plot using Seaborn
        sns.set(style="whitegrid")  # Set the style of the plot
        plt.figure(figsize=(16, 12))  # Set the figure size

        # Create the bar plot
        sns.barplot(x=categories, y=values, palette="viridis")

        # Add labels and title
        plt.xlabel("Categories")
        plt.ylabel("Product Quantity")
        plt.title("Bar Plot Example")

        # Display the plot
        plt.savefig('static/category_count.png')
        return render_template('admin_summary.html')
    
    return redirect('/admin-sign_in')