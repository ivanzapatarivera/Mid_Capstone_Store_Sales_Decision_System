from flask_wtf import FlaskForm
from wtforms import *


# Class to create Add Employee form
class AddEmployee(FlaskForm):

    emp_name = StringField('Name: ')
    pay_grade = StringField('Pay Grade: ')
    region = StringField('Region: ')
    emp_id = StringField('Employee ID: ')
    submit = SubmitField('Add')


# Class to create Add Product form
class AddProduct(FlaskForm):

    item_code = StringField('Item Code: ')
    item_name = StringField('Item Name: ')
    url = StringField('URL (optional): ')
    link = StringField('Name for Link (optional): ')
    manufacturer = StringField('Manufacturer (optional): ')
    submit = SubmitField('Add')

