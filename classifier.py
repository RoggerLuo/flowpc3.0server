import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'textCls'))
# import numpy as np
import time
import json
from textCls.main import train,predict
from dao.sysState import isTraining,startTrain,endTrain
from dao.notes import get_categorized_notes,get_uncategorized_notes,checkIfNeedTrain,mark_training_notes
from dao.note import get_note,id2note
from dao.category import savePrediction,get_category
from corpus.corpusApi import getRandomNegSamples
import jieba
from dbEngine import run,run_middleware
from dao.ignoreList import get_ignore_list

minimum_threshold = 3 # 开始训练某个category的所需文章的最小数量
how_many_epoch_each_note = 3
predict_period_in_sec = 5*60
newCategorizedNotesNum_for_startTrain = 10
commonNegNotes = getRandomNegSamples()

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
    # commonNegNotes = getRandomNegSamples()
    newCategorizedNotes = __categorize_notes(newCategorizedNotes)
    categories = list(newCategorizedNotes.keys())

    notes_catd = __categorize_notes(get_categorized_notes())
    allCategories = list(notes_catd.keys())
    for cate_yes in categories:
        yes = notes_catd[cate_yes]
        no = []
        for cate_no in allCategories:
            if cate_no != cate_yes:
                for note in notes_catd[cate_no]:
                    no.append(note)
        print('current category id:',cate_yes)
        # string = choice(no)['content']
        # no = no + commonNegNotes
        train_each_category(cate_yes,yes,no)

def train_each_category(categoryId,yes,no):
    if len(yes) < minimum_threshold: # 开始训练某个category的所需文章的最小数量
        print('note num for category:',categoryId,'too small,skip')
        return
    epoch = len(yes)*how_many_epoch_each_note
    train(categoryId,yes,no,epoch,negSample_times=1)
    print('category training end for categoryId:',categoryId)
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    mark_training_notes(yes)

    notes = get_uncategorized_notes(60*60*24*30*12*2)
    predictNotesIdList = predict(categoryId,notes)
    savePrediction(categoryId,predictNotesIdList,'replace')

def predict_uncategorized_notes(sec): # 新写的notes
    notes = get_uncategorized_notes(sec)
    if len(notes) > 0:
        for cate in get_category():
            print('---start predict category:',cate[0])
            categoryId = cate[0]
            predictNotesIdList = predict(categoryId,notes)
            savePrediction(categoryId,predictNotesIdList,'append')
            print('--- predict end ---')

        print('predict results save finished')
    else:
        print('too less notes to predict')

def main2():
    print('start runing')
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    newCategorizedNotes = checkIfNeedTrain()
    if  len(newCategorizedNotes) > newCategorizedNotesNum_for_startTrain:
        main(newCategorizedNotes,train_each_category)
    else:
        print('training standard is not reached')

def similarAlg(noteId):
    content = get_note(noteId) # get note content dynamic
    
    selected_note_word_list = jieba.lcut_for_search(content)
    ignore_list = get_ignore_list()
    selected_note_word_list = list(filter(lambda x:x not in ignore_list,selected_note_word_list))
        
    notes = get_categorized_notes() + get_uncategorized_notes(60*60*24*300)
    returnList = []
    for note in notes:
        count = 0
        current_word_list = jieba.lcut_for_search(note['content'])
        match_list = []
        for word in current_word_list:
            if word in selected_note_word_list:  # 如果和当前文章有相同的词，则记录
                if word not in match_list: # 去重
                    count += 1
                    match_list.append(word)
        if count > 0 :
            note['count'] = count
            note['match_list'] = match_list
            returnList.append(note)
    
    returnList = sorted(returnList, key=lambda x: -len(x['match_list']))
    return json.dumps(returnList) 

if __name__ == "__main__":
    if isTraining() == False:
        print('start training')
        startTrain()
        main2()
        predict_uncategorized_notes(predict_period_in_sec)
        endTrain()
        print('end training')
    else:
        print('it is training now, action drop')

