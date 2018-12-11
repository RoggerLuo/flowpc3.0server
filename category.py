from _mysql import run
import numpy as np
def query_categories(categoryId,pageSize,pageNum):
    if pageNum == None:
        pageNum = 1
    if pageSize == None:
        pageSize = 10
    if categoryId == None:
        categoryId = False
    pageNum = int(pageNum)
    pageSize = int(pageSize)
    def callback(conn,cursor):
        cursor.execute(
            "SELECT * from note where status = 0 Order By modify_time Desc limit %s,%s",
            [(pageNum-1)*pageSize,pageSize]
        )
        return cursor.fetchall()
    return run(callback)
