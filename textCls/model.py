import tensorflow as tf
import numpy as np
from attentionEncode import getArticleRepresentation

def getW(name,shape=[200,200], stddev=0.1, mean=0):
    initial = tf.truncated_normal(shape=shape, mean=mean, stddev=stddev)
    with tf.variable_scope('mlp', reuse=tf.AUTO_REUSE):
        return tf.get_variable(name,initializer=initial)

def getB(name,shape=[200], value=0.1):
    initial = tf.constant(value=value, shape=shape)
    with tf.variable_scope('mlp', reuse=tf.AUTO_REUSE):
        return tf.get_variable(name,initializer=initial)


def multilayer_perceptron(x, keep_prob): # 在不go down gradient，keep_prob带来了每次sess.run的唯一的不确定性，
    xLen = 256
    x = tf.reshape(x,[1,xLen])
    layer_1 = tf.add(tf.matmul(x, getW('w1',[xLen,xLen])), getB('b1',[xLen]))
    layer_1 = tf.nn.relu(layer_1)
    layer_1 = tf.nn.dropout(layer_1, keep_prob)
    out_layer = tf.matmul(layer_1, getW('w2',[xLen,2])) + getB('b2',[2])
    # Tensor("add:0", shape=(1, 2), dtype=float32)
    return out_layer

def getPredictionModel():
    embedingPlaceholder = tf.placeholder(tf.float32, shape=[None, 200], name='embeding')
    rep = getArticleRepresentation(embedingPlaceholder)
    y = multilayer_perceptron(rep,1)
    soft_y = tf.nn.softmax(y)
    return [embedingPlaceholder,soft_y]

def getTrainingModel():
    embedingPlaceholder = tf.placeholder(tf.float32, shape=[None, 200], name='embeding')
    rep = getArticleRepresentation(embedingPlaceholder)
    y = multilayer_perceptron(rep,0.8)
    return [embedingPlaceholder,y]
