from dbEngine import run,run_middleware
import numpy as np
import time

def startTrain():
    def callback(conn,cursor):
        cursor.execute('UPDATE sys_state set status = %s where name = %s', ['ing','train'])
        conn.commit()
    return run_middleware(callback)

def endTrain():
    def callback(conn,cursor):
        cursor.execute('UPDATE sys_state set status = %s where name = %s', ['no','train'])
        conn.commit()
    return run_middleware(callback)

def isTraining():
    def callback(conn,cursor):
        cursor.execute("select * from sys_state where name='train' ")
        values = cursor.fetchall()
        return values[0][2] == 'ing'
    return run_middleware(callback)

