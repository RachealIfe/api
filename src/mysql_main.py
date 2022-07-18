import pypyodbc
from flask import Flask

server="localhost"
user="root"
password=""
db="apidb"
port=3306
conn =pypyodbc.connect(driver='{SQL Server}', server=server, uid=user, pwd=password, database=db)
cursor = conn.cursor()
"""
cursor.execute("SELECT * as count FROM users")
row = cursor.fetchall()
"""

@app.get('/user/<id>')
def user(id):
    conn=pymssql.connect("SELECT * FROM users WHERE id = %d", id)
    row=cursor.fetchone()
    return {'name': row['name']}

conn.close

print(row)

app=Flask(__name__)