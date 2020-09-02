# Imports
import pymysql


# Helpers
def open_connection():
    my_database = pymysql.connect(host="localhost", user="root", passwd="Tpwifsql", db="RTP")
    return my_database


def get_column_headers(connection, table_name):
    get_column_heads = connection.cursor()
    get_column_heads.execute("DESC " + table_name)
    return get_column_heads.fetchall()


# Main

dbConnection = open_connection()

columnHeaders = get_column_headers(dbConnection, "00_Current")
for column in columnHeaders:
    print(column[0], end=' ')
print()

testCursor = dbConnection.cursor()

testCursor.execute("SELECT * FROM 00_Current where name='Eric Wineland'")

result = testCursor.fetchall()

for row in result:
    for x in row:
        print(x, end=' ')

print()
