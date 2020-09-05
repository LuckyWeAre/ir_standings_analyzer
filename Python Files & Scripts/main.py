# Imports
import pymysql
from ir_webstats_rc_09012020 import constants as cts
from ir_webstats_rc_09012020.client import iRWebStats
from ir_webstats_rc_09012020.util import clean
import private_constants as priv_cts
from SQL_Helper.helper import SQL_Helper

# Helpers

"""def openConnection():
    myDB = pymysql.connect(host="localhost", user="root", passwd="Tpwifsql", db="RTP")
    return myDB

def getColumnHeaders(connection, tableName):
    getCH = connection.cursor()
    getCH.execute("DESC " + tableName)
    return getCH.fetchall()"""

"""dbConnection = openConnection()

columnHeaders = getColumnHeaders(dbConnection, "0_ALL")
for column in columnHeaders:
    print(column[0], end=' ')
print()

testCursor = dbConnection.cursor()

testCursor.execute("SELECT * FROM 0_ALL where name='Eric Wineland'")

result = testCursor.fetchall()

for row in result:
    for x in row:
        print(x, end=' ')

print()"""

email = priv_cts.EMAIL
pswd = priv_cts.IRACING_PASSWORD

iracing = iRWebStats()
iracing.login(email, pswd)
if not iracing.logged:
    print("INVALID CREDENTIALS")
    exit()

url1 = 'https://members.iracing.com/memberstats/member/GetSeasonStandings?format=csv&seasonid=2721&carclassid=71' \
       '&clubid=-1&raceweek=-1&division=-1&start=1&end=25&sort=points&order=desc'
resp = iracing.download_csv(url1)
rtp_all_file = open('/home/eric/Desktop/00_Current.csv', 'w')
wrtr = rtp_all_file.write(resp)
rtp_all_file.close()

resp2 = iracing.get_output_csv(2721, 71)
print(resp2)

sql = SQL_Helper(priv_cts.HOST, priv_cts.USER, priv_cts.SQL_PASSWORD, 'RTP')
db = sql.open_connection()

heads = sql.get_column_headers(db, '00_Current')
print(heads)

sql.close_connection(db)
