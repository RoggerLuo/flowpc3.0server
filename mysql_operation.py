import time
from mysql.connector import connect

def select2(sql_cmd, param):
    try:
        cursor.execute(sql_cmd, param)
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))
    finally:
        cursor.close()
        conn.close()

def open():
    conn = connect(user='root', password='as56210', database='flowpc3.0', use_unicode=True)
    cursor = conn.cursor()
    return conn, cursor


def writeHistory(word):
    conn, cursor = connect2Mysql()
    cursor.execute('INSERT into search_history (word, timestamp) values (%s, %s)', [
                   word, time.time()])
    conn.commit()
    cursor.close()
    conn.close()


def readHistory():
    conn, cursor = connect2Mysql()
    cursor.execute(
        'SELECT * from search_history Order By timestamp Desc limit 300')
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return values


def readNotes():
    conn, cursor = connect2Mysql()
    cursor.execute(
        'SELECT * from flow_item where status = 0 Order By modify_time Desc')
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return values

def readDeletedNotes():
    conn, cursor = connect2Mysql()
    cursor.execute(
        'SELECT * from flow_item where status = 1 Order By modify_time Desc')
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return values


def readNotesById(item_id):
    conn, cursor = connect2Mysql()
    cursor.execute('SELECT * from flow_item where item_id = %s', (item_id,))
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return values


def deleteNote(item_id):
    conn, cursor = connect2Mysql()
    cursor.execute('SELECT * from flow_item where item_id = %s', (item_id,))
    values = cursor.fetchall()
    if len(values) != 0:  # find none
        cursor.execute(
            'UPDATE flow_item set status = 1 where item_id = %s', (item_id,))
        conn.commit()
    cursor.close()
    conn.close()


def touchNote(item_id, content, wordlist):
    conn, cursor = connect2Mysql()
    cursor.execute('SELECT * from flow_item where item_id = %s', (item_id,))
    values = cursor.fetchall()

    now = time.time()
    if len(values) == 0:  # find none
        cursor.execute('INSERT into flow_item (content, item_id, modify_time, wordlist) values (%s, %s, %s, %s)', [
                       content, item_id, now, wordlist])
        cursor.execute(
            'UPDATE temp set value = 1 where name = %s', ('has_new',))

    else:  # find one
        cursor.execute('UPDATE flow_item set content = %s, modify_time = %s, wordlist = %s where item_id = %s', [
                       content, now, wordlist, item_id])
    # insert_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()


def getHeaderText():
    conn, cursor = connect2Mysql()
    cursor.execute('SELECT * from temp where name = "headerText" ')
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return values[0]


def writeHeaderText(text):
    conn, cursor = connect2Mysql()
    cursor.execute(
        'UPDATE temp set str = %s where name = "headerText" ', [text, ])
    conn.commit()
    cursor.close()
    conn.close()
