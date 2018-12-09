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


