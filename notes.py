from dbEngine import run
import numpy as np
def query_notes(categoryId,pageSize,pageNum):
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
        values = cursor.fetchall()
        columes = ['id','content','category','create_time','modify_time','status']
        return [dict(zip(columes,value)) for value in values]
    return run(callback)
