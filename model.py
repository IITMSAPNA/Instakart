
from sqlalchemy import create_engine, Column, Integer, String, update, delete
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///godam.sqlite3', echo=True)
Session = sessionmaker(bind=engine)


Base = declarative_base()
postman = Session()
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column('name',String)
    category = Column('category',String)
    description = Column('description',String)
    image = Column('image', String)
    price = Column('price', Integer)
    quantity = Column('quantity',Integer)
    is_available = Column('is_available',Integer)
    manufacturing_date = Column('manufacturing_date',String)
    expiry_date = Column('expiry_date',String)
    
    def __init__(self, name, category, image, price, quantity, description, is_available, manufacturing_date, expiry_date ):
        self.name = name
        self.category = category
        self.image = image
        self.price = price
        self.quantity = quantity
        self.description = description
        self.is_available = is_available
        self.manufacturing_date = manufacturing_date
        self.expiry_date = expiry_date



class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column('name',String)
    image = Column('image', String)
    
    def __init__(self, name, image):
        self.name = name
        self.image = image

class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column('user_id',Integer)
    item_id = Column('item_id', Integer)
    quantity = Column('quantity',Integer)
    created_at = Column('created_at', String)
    price = Column('price',Integer)
    name = Column('name',String)
    total = Column('total',Integer)
    
    def __init__(self, user_id, item_id, quantity, price, name):
        self.user_id = user_id
        self.item_id = item_id
        self.quantity = quantity
        self.price = price
        self.name = name
        self.created_at = datetime.now()
        self.total = int(self.quantity) * int(self.price)

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column('fullname', String)
    email = Column('email', String)
    password = Column('password', String)
    address =Column('address', String)
    phone_no = Column('phone_n0', Integer)

    def __init__(self, fullname, email, password, address, phone_no):
        self.fullname = fullname
        self.email = email
        self.password = password
        self.address = address
        self.phone_no =  phone_no

class Admin(Base):
    __tablename__ = 'Admin'
    email = Column('email',String)
    id = Column('id', Integer, primary_key=True)
    password = Column('password', String)

    def __init__(self, email, password):
        self.email = email
        self.password = password
     

Base.metadata.create_all(engine)