import numpy as np
import os
import pickle
import mysql.connector

import json
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

def getEvenForEachNote(note,data):
    words= json.loads(note[3])
    rs = np.zeros(8)
    for word in words:
        entrys = getEntrysByWord(word,data)
        if len(entrys) != 0:
            entry = entrys[0]
            rs+=entry['vec'][:8]
    evenValue = rs/len(words)
    return evenValue


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

def by_single_word(word_list, length=10):
    rs_list = []
    if len(word_list) == 0:
        return []
    
    word = word_list[0]
    data = getDbData()
    notes = readNotes()

        
    for note in notes:
        even = getEvenForEachNote(note,data)
        entrys = getEntrysByWord(word,data)
        if len(entrys) != 0:
            entry = entrys[0]
            rs_list.append({'note': note,'distance': np.sum(np.square(entry['vec'][:8] - even))})

    
    rs_list = sorted(rs_list, key=lambda dic: dic['distance'])
    return rs_list[0:30]
    # for e in rs_list[0:30]:
    #     print(e['note'][2])
    #     print(e['distance'])
    # return 
    # for word in word_list:
    #     rs_list.append(byWord(word,length,data))
    # return rs_list
