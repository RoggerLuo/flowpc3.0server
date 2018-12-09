from mysql.connector import connect

def run(callback):
    conn = connect(user='root', password='as56210', database='flowpc3.0', use_unicode=True)
    cursor = conn.cursor()
    try:
        return callback(conn, cursor)
    except mysql.connector.Error as e:
        print('mysql operation fails!{}'.format(e))
    finally:
        cursor.close()
        conn.close()

