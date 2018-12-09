import jieba
import numpy as np
import mysql.connector


def connect2Mysql():
    conn = mysql.connector.connect(
        user='root', password='as56210', database='flow4.0', use_unicode=True)
    cursor = conn.cursor()
    return conn, cursor

def getIgnores():
    conn, cursor = connect2Mysql()
    cursor.execute('SELECT * from ignore_list')
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return [v[1] for v in values]


def readNotes():
    conn, cursor = connect2Mysql()
    cursor.execute('SELECT * from flow_item')
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return values

class Sentence(object):

    def __init__(self,string):
        self.word_list = []
        self.string = string

    def segment(self):
        self.word_list = jieba.lcut(self.string)  # 默认是精确模式
        return self

    def filter(self):
        ignored_list = getIgnores()
        filtered_list = []
        for word in self.word_list:
            if word not in ignored_list:
                filtered_list.append(word)
        self.word_list = filtered_list
        return self


def touchWord(word):
    conn, cursor = connect2Mysql()
    cursor.execute('SELECT * from wordlist where word = %s', (word,))
    values = cursor.fetchall()

    
    if len(values) == 0:  # find none
        cursor.execute('INSERT into wordlist (word, count) values (%s, %s)', [word, 1])

    else:  # find one
        entry = values[0]
        cursor.execute('UPDATE wordlist set  count = %s where word = %s', [entry[2]+1, word])
    # insert_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()



notes = readNotes()    

length = len(notes)
    
for i in range(length):
    content = notes[i][2]
    if len(content) > 10:
        # print('[第%d轮]' % x)
        print('    当前第%d段,一共%d段:' % (i, length))
        trimmedContent = content.strip()
        # print(trimmedContent[:20])
        

        for word in Sentence(trimmedContent).segment().filter().word_list:
            touchWord(word)
            print(word)




