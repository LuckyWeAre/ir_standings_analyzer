# Imports
from ir_webstats_rc_09012020 import constants as cts
from ir_webstats_rc_09012020.client import iRWebStats
from ir_webstats_rc_09012020.util import clean
import private_constants as priv_cts
from SQL_Helper.helper import SQL_Helper

email = priv_cts.EMAIL
pswd = priv_cts.IRACING_PASSWORD

iracing = iRWebStats()
iracing.login(email, pswd)
if not iracing.logged:
    print("INVALID CREDENTIALS")
    exit()
"""
url1 = 'https://members.iracing.com/memberstats/member/GetSeasonStandings?format=csv&seasonid=2721&carclassid=71' \
       '&clubid=-1&raceweek=-1&division=-1&start=1&end=25&sort=points&order=desc'
resp = iracing.download_csv(url1)
rtp_all_file = open('/home/eric/Desktop/00_Current.csv', 'w')
wrtr = rtp_all_file.write(resp)
rtp_all_file.close()"""
"""
resp2 = iracing.get_output_csv(2721, 71)
print(resp2)

resp3 = iracing.get_output_csv(2721, 71, race_week=1)
print(resp3)"""

# Main
"""Get CSV files from iRacing stats page for RTP series and write them to respective files"""
"""
resp_race_00 = iracing.get_output_csv(2721, 71)
resp_race_01 = iracing.get_output_csv(2721, 71, race_week=1)
resp_race_02 = iracing.get_output_csv(2721, 71, race_week=2)
resp_race_03 = iracing.get_output_csv(2721, 71, race_week=3)
resp_race_04 = iracing.get_output_csv(2721, 71, race_week=4)
resp_race_05 = iracing.get_output_csv(2721, 71, race_week=5)
resp_race_06 = iracing.get_output_csv(2721, 71, race_week=6)
resp_race_07 = iracing.get_output_csv(2721, 71, race_week=7)
resp_race_08 = iracing.get_output_csv(2721, 71, race_week=8)
resp_race_09 = iracing.get_output_csv(2721, 71, race_week=9)
resp_race_10 = iracing.get_output_csv(2721, 71, race_week=10)
resp_race_11 = iracing.get_output_csv(2721, 71, race_week=11)
resp_race_12 = iracing.get_output_csv(2721, 71, race_week=12)
resp_race_13 = iracing.get_output_csv(2721, 71, race_week=13)
resp_race_14 = iracing.get_output_csv(2721, 71, race_week=14)"""

file_names = ['00_Current.csv', '01_Daytona.csv', '02_Rockingham.csv', '03_Homestead.csv', '04_Atlanta.csv',
              '05_CharlotteRoval.csv', '06_Michigan.csv', '07_Richmond.csv', '08_Darlington.csv', '09_Dover.csv',
              '10_LasVegas.csv', '11_CanadianTire.csv', '12_Texas.csv', '13_Martinsville.csv', '14_Phoenix.csv']

num_races = 14
for i in range(num_races + 1):
    if i == 0:
        output_resp = iracing.get_output_csv(2721, 71)
    else:
        output_resp = iracing.get_output_csv(2721, 71, race_week=i)

    rtp_file = open('/home/eric/PycharmProjects/ir_standings_analyzer/Generated CSVs/' + file_names[i], 'w')
    rtp_file.write(output_resp)
    rtp_file.close()


sql = SQL_Helper(priv_cts.HOST, priv_cts.USER, priv_cts.SQL_PASSWORD, 'RTP')
db = sql.open_connection()

# heads = sql.get_column_headers(db, '00_Current')
# print(heads)
query_result = sql.execute_query(db, 'source /home/eric/PycharmProjects/ir_standings_analyzer/SQL Files & Scripts/script.sql')
print(query_result)

sql.close_connection(db)
