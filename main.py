# Importing required dependencies
import os
from flask import Flask, redirect, render_template, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.dialects.mysql import *


# Creating app variable and configurations
app = Flask(__name__)
app.config['SECRET KEY'] = 'mysecretkey'

import config
from config import username, password, server, database, db_uri

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Defining db
db = SQLAlchemy(app)
Migrate(app, db)


class ProductSales(db.Model):

    __tablename__ = 'product_sales'

    sale_id = Column(Integer(display_width = 10), nullable = False)
    index = Column(Integer(display_width = 10), nullable = False)
    item_code = 


db.create_all()