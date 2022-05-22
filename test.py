import pyodbc
import pandas as pd

#database details
server = 'localhost' 
database = 'INNO'

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + server + '; DATABASE=' + database + '; Trusted_Connection=yes;')
cursor = cnxn.cursor()
data = pd.read_sql('SELECT DISTINCT Tag FROM Responses', cnxn)
x = pd.read_sql_query('SELECT DISTINCT Tag FROM Responses', cnxn)
del cnxn
print(x)
