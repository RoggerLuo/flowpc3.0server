import numpy as np
import os
import pickle

db_path = os.path.dirname(os.path.realpath(__file__)) + '/w2v.pkl'


def getEntrysByWord(word, data):
    return list(filter(lambda e: e['word'] == word, data))


class WordsCompress(object):

    def __init__(self):
        self.data = self.getDbData()

    def feedWordlist(self, wordlist):
        wordlist = self.uniq(wordlist)
        entrylist = self.wordlist2entrylist(wordlist)
        combinedlist = self.combine2list(entrylist)
        return list(map(lambda x: x['word'],combinedlist))
        # sortedList = sorted(combinationList, key=lambda dic: dic['devi'])
        # interception = sortedList[:10]
        # return self.getBackWordlist(interception)

    def getBackWordlist(self, interception):
        wordlist = []
        for item in interception:
            wordlist.append(item['entry1'])
            wordlist.append(item['entry2'])
        wordlist = self.uniq(wordlist)
        return wordlist

    def wordlist2entrylist(self, wordlist):
        entrylist = []
        for word in wordlist:
            entrys = getEntrysByWord(word, self.data)
            if len(entrys) != 0:
                entrylist.append(entrys[0])
        return entrylist

    def uniq(self, wordlist):
        uniqList = []
        for word in wordlist:
            if word not in uniqList:
                uniqList.append(word)
        return uniqList

    def combine2list(self, entrylist):
        combinationList = [entrylist[0]]
        for i in range(len(entrylist)):  # len = 3, i = 1
            entry = entrylist[i]
            flag = True
            for item in combinationList:
                if self.calcDevi(entry, item) < 12:
                    flag = False
            if flag == True:
                combinationList.append(entry)


            # for j in range(len(entrylist) - i - 1):  # len = 1, j = 0
            #     _entry = entrylist[i + j + 1]  # i+j+1 = 2
            #     combinationList.append({'entry1': entry['word'], 'entry2': _entry[
            #                            'word'], 'devi': self.calcDevi(entry, _entry)})
        return combinationList

    def getDbData(self):
        data = []
        if os.path.exists(db_path):
            with open(db_path, 'rb') as f:
                data = pickle.load(f)
        else:
            data = []
        return data

    def calcDevi(self, entry, _entry):
        deviationVec = entry['vec'][:8] - _entry['vec'][:8]
        deviationVec = np.square(deviationVec)
        return np.sum(deviationVec)


# f = WordsCompress()
# r=f.feedWordlist(["按照", "编辑", "时间", "一天", "版本", "删除", "增加", "版本", "删除", "训练", "改成", "版本","16", "位", "vector", "搜索", "搜", "几个", "词"])
# print(r)