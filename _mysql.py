import mysql.connector
import json

def run(callback):
    conn = mysql.connector.connect(user='root', password='as56210', database='flowpc3.0', use_unicode=True)
    cursor = conn.cursor()
    try:
        values = callback(conn, cursor)
        return json.dumps(values)
         
    except mysql.connector.Error as e:
        print('mysql operation fails!{}'.format(e))
    finally:
        cursor.close()
        conn.close()

