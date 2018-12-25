import sys
import os
# sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
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
    categories = list(categorize_note().keys())
    for cate_yes in categories:
        yes = categorized_notes[cate_yes]
        no = []
        for cate_no in categories: # no
            if cate_no != cate_yes:
                for note in categorized_notes[cate_no]:
                    no.append(note)
        print('cate_yes',cate_yes)
        train_each_category(cate_yes,yes,no)

#  savePrediction(categoryId,idList):

def train_each_category(categoryId,yes,no):
    if len(yes) < 4:
        print(len(yes))
        return
    epoch = len(yes)*10#0
    train(categoryId,yes,no,epoch)
    notes = get_uncategorized_notes()
    predictNotesIdList = predict(categoryId,notes)

    print(predictNotesIdList)
    # save(categoryId,predictNotesIdList)
    # 根据yes和no，打乱他们的顺序，随机训练 100*len(yes) 次
    # 每次训练一个yes,一个no

    # 保存到以category+id命名的文件夹
    # 读取也用category id, 使用之前训练过的model参数

    # 对未分类文章进行分类

    # 加入打印训练各个阶段的时间
getTrainingData(train_each_category)


