import tensorflow as tf
from model import getTrainingModel,getPredictionModel
from getLoss import getLoss
from embed import str2embed
from os.path import exists
import os
from tensorflow.contrib import layers
from random import choice
import random
import jieba
import sys
sys.path.append('..')
from dao.ignoreList import get_ignore_list
ignore_list = get_ignore_list()

def optimizer(loss):    
    # with tf.variable_scope('attention', reuse=tf.AUTO_REUSE):
    return layers.optimize_loss(
        loss, tf.train.get_global_step(),
        optimizer='Adam',
        learning_rate=0.001 #0.001
    )

def predict(categoryId,notes):
    tf.reset_default_graph()
    embedingPlaceholder,y = getPredictionModel()
    def predict_feed_fn(string):
        x = str2embed(string)
        return {embedingPlaceholder:x}

    saver = tf.train.Saver()
    sess = tf.Session()
    sess.run(tf.global_variables_initializer()) # 每次不写就会报错

    ckptDirName = 'category' + str(categoryId)
    subCkptDirPath = os.path.join(os.path.dirname(__file__),'ckpt',ckptDirName) # 'ckpt/' + ckptDirName 

    # name = 'category'+categoryId
    # pathName = 'ckpt/' + name
    if exists(subCkptDirPath):
        ckpt = tf.train.get_checkpoint_state(subCkptDirPath)
        saver.restore(sess, ckpt.model_checkpoint_path)
        print('Restore from', ckpt.model_checkpoint_path)
    else:
        return []
    predictList = []
    for note in notes:
        try:
            content = note['content']
            # 分词 + 过滤
            word_list = jieba.lcut_for_search(content)
            word_list = list(filter(lambda x:x not in ignore_list,word_list))
            content = ' '.join(word_list)

            _y = sess.run(y,feed_dict=predict_feed_fn(content))
            print(_y)
            if _y[0][1] > 0.75:
                predictList.append({'id':note['id'],'score':_y[0][1]})
            # predictList.append({'id':note['id'],'score':_y[0][1]})
        except Exception as e:
            print(e)

    predictList = sorted(predictList, key=lambda x: -x['score'])
    predictList = list(map(lambda x:x['id'],predictList))
    return predictList    

def train(categoryId,yes,no,epoch,negSample_times=5):
    tf.reset_default_graph() # 运行两次就报错，第一次读取ckpt参数没事，第二次就有事了
    embedingPlaceholder,y = getTrainingModel()
    y_labelPlaceholder,cross_entropy,accuracy = getLoss(y)
    train_op = optimizer(cross_entropy)
    def feed_fn(string,flag):
        label = [0]
        if flag == True:
            label = [1]
        x = str2embed(string)
        return {embedingPlaceholder:x,y_labelPlaceholder:label}

    saver = tf.train.Saver()
    sess = tf.Session()
    sess.run(tf.global_variables_initializer()) # 每次不写就会报错

    ckptDirName = 'category' + str(categoryId)
    subCkptDirPath = os.path.join(os.path.dirname(__file__),'ckpt',ckptDirName) # 'ckpt/' + ckptDirName 

    if exists(subCkptDirPath):
        ckpt = tf.train.get_checkpoint_state(subCkptDirPath)
        saver.restore(sess, ckpt.model_checkpoint_path)
        print('Restore from', ckpt.model_checkpoint_path)

    for i in range(epoch):
        random.shuffle(no)
        random.shuffle(yes)
        for idx in range(len(yes)):
            
            content = no[idx]['content']
            # 分词 + 过滤
            word_list = jieba.lcut_for_search(content)
            word_list = list(filter(lambda x:x not in ignore_list,word_list))
            content = ' '.join(word_list)
            if content == '':
                continue
            flag = False
            loss,_ = sess.run([cross_entropy,train_op],feed_dict=feed_fn(content,flag)) # accuracy acc
            if i%100 == 0:
                print('epoch:' + str(i) + '----neg train----')
                print('loss:',loss)
                print('----------------------------------------')


            content = yes[idx]['content']
            # 分词 + 过滤
            word_list = jieba.lcut_for_search(content)
            word_list = list(filter(lambda x:x not in ignore_list,word_list))
            content = ' '.join(word_list)
            if content == '':
                continue
            flag = True
            loss,_ = sess.run([cross_entropy,train_op],feed_dict=feed_fn(content,flag)) # accuracy acc
            if i%100 == 0:
                print('epoch:' + str(i) + '----pos train----')
                print('loss:',loss)
                print('----------------------------------------')

        

    folder = os.path.exists(subCkptDirPath)
    if not folder:
        os.makedirs(subCkptDirPath)
    
    saver.save(sess, os.path.join(subCkptDirPath,'model.ckpt')) # 'ckpt/' + ckptDirName +'/model.ckpt'
    print('save ckpt success')

