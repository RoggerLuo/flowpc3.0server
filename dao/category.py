from dbEngine import run
import numpy as np
import json
def colorChange(category_id,color):
    def callback(conn,cursor):
        cursor.execute('UPDATE category set color = %s where id = %s', [color, category_id])
        conn.commit()
        return 'success'
    return run(callback)

def orderChange(category_id,order):
    def callback(conn,cursor):
        cursor.execute('UPDATE category set order_number = %s where id = %s', [order, category_id])
        conn.commit()
        return 'success'
    return run(callback)

def query_categories():
    def callback(conn,cursor):
        cursor.execute("select * from category order by order_number desc")
        values = cursor.fetchall()
        columes = ['id','name','prediction','order_number','color']
        return [dict(zip(columes,value)) for value in values]
    return run(callback)

def create_category(name):
    def callback(conn,cursor):
        cursor.execute('INSERT into category (name) values (%s)', [name])
        insert_id = cursor.lastrowid # 一定要在conn.commit()之前，否则会返回0
        conn.commit()
        return {'insert_id':insert_id}
    return run(callback)

def modify_category(category_id,name):
    def callback(conn,cursor):
        cursor.execute('UPDATE category set name = %s where id = %s', [
            name, category_id])
        conn.commit()
        return 'success'
    return run(callback)

def delete_category(category_id):
    def callback(conn,cursor):
        cursor.execute('delete from category where id = %s', (category_id,))
        conn.commit()
        return 'success'
    return run(callback)

def savePrediction(category_id,noteIds):
    def callback(conn,cursor):
        cursor.execute('UPDATE category set prediction = %s where id = %s', [
            json.dumps(noteIds), category_id])
        conn.commit()
        return 'success'
    return run(callback)