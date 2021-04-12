import pandas as pd
import sqlalchemy as sql
from config import db_uri


# Creating engine to connect to db_uri on MySQL
engine = sql.create_engine(db_uri)

# Importing and reading local .xlsx file with data from each sheet
filename = 'data.xlsx'
employees = pd.read_excel(filename, sheet_name = 'Employees')
items_offered = pd.read_excel(filename, sheet_name = 'Items Offered')
product_sales = pd.read_excel(filename, sheet_name = 'Product Sales')
sales_periods = pd.read_excel(filename, sheet_name = 'Sales Periods')
product_price_change = pd.read_excel(filename, sheet_name = 'Product Price Change')


# Establishing dataframes
df_emp = pd.DataFrame(employees)
df_items_offered = pd.DataFrame(items_offered)
df_product_price_change = pd.DataFrame(product_price_change)
df_sales_period = pd.DataFrame(sales_periods)
df_product_sales = pd.DataFrame(product_sales)


# Exporting employee dataframes to MySQL
db_cols_emp = ['emp_name', 'pay_grade', 'region', 'emp_id']
df_emp.rename(columns= dict(zip(df_emp.columns, db_cols_emp))).to_sql(con = engine, name='employees', if_exists='append', index=False, index_label=None)
print(df_emp)

# Exporting items offered dataframes to MySQL
db_cols_items = ['item_code', 'item_name', 'url', 'link', 'manufacturer', 'price']
df_items_offered.rename(columns= dict(zip(df_items_offered.columns, db_cols_items))).to_sql(con = engine, name='items_offered', if_exists='append', index=False, index_label=None)
print(df_items_offered)

# Exporting product price changes dataframes to MySQL
db_cols_product_price_change = ['price_id', 'item_code', 'attribute', 'value']
df_product_price_change.rename(columns= dict(zip(df_product_price_change.columns, db_cols_product_price_change))).to_sql(con = engine, name='product_price_change', if_exists='append', index=False, index_label=None)
print(df_product_price_change)

# Exporting sales periods dataframes to MySQL
db_cols_sales_period = ['date', 'attribute', 'sales_period', 'sales_year']
df_sales_period.rename(columns= dict(zip(df_sales_period.columns, db_cols_sales_period))).to_sql(con = engine, name='sales_periods', if_exists='append', index=False, index_label=None)
print(df_sales_period)

# Exporting product sales dataframes to MySQL
db_cols_product_sales = ['sale_id', 'index', 'item_code', 'emp_id', 'attribute', 'year', 'value']
df_product_sales.rename(columns= dict(zip(df_product_sales.columns, db_cols_product_sales))).to_sql(con = engine, name='product_sales', if_exists='append', index=False, index_label=None)
print(df_product_sales)