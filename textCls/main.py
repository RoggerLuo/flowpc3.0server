import tensorflow as tf
import numpy as np
from model import getTrainingModel,getPredictionModel
from getLoss import getLoss
from embed import str2embed
from os.path import exists
import os
from tensorflow.contrib import layers
from random import choice
def optimizer(loss):    
    return layers.optimize_loss(
        loss, tf.train.get_global_step(),
        optimizer='Adam',
        learning_rate=0.001 #0.001
    )

def predict(categoryId,notes):
    embedingPlaceholder,y = getPredictionModel()
    def predict_feed_fn(string):
        x = str2embed(string)
        return {embedingPlaceholder:x}

    saver = tf.train.Saver()
    sess = tf.Session()
    sess.run(tf.global_variables_initializer()) # 每次不写就会报错

    name = 'category'+categoryId
    pathName = 'ckpt/' + name
    if exists(pathName):
        ckpt = tf.train.get_checkpoint_state(pathName)
        saver.restore(sess, ckpt.model_checkpoint_path)
        print('Restore from', ckpt.model_checkpoint_path)

    predictList = []
    for note in notes:
        string = note['content']
        _y = sess.run(y,feed_dict=predict_feed_fn(string))
        print(_y)
        if _y[0][1] > 0.75:
            predictList.append({'id':note['id']})
    return predictList    

def train(categoryId,yes,no,epoch):
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

    if exists('ckpt'):
        ckpt = tf.train.get_checkpoint_state('./ckpt')
        saver.restore(sess, ckpt.model_checkpoint_path)
        print('Restore from', ckpt.model_checkpoint_path)
    print('开始训练')
    for i in range(epoch):
        string = choice(no)['content']
        flag = False
        # print(flag)
        # print(string)
        loss,_ = sess.run([cross_entropy,train_op],feed_dict=feed_fn(string,flag)) # accuracy acc
        if i%100 == 0:
            print('epoch:' + str(i) + '----反向训练----')
            # print('----[acc]----')
            # print(acc)
            print('loss:',loss)
            print('----------------------------------------')
        


        string = choice(yes)['content']
        flag = True
        # print(flag)
        # print(string)
        loss,_ = sess.run([cross_entropy,train_op],feed_dict=feed_fn(string,flag)) # acc accuracy
        if i%100 == 0:
            print('epoch:' + str(i) + '----正向训练----')
            # print('----[acc]----')
            # print(acc)
            print('loss:',loss)
            print('----------------------------------------')

    # if i%100 == 0:
    name = 'category'+ str(categoryId)
    dirName = 'ckpt/' + name
    folder = os.path.exists(dirName)
    if not folder:
        os.makedirs(dirName)
    saver.save(sess, 'ckpt/' + name +'/model.ckpt')


# train()

# prediction()


# string = '先搞课程模块,登陆界面和状态栏以后再搞,杨老师那边先丢点东西过去'
# _y = sess.run(y,feed_dict=predict_feed_fn(string))
# print(_y)
# string = '每天的节点要搞清楚,自己的,公司的,特别是自己的,都是焦虑的来源'
# _y = sess.run(y,feed_dict=predict_feed_fn(string))
# print(_y)

# string = '不要把决策权给客户，解决问题的方向是:对用户有帮助的,对方说的不一定能解决问题自己判断，别照单全收，而是给出建议'
# _y = sess.run(y,feed_dict=predict_feed_fn(string))
# print(_y)


# string = '当外界不能按照主观意愿发展的时候，人就会产生一系列特殊的行为'
# _y = sess.run(y,feed_dict=predict_feed_fn(string))
# print(_y)

# string = '前端工程化,应用生命周期各个阶段，组件化强制规范,文件组织结构与框架。'
# _y = sess.run(y,feed_dict=predict_feed_fn(string))
# print(_y)