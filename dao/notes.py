from dbEngine import run,run_middleware
import numpy as np
import time
import json
def get_uncategorized_notes():
    def callback(conn,cursor):
        hours = 24
        timeRange = time.time() - 60*60*hours
        # cursor.execute("select * from note where category!=0 and status=0 and modify_time > %s",[timeRange])
        cursor.execute("select * from note where category=0 and status=0")
        values = cursor.fetchall()
        columns = ['id','content','category','create_time','modify_time','status']
        return [dict(zip(columns,value)) for value in values]
    return run_middleware(callback)

def get_categorized_notes():
    def callback(conn,cursor):
        hours = 24
        timeRange = time.time() - 60*60*hours
        # cursor.execute("select * from note where category!=0 and status=0 and modify_time > %s",[timeRange])
        cursor.execute("select * from note where category!=0 and status=0")
        values = cursor.fetchall()
        columns = ['id','content','category','create_time','modify_time','status']
        return [dict(zip(columns,value)) for value in values]
    return run_middleware(callback)



def query_notes(categoryId,pageSize,pageNum):
    if pageNum == None:
        pageNum = 1
    if pageSize == None:
        pageSize = 10
    if categoryId == None:
        categoryId = 'all'

    pageNum = int(pageNum)
    pageSize = int(pageSize)
    def callback(conn,cursor):
        notes = []
        if categoryId == 'all' or categoryId == '0':
            if categoryId == '0':
                cursor.execute(
                    "SELECT * from note where category=%s and status=0 Order By modify_time Desc limit %s,%s",
                    [categoryId,(pageNum-1)*pageSize,pageSize]
                )
            else:
                cursor.execute(
                    "SELECT * from note where status=0 Order By modify_time Desc limit %s,%s",
                    [(pageNum-1)*pageSize,pageSize]
                )
            notes = cursor.fetchall()
        else:

            cursor.execute("SELECT * from category where id = %s",[categoryId])
            values = cursor.fetchall()
            prediction = values[0][2]
            predictionList = json.loads(prediction)

            cursor.execute("SELECT * from note where status=0")
            values = cursor.fetchall()
            predictionNotes = list(filter(lambda x:x[0] in predictionList,values))

            cursor.execute(
                "SELECT * from note where category=%s and status=0 Order By modify_time Desc limit %s,%s",
                [categoryId,(pageNum-1)*pageSize,pageSize]
            )
            hardCateNotes = cursor.fetchall()
            # 把硬分类的文章加上去, 并去重
            for hNote in hardCateNotes:
                if hNote[0] not in predictionList:
                    predictionNotes.append(hNote)
            # 判断predictionNotes中是否有 硬分类不属于这个分类的 剔除
            filterdNotes = list(filter(lambda x:x[2]==0 or x[2]==categoryId,predictionNotes))
            # 加上分页
            notes = filterdNotes[(pageNum-1)*pageSize:pageNum*pageSize]

        # values = cursor.fetchall()
        columes = ['id','content','category','create_time','modify_time','status']
        return [dict(zip(columes,note)) for note in notes]
    return run(callback)
