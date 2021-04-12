# Importing required dependencies
from config import username, password, server, database, db_uri
import config
import os
from flask import Flask, redirect, render_template, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.dialects.mysql import *

# Importing forms
from forms import *

# Creating app variable and configurations
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

### MySQL DATABASE SECTION ###
import config

# Importing environmental variables using config.py
from config import username, password, server, database, db_uri

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
    price = Column(SMALLINT(10))

    def __init__(self, item_code, item_name, url, link, manufacturer, price):
        self.item_code = item_code
        self.item_name = item_name
        self.url = url
        self.link = link
        self.manufacturer = manufacturer
        self.price = price

    def __repr__(self):
        return f'{self.item_code} \n {self.item_name} \n {self.url} \n {self.link} \n {self.manufacturer} {self.price}'


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

    def __init__(self, item_code, attribute, value):
        self.item_code = item_code
        self.attribute = attribute
        self.value = value

    def __repr__(self):
        return f'{self.item_code} {self.attribute} {self.value}'


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

# Route to rendder add employee form
@app.route('/add_emp', methods = ['GET', 'POST'])
def add_emp():

    form = AddEmployee()

    if form.validate_on_submit():

        emp_name = form.emp_name.data
        pay_grade = form.pay_grade.data
        region = form.region.data
        emp_id = form.emp_id.data

        added_employee = Employees(emp_name, pay_grade, region, emp_id)
        db.session.add(added_employee)
        db.session.commit()

        return redirect(url_for('index'))

    pay_grade_list = Employees.query.all()
    region_list = ['NW', 'SW']
    return render_template('add_emp.html', form = form, pay_grade_list = pay_grade_list, region_list = region_list)


# Route to render add product form
@app.route('/add_prod', methods = ['GET', 'POST'])
def add_prod():

    form = AddProduct()

    if form.validate_on_submit():

        item_code = form.item_code.data
        item_name = form.item_name.data
        url = form.url.data
        link = form.link.data
        manufacturer = form.manufacturer.data  
        price = form.price.data

        added_product = ItemsOffered(item_code, item_name, url, link, manufacturer, price)
        db.session.add(added_product)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_prod.html', form = form)


# Route to render add product form
@app.route('/add_warr', methods = ['GET', 'POST'])
def add_warr():

    form = AddWarranty()

    if form.validate_on_submit():

        item_code = form.item_code.data
        item_name = form.item_name.data
        url = form.url.data
        link = form.link.data
        manufacturer = form.manufacturer.data
        price = form.price.data

        added_warranty = ItemsOffered(item_code, item_name, url, link, manufacturer, price)
        db.session.add(added_warranty)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_warr.html', form = form)


# Route to render product price change form
@app.route('/price_change', methods = ['GET', 'POST'])
def price_change():

    form = PriceChange()

    if form.validate_on_submit():

        item_code = form.item_code.data
        attribute = form.attribute.data.upper()
        value = form.value.data
        price_change = ProductPriceChange(item_code, attribute, value)
        db.session.add(price_change)
        db.session.commit()

        return redirect(url_for('index'))

    
    item_code_list = ItemsOffered.query.all()
    return render_template('price_change.html', form = form, items = item_code_list)


# Route to render sales form
@app.route('/sales', methods = ['GET', 'POST'])
def sales():

    form = PriceChange()

    if form.validate_on_submit():

        sale_id = form.sale_id.data
        index = form.index.data
        item_code = form.item_code.data
        emp_id = form.emp_id.data
        attribute = form.attribute.data
        year = form.year.data
        value = form.value.data

        price_change = ProductPriceChange(item_code, attribute, value)
        db.session.add(price_change)
        db.session.commit()

        return redirect(url_for('index'))

    item_code_list = ItemsOffered.query.all()
    emp_id_list = Employees.query.all()
    attribute_year = SalesPeriods.query.all()
    return render_template('price_change.html', form = form, items = item_code_list, emps = emp_id_list, attr = attribute_year)

if __name__ == "__main__":
    app.run(debug = True)