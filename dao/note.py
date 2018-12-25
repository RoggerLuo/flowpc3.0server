from dbEngine import run
import numpy as np
import time
def create_note(content,category_id):
    if category_id == None:
        category_id = 0
    def callback(conn,cursor):
        now = time.time()
        cursor.execute('INSERT into note (content,category,modify_time) values (%s, %s, %s)', [content,category_id,now])
        insert_id = cursor.lastrowid # 一定要在conn.commit()之前，否则会返回0
        conn.commit()
        return {'insert_id':insert_id}
    return run(callback)

def modify_note(note_id,content):
    def callback(conn,cursor):
        now = time.time()
        cursor.execute('UPDATE note set content = %s, modify_time = %s where id = %s', [
            content, now, note_id])
        conn.commit()
        return 'success'
    return run(callback)

def delete_note(note_id):
    def callback(conn,cursor):
        cursor.execute('UPDATE note set status = 1 where id = %s', (note_id,))
        conn.commit()
        return 'success'
    return run(callback)







