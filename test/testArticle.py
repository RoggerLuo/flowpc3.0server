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
    cursor.execute('SELECT * from flow_item order by modify_time DESC')
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return values


def getCountDDD(word):
    conn, cursor = connect2Mysql()
    cursor.execute('SELECT * from ddd where word = %s',[word])
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(values) == 0:
        return 0
    else:
        return values[0][2]

def getCount(word):
    conn, cursor = connect2Mysql()
    cursor.execute('SELECT * from wordlist where word = %s',[word])
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(values) == 0:
        return 0
    else:
        return values[0][2]



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

import numpy as np
import os
import pickle


db_path = os.path.dirname(os.path.realpath(__file__))+'/w2v.pkl'
def getDbData():
    data = []
    if os.path.exists(db_path):
        with open(db_path, 'rb') as f:
            data = pickle.load(f)
    else:
        data = []
    return data


def getEntrysByWord(word, data):
    return list(filter(lambda e: e['word'] == word, data))


def sortByDeviation(entry, data):
    unsortedList = []
    for et in data:
        deviationArr = entry['vec'][:8] - et['vec'][:8]
        # deviationArr = np.fabs(deviationArr)
        deviationArr = [round(de, 5) for de in deviationArr.tolist()]
        deviationArr = np.square(np.array(deviationArr))
        # deviationArr = np.array(deviationArr)
        deviation = np.sum(deviationArr)
        unsortedList.append({'deviation': deviation, 'word': et['word']})

    sortedList = sorted(unsortedList, key=lambda dic: dic['deviation'])
    return sortedList


def byWord(word, length=10):
    data = getDbData()
    entrys = getEntrysByWord(word, data)
    if len(entrys) == 0:
        print('没找到')
        return 0
    else:
        entry = entrys[0]
        x = entry['vec'][:8]
        return x#sum([ i*i for i in x])



values = readNotes()
for entry in values[0:30]:
    print('------------------------')
    print('------------------------')
    print(entry[2])
    evenVec = np.zeros(8)
    count = 0
    ls = []
    for item in Sentence(entry[2]).segment().filter().word_list:
        if getCountDDD(item)<375:
            if getCount(item)<10:
                ls.append(item)
                evenVec += byWord(item)
                count += 1
                #print(evenVec)
                #print(count)
    even = evenVec/count
    ls2 =[]
    for item in ls:
        vec = byWord(item)
        deviationArr = vec - even
        ssum = sum([ i*i for i in deviationArr])
        ls2.append({'word':item,'sum':ssum})

    sortedList = sorted(ls2, key=lambda item: item['sum'])
    print('---')
    for item in sortedList[:10]:
        print(item['word'])    
    #print(evenVec/count)
    #print('---')
    #print(string)
        #print(getCount(item))
        #print('--')

