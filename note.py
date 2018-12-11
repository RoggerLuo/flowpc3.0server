from _mysql import run
import numpy as np
import time
def create_note(content):
    def callback(conn,cursor):
        now = time.time()
        cursor.execute('INSERT into note (content, modify_time) values (%s, %s)', [content, now])
        insert_id = conn.insert_id() # 一定要在conn.commit()之前，否则会返回0
        return insert_id
    return run(callback)


