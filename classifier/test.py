import sys
sys.path.append('..')
from dbEngine import run
import numpy as np
import time

def get_allNotes():
    def callback(conn,cursor):
        hours = 24
        timeRange = time.time() - 60*60*hours
        cursor.execute("select * from note where modify_time > %s",[timeRange])
        values = cursor.fetchall()
        columns = ['id','content','category','create_time','modify_time','status']
        return [dict(zip(columns,value)) for value in values]
    return run(callback)

classified_notes = {}
classified_notes.get()
for note in notes:

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


