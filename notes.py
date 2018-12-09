from _mysql import run
import numpy as np

def query_notes(categoryId=False,pageSize=10,pageNum=1):
    def callback(conn,cursor):
        cursor.execute(
            'SELECT * from notes where status = 0 Order By modify_time Desc limit %s,%s',
            ((pageNum-1)*pageSize,pageSize)
        )
        values = cursor.fetchall()
        return values
    return run(callback)
