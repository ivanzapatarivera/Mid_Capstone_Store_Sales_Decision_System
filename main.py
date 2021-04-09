# Importing required dependencies
import os
from flask import Flask, redirect, render_template, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *


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

print(db)