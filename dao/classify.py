from dbEngine import run
# import numpy as np
import time
def classify(note_id,cate_id):
    def callback(conn,cursor):
        now = time.time()
        cursor.execute('UPDATE note set category = %s, create_time = %s where id = %s', [cate_id,now,note_id])
        conn.commit()
        return 'success'
    return run(callback)

def unclassify(note_id):
    def callback(conn,cursor):
        now = time.time()
        cursor.execute('UPDATE note set category = %s, modify_time = %s where id = %s', [0,now,note_id])
        conn.commit()
        return 'success'
    return run(callback)






