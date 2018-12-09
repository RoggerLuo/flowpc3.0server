from config import Config
import mysql.connector
from task import Task
import os
import json
import time

c = Config()
t = Task(c)


def connect2Mysql():
    conn = mysql.connector.connect(
        user='root', password='as56210', database='flow4.0', use_unicode=True)
    cursor = conn.cursor()
    return conn, cursor


def readNotes():
    conn, cursor = connect2Mysql()
    cursor.execute(
        'SELECT * from flow_item where status = 0 Order By modify_time Desc')
    values = cursor.fetchall()

    cursor.execute('UPDATE temp set value = 0 where name = %s', ('has_new',))
    conn.commit()

    cursor.close()
    conn.close()
    return values


# def readDeletedNotes():
#     conn, cursor = connect2Mysql()
#     cursor.execute(
#         'SELECT * from flow_item where status = 1 Order By modify_time Desc')
#     values = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return values


def ifNewNoteComing():
    conn, cursor = connect2Mysql()
    cursor.execute('SELECT * from temp where name = %s', ('has_new',))
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return values[0][2]

lastCost = 1
for x in range(20000):
    startTime = time.time()
    notes = readNotes()
    # deletedNote = readDeletedNotes()

    notes_counts = len(notes)
    cost = 0
    for i in range(notes_counts):
        if ifNewNoteComing() == 1:
            break
        wordlist = json.loads(notes[i][3])
        cost += t.feedlist(wordlist) / 1000
    t.save()

    # if x % 4 == 0:
    #     for j in range(len(deletedNote)):
    #         wordlist = json.loads(deletedNote[j][3])
    #         t.feedlist(wordlist)

    print('[第%d轮,耗时%f分],cost:%f' % (x, (startTime - time.time()) / 60, cost))
    # if abs(cost - lastCost) / lastCost <= 0.02:
    #     c.rateChange(0.01)
    #     print('rate change 0.01')
    # else:
    #     c.rateChange(0.05)
    #     print('rate change 0.05')
    # lastCost = cost

    # print('[第%d轮]' % x)
    # print('    当前第%d篇,一共%d篇:' % (i, notes_counts))
