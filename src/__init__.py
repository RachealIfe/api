from flask import Flask, jsonify, request

import psycopg2
from .config import config

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    def connect():
        conn =None
        try:
            params = config()

            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)

            cur=conn.cursor()
            print('PostgreSQL database version: ')
            cur.execute('SELECT version()')

            db_version=cur.fetchone()
            print(db_version)
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

    @app.post("/add/user")
    def add_user():
        sql="""INSERT INTO users(name, email) VALUES(%s,%s) RETURNING id"""
        conn = None 
        user_id = None
        if request.method=='POST':
            name=request.form['name']
            email=request.form['email']
            try:
                params=config()
                conn=psycopg2.connect(**params)
                cur=conn.cursor()
                cur.execute(sql, (name, email))
                user_id=cur.fetchone()
                conn.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
        return {"success":"User added successfully"}

    @app.post("/delete/user/<int:user_id>")
    def delete_user(user_id):
        sql="""DELETE FROM users WHERE id=%s"""
        conn=None
        updated_rows=None
        try:
            params=config()
            conn=psycopg2.connect(**params)
            cur=conn.cursor()
            cur.execute(sql,[user_id])
            conn.commit()
            cur.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return {"success":"User deleted"}

    @app.get("/all/users")
    def all_users():
        sql="""SELECT * FROM users"""
        conn=None
        updated_rows=None
        try:
            params=config()
            conn=psycopg2.connect(**params)
            cur=conn.cursor()
            cur.execute(sql)
            updated_rows=cur.fetchall()
            print(updated_rows)
            conn.commit()
            cur.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return jsonify(updated_rows)


    """if __name__ == '__main__':
        #connect()
        #insert_user("Special", "special@mail.com")
        #update_user(2,"Special", "special@mail.com")
        #delete_user(2)
        #all_users()
        app.run()"""
    return app
    """@app.get('/users')
    def users():
        users = all_users()
        return jsonify([user.to_json() for user in users])

    @app.post('/create/user')
    def create_user():
        return {'user':'created'}

    @app.get('/all/blogs')
    def all_blogs():
        pass 

    @app.get('/all/users')
    def all_users():
        pass"""