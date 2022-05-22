import pyodbc 

#database details
server = 'localhost' 
database = 'INNO'

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + server + '; DATABASE=' + database + '; Trusted_Connection=yes;')

cursor = cnxn.cursor()
cursor.execute('SELECT DISTINCT Tag FROM Responses')
row = cursor.fetchall()

tags = []

for i in row:
    data = i[0]
    tags.append(data)

print(tags)