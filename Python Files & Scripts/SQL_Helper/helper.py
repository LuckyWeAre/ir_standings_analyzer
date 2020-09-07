import pymysql

class SQL_Helper:

    def __init__(self, host, user, password, database):

        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def open_connection(self):
        self.database = pymysql.connect(self.host, self.user, self.password, self.database, local_infile=1)
        if self.database is not None:
            return 0
        else:
            return 1

    def close_connection(self):
        self.database.close()
        return 0

    def get_column_headers(self, table_name):
        get_column_heads = self.database.cursor()
        get_column_heads.execute("DESC " + table_name)
        return get_column_heads.fetchall()

    def execute_query(self, query):
        execute_cursor = self.database.cursor()
        execute_cursor.execute(query)
        result = execute_cursor.fetchall()
        execute_cursor.close()
        return result

    def get_commands_from_script(self, file_path):
        sql_script_file = open(file_path, 'r')
        sql_script_contents = sql_script_file.read()
        sql_script_file.close()
        sql_script_contents.replace('\n', '')
        sql_script_contents.replace('\\', '')
        sql_commands = sql_script_contents.split(';')
        return sql_commands
