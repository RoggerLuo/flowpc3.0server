import mysql.connector
import json

outerConfig = {'host':'rorrc.3322.org','port':'6033','user':'root', 'password':'!@as56210', 'database':'flowpc3.0', 'use_unicode':True}
synology = {'host':'172.17.0.1','port':'6033','user':'root', 'password':'!@as56210', 'database':'flowpc3.0', 'use_unicode':True}
intraConfig = {'host':'192.168.1.4','port':'6033','user':'root', 'password':'!@as56210', 'database':'flowpc3.0', 'use_unicode':True}

def run(callback):
    conn = mysql.connector.connect(**synology)
    # conn = mysql.connector.connect(**intraConfig)
    # conn = mysql.connector.connect(**outerConfig)

    cursor = conn.cursor()
    try:
        values = callback(conn, cursor)
        obj = {'data':values,'hasErrors':False}
        return json.dumps(obj)
         
    except mysql.connector.Error as e:
        message = 'mysql operation fails!{}'.format(e)
        print(message)
        obj = {'message':message,'hasErrors':True}
        return json.dumps(obj)

    except BaseException as e:
        message = 'error!{}'.format(e)
        print(message)
        obj = {'message':message,'hasErrors':True}
        return json.dumps(obj)
    finally:
        cursor.close()
        conn.close()

def run_middleware(callback):
    conn = mysql.connector.connect(**synology)
    # conn = mysql.connector.connect(**intraConfig)
    # conn = mysql.connector.connect(**outerConfig)

    cursor = conn.cursor()
    try:
        return callback(conn, cursor)
    except mysql.connector.Error as e:
        message = 'mysql operation fails!{}'.format(e)
        print(message)
        obj = {'message':message,'hasErrors':True}
        return obj
    except BaseException as e:
        message = 'error!{}'.format(e)
        print(message)
        obj = {'message':message,'hasErrors':True}
        return obj
    finally:
        cursor.close()
        conn.close()

