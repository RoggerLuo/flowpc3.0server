import mysql.connector
import json

def run(callback):
    conn = mysql.connector.connect(user='root', password='as56210', database='flowpc3.0', use_unicode=True)
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

