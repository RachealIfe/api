import psycopg2

db='apidb'
host='127.0.0.1'
user='superuser'
password='superuser'
conn = psycopg2.connect(database=db, user=user, password=password, host=host, port="5555")
cursor = conn.cursor()

cursor.execute('SELECT COUNT(MemberID) as count FROM Menber Where id = 1')
row = cursor.fetchone()

comm.close()

print(row)