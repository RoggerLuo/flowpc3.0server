import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'textCls'))
# import numpy as np
import time
from textCls.main import train,predict
from dao.notes import get_categorized_notes,get_uncategorized_notes,checkIfNeedTrain
from dao.category import savePrediction
minimum_threshold = 10 # 开始训练某个category的所需文章的最小数量
how_many_epoch_each_note =  20
def __categorize_notes(notes):
    categorized_notes = {}
    for note in notes:
        cate = note['category']
        if categorized_notes.get(cate,None) == None:
            categorized_notes[cate] = [note]
        else:
            categorized_notes[cate].append(note)
    return categorized_notes

def main(newCategorizedNotes,train_each_category):
    newCategorizedNotes = __categorize_notes(newCategorizedNotes)
    categories = list(newCategorizedNotes.keys())

    notes = __categorize_notes(get_categorized_notes())
    allCategories = list(notes.keys())
    for cate_yes in categories:
        yes = notes[cate_yes]
        no = []
        for cate_no in allCategories:
            if cate_no != cate_yes:
                for note in notes[cate_no]:
                    no.append(note)
        print('cate_yes',cate_yes)
        train_each_category(cate_yes,yes,no)

def train_each_category(categoryId,yes,no):
    if len(yes) < minimum_threshold:
   # 开始训练某个category的所需文章的最小数量      print(len(yes))
        return
    epoch = len(yes)*how_many_epoch_each_note
    train(categoryId,yes,no,epoch)
    notes = get_uncategorized_notes()
    predictNotesIdList = predict(categoryId,notes)
    savePrediction(categoryId,predictNotesIdList)
    print(predictNotesIdList)
    print(time.time())
    # 加入打印训练各个阶段的时间

newCategorizedNotes = checkIfNeedTrain(1)
if  len(newCategorizedNotes) > 20:
    main(newCategorizedNotes,train_each_category)
else:
    print('training standard is not reached')
