import tensorflow as tf
import numpy as np

CE = tf.nn.sparse_softmax_cross_entropy_with_logits
def getLoss(y):
    y_label = tf.placeholder(tf.int32, shape=[None], name='y_label')

    y_predict = tf.cast(tf.argmax(y, axis=1), tf.int32)

    correct_prediction = tf.equal(y_predict, y_label)
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    
    # Loss
    cross_entropy = tf.reduce_mean(CE(labels=y_label,logits=tf.cast(y, tf.float32)))
    
    return y_label,cross_entropy,accuracy
