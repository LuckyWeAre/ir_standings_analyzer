import pymysql

class SQL_Helper:

    def __init__(self, host, user, password, database):

        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def open_connection(self):
        db = pymysql.connect(self.host, self.user, self.password, self.database)
        return db

    def close_connection(self, database):
        database.close()
        return 0

    def get_column_headers(self, database, table_name):
        get_column_heads = database.cursor()
        get_column_heads.execute("DESC " + table_name)
        return get_column_heads.fetchall()

    def execute_query(self, database, query):
        execute_cursor = database.cursor()
        execute_cursor.execute(query)
        result = execute_cursor.fetchall()
        execute_cursor.close()
        return result
