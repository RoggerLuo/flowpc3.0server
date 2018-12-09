import numpy as np
import os
import pickle
import mysql.connector
import json

def connect2Mysql():
    conn = mysql.connector.connect(
        user='root', password='as56210', database='flow4.0', use_unicode=True)
    cursor = conn.cursor()
    return conn, cursor


def readNotes():
    conn, cursor = connect2Mysql()
    cursor.execute(
        'SELECT * from flow_item where id = 6348 Order By modify_time Desc')
    values = cursor.fetchall()

    cursor.close()
    conn.close()
    return values

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



note = readNotes()
data = getDbData()
def forEachNote(note):
    words= json.loads(note[3])
    rs = np.zeros(8)
    for word in words:
        entrys = getEntrysByWord(word,data)
        if len(entrys) != 0:
            entry = entrys[0]
            rs+=entry['vec'][:8]
    evenValue = rs/len(words)
    return evenValue
    # arr = []
    # for word in words:
    #     entrys = getEntrysByWord(word,data)
    #     if len(entrys) != 0:
    #         entry = entrys[0]
    #         arr.append({'word':word,'sum':np.sum(np.square(entry['vec'][:8] - evenValue))})
    # arr = sorted(arr, key=lambda dic: dic['sum'])
    # for e in arr:
    #     print(e['word'])

forEachNote(note[0])

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
        # print('没找到')
        return []
    else:
        entry = entrys[0]
        sortedList = sortByDeviation(entry, data)
    return sortedList[0:length]

def by_word_list(word_list, length=10):
    rs_list = []
    for word in word_list:
        rs_list.append(byWord(word,length))
    return rs_list


