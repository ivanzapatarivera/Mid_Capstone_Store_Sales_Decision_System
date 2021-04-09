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


class SalesTeamLeads(db.Model):

    __tablename__ = 'sales_team_leads'

    name = db.Column(db.Text, nullable = False)
    paygrade = db.Column(db.VARCHAR(3), nullable = False)
    region = db.Column(db.VARCHAR(2), nullable = False)
    final_emp_no = db.Column(db.VARCHAR(6), nullable = False)

    def __init__(self, name, paygrade, region, final_emp_no):
        self.name = name
        self.paygrade = paygrade
        self.region = region
        self.final_emp_no = final_emp_no

    def __repr__(self):
        return f"Employee name: {name} \nEmployee Number: {final_emp_no} \nSales Region: {region} \nPay Grade: {paygrade}"