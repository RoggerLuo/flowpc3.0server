import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'textCls'))
import numpy as np
import time
from textCls.main import train,predict
from dao.notes import get_categorized_notes,get_uncategorized_notes
from dao.category import savePrediction
def categorize_notes():
    notes = get_categorized_notes()
    categorized_notes = {}
    for note in notes:
        cate = note['category']
        if categorized_notes.get(cate,None) == None:
            categorized_notes[cate] = [note]
        else:
            categorized_notes[cate].append(note)
    return categorized_notes

def getTrainingData(train_each_category):
    categorized_notes = categorize_notes()
    categories = list(categorize_notes().keys())
    for cate_yes in categories:
        yes = categorized_notes[cate_yes]
        no = []
        for cate_no in categories: # no
            if cate_no != cate_yes:
                for note in categorized_notes[cate_no]:
                    no.append(note)
        print('cate_yes',cate_yes)
        train_each_category(cate_yes,yes,no)


def train_each_category(categoryId,yes,no):
    if len(yes) < 4:
        print(len(yes))
        return
    epoch = len(yes)*10 #0
    train(categoryId,yes,no,epoch)
    notes = get_uncategorized_notes()
    predictNotesIdList = predict(categoryId,notes)
    savePrediction(categoryId,predictNotesIdList)
    print(predictNotesIdList)
    print(time.time)
    # 加入打印训练各个阶段的时间
getTrainingData(train_each_category)


