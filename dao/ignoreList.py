from dbEngine import run,run_middleware
def get_ignore_list():
    def callback(conn,cursor):
        cursor.execute("select * from ignore_list")
        values = cursor.fetchall()
        values = list(map(lambda x:x[1],values))
        return values
    return run_middleware(callback)
