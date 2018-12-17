import mysql.connector
import jieba
import numpy as np


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


def get_high_frequency_list():
    conn, cursor = connect2Mysql()
    cursor.execute('SELECT * from high_frequency_list')
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return [v[1] for v in values]


class String2word(object):

    def __init__(self):
        self.jieba = jieba
        self.word_list = []
        self.ignored_list = getIgnores()
        self.high_frequency_list = get_high_frequency_list()

    def segment(self,string):
        self.word_list = self.jieba.lcut(string)  # 默认是精确模式
        return self

    def filter(self):
        filtered_list = []
        for word in self.word_list:
            if word not in self.ignored_list:
                if word not in self.high_frequency_list:
                    filtered_list.append(word)

        self.word_list = filtered_list
        return filtered_list
