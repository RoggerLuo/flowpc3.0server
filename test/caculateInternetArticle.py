import os
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


path_name = './result'
for item in os.listdir(path_name):
    full_path = os.path.abspath(os.path.join(path_name, item))
    file_opened = open(full_path)
    lines = file_opened.readlines()        
    length = len(lines)
    for i in range(length):
        print('    文件%s:当前第%d段,一共%d段:' %(item,i,length))
        trimmedContent = lines[i].strip()
        if len(trimmedContent) > 20:
            print (trimmedContent[:10])

            for word in Sentence(trimmedContent).segment().filter().word_list:
                touchWord(word)
                print(word)
        else: 
            print('    console:当前line太短了,跳过')



