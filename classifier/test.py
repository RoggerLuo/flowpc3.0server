import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
sys.path.append(os.path.join(os.path.dirname(__file__),'../textCls'))
from dbEngine import run_middleware
import numpy as np
import time
from textCls.main import train,predict
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

def categorize_note():
    notes = get_categorized_notes()
    categorized_notes = {}
    for note in notes:
        cate = note['category']
        if categorized_notes.get(cate,None) == None:
            categorized_notes[cate] = [note]
        else:
            categorized_notes[cate].append(note)
    return categorized_notes

def getTrainingData(train_each_category):
    categorized_notes = categorize_note()
    categories = list(categorize_note().keys())
    for cate_yes in categories:
        yes = categorized_notes[cate_yes]
        no = []
        for cate_no in categories: # no
            if cate_no != cate_yes:
                for note in categorized_notes[cate_no]:
                    no.append(note)
        print('cate_yes',cate_yes)
        train_each_category(cate_yes,yes,no)

# def save(categoryId,idList):

def train_each_category(categoryId,yes,no):
    # print(len(yes))
    # print(len(no))
    # print('categoryId',categoryId)
    if len(yes) < 4:
        print(len(yes))
        return
    epoch = len(yes)*10#0
    train(categoryId,yes,no,epoch)
    notes = get_uncategorized_notes()
    predictNotesIdList = predict(categoryId,notes)
    print(predictNotesIdList)
    # save(categoryId,predictNotesIdList)
    # 根据yes和no，打乱他们的顺序，随机训练 100*len(yes) 次
    # 每次训练一个yes,一个no

    # 保存到以category+id命名的文件夹
    # 读取也用category id, 使用之前训练过的model参数

    # 对未分类文章进行分类

    # 加入打印训练各个阶段的时间
getTrainingData(train_each_category)



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


