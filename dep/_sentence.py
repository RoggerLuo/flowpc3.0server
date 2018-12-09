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
