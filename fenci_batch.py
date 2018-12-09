import time
import mysql.connector
import jieba
from string2word import String2word 
import json

def connect2Mysql():
    conn = mysql.connector.connect(
        user='root', password='as56210', database='flow4.0', use_unicode=True)
    cursor = conn.cursor()
    return conn, cursor


def readNotes():
    conn, cursor = connect2Mysql()
    cursor.execute(
        'SELECT * from flow_item Order By modify_time Desc') # where status = 0 
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return values

s2w = String2word()

def fenci(note):
    wordlist = s2w.segment(note[2]).filter()
    wordlistStr = json.dumps(wordlist,ensure_ascii=False)

    conn, cursor = connect2Mysql()
    cursor.execute('UPDATE flow_item set wordlist = %s where item_id = %s', [ wordlistStr, note[1] ])
    conn.commit()
    cursor.close()
    conn.close()
    print(note[1])

def do_batch():
    notes = readNotes() 
    for note in notes:
        fenci(note)

do_batch()

