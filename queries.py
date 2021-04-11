import pandas as pd
import sqlalchemy as sql
from config import db_uri
import matplotlib.pyplot as plt


# Creating engine to connect to db_uri on MySQL
engine = sql.create_engine(db_uri)

# Calling and reading local .xlsx files with data
filename = 'data.xlsx'


# Reading Excel file sheets
df_emp = pd.read_excel(filename, sheet_name = 'Employees')
df_product_sales = pd.read_excel(filename, sheet_name = 'Product Sales')


# Creating sales per region dataframe
df_joined_emp_product_sales = df_emp.merge(df_product_sales, how = 'left')
df_sales_region = df_joined_emp_product_sales[['Region', 'ITEM_CODE', 'Attribute', 'Value']]

print(df_sales_region.plot())
