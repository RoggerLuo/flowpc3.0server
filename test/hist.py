import jieba
import numpy as np
import mysql.connector


def connect2Mysql():
    conn = mysql.connector.connect(
        user='root', password='as56210', database='flow4.0', use_unicode=True)
    cursor = conn.cursor()
    return conn, cursor

def getIgnores():
    conn, cursor = connect2Mysql()
    cursor.execute('SELECT * from ignore_list')
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return [v[1] for v in values]


def readWords():
    conn, cursor = connect2Mysql()
    cursor.execute('SELECT * from wordlist order by count DESC')
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return values

words = readWords()
y=[]
for item in words:
    y.append(item[2])

import matplotlib.pyplot as plt
plt.figure(figsize=(12, 8))
plt.plot(y) 
plt.show()


