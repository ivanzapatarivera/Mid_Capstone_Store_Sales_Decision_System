# Importing required dependencies
from config import username, password, server, database, db_uri
import config
import os
from flask import Flask, redirect, render_template, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.dialects.mysql import *


# Creating app variable and configurations
app = Flask(__name__)
app.config['SECRET KEY'] = 'mysecretkey'


app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Defining db
db = SQLAlchemy(app)
Migrate(app, db)


class Employees(db.Model):

    __tablename__ = 'employees'

    emp_name = Column(VARCHAR(64), nullable=False)
    pay_grade = Column(VARCHAR(3), nullable=False)
    region = Column(VARCHAR(2), nullable=False)
    emp_id = Column(VARCHAR(7), nullable=False, primary_key=True)

    def __init__(self, emp_name, pay_grade, region, emp_id):
        self.emp_name = emp_name
        self.pay_grade = pay_grade
        self.region = region
        self.emp_id = emp_id

    def __repr__(self):
        return f'{self.emp_name} \n {self.pay_grade} \n {self.region} \n {self.emp_id} \n'


class ItemsOffered(db.Model):

    __tablename__ = 'items_offered'

    item_code = Column(VARCHAR(8), nullable=False, primary_key=True)
    item_name = Column(VARCHAR(40), nullable=False)
    url = Column(Text, nullable=True)
    link = Column(Text, nullable=True)
    manufacturer = Column(VARCHAR(40), nullable=True)

    def __init__(self, item_code, item_name, url, link, manufacturer):
        self.item_code = item_code
        self.item_name = item_name
        self.url = url
        self.link = link
        self.manufacturer = manufacturer

    def __repr__(self):
        return f'{self.item_code} \n {self.item_name} \n {self.url} \n {self.link} \n {self.manufacturer}'


class SalesPeriods(db.Model):

    __tablename__ = 'sales_periods'

    date = Column(DATE, nullable=False)
    attribute = Column(VARCHAR(3), nullable=False, primary_key=True)
    sales_period = Column(TINYINT(2), nullable=False)
    sales_year = Column(SMALLINT(4), nullable=False, primary_key=True)
    quarter = Column(TINYINT(1), nullable = False)

    __table_args__ = (
        PrimaryKeyConstraint('attribute', 'sales_year'),
        {},
    )


    def __init__(self, date, attribute, sales_period, sales_year):
        self.date = date
        self.attribute = attribute
        self.sales_period = sales_period
        self.sales_year = sales_year

    def __repr__(self):
        return f'{self.date} {self.attribute} {self.sales_period} {self.sales_year}'


class ProductSales(db.Model):

    __tablename__ = 'product_sales'

    sale_id = Column(INTEGER(display_width=10), nullable=False, primary_key=True)
    index = Column(INTEGER(display_width=10), nullable=False)
    item_code = Column(VARCHAR(10), ForeignKey(
        ItemsOffered.item_code, onupdate='CASCADE'))
    emp_id = Column(VARCHAR(6), ForeignKey(
        Employees.emp_id, onupdate='CASCADE'))
    attribute = Column(VARCHAR(6))
    year = Column(SMALLINT(4))
    value = Column(INTEGER(display_width=10), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            [attribute, year],
            [SalesPeriods.attribute, SalesPeriods.sales_year],
            onupdate="CASCADE", ondelete='Set Null'
        ),
    )

    def __init__(self, index, item_code, emp_id, attribute, year, value):
        self.index = index
        self.item_code = item_code
        self.emp_id = emp_id
        self.attribute = attribute
        self.year = year
        self.value = value

    def __repr__(self):
        return f"{self.index} \n{self.item_code} \n{self.emp_id} \n{self.attribute} \n {self.year} \n{self.value}"


class ProductPriceChange(db.Model):

    __tablename__ = 'product_price_change'

    price_id = Column(INTEGER, primary_key=True, autoincrement=True)
    item_code = Column(VARCHAR(10), ForeignKey(
        ItemsOffered.item_code, onupdate='CASCADE'), nullable=False)
    attribute = Column(VARCHAR(6), nullable=False)
    value = Column(INTEGER(display_width=10), nullable=False)

    def __init__(self, price_id, item_code, attribute, value):
        self.price_id = price_id
        self.item_code = item_code
        self.attribute = attribute
        self.value = value

    def __repr__(self):
        return f'{self.price_id} {self.item_code} {self.attribute} {self.value}'


# Validating if sql string will throw a try/except error
# If it throws an error, .create_all() method will execute
sql = 'SELECT * FROM employees; SELECT * FROM items_offered; SELECT * FROM product_price_change; SELECT * FROM product_sales; SELECT * FROM sales_periods;'
engine = create_engine(db_uri)
session = db.session()

try: 
    cursor = session.execute(sql).cursor
    if(cursor):
        print('CONNECTED')
       
except:
    print(f'Table does not exist and string {sql} was not executed.')
    print(f'*** CREATING TABLE ***')
    db.create_all()
    print(f'*** TABLE CREATED ***')
db.create_all()


##############################################
###############    ROUTES    #################
##############################################

# Home Page
@app.route('/')
def index():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug = True)