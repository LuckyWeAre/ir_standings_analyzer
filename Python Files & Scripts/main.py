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

# Main
"""Get CSV files from iRacing stats page for RTP series and write them to respective files"""

file_names = ['00_Current.csv', '01_Daytona.csv', '02_Rockingham.csv', '03_Homestead.csv', '04_Atlanta.csv',
              '05_CharlotteRoval.csv', '06_Michigan.csv', '07_Richmond.csv', '08_Darlington.csv', '09_Dover.csv',
              '10_LasVegas.csv', '11_CanadianTire.csv', '12_Texas.csv', '13_Martinsville.csv', '14_Phoenix.csv']
"""
num_races = 14
for i in range(num_races + 1):
    if i == 0:
        output_resp = iracing.get_output_csv(2721, 71)
    else:
        output_resp = iracing.get_output_csv(2721, 71, race_week=i)

    rtp_file = open('/home/eric/PycharmProjects/ir_standings_analyzer/Generated CSVs/' + file_names[i], 'w')
    rtp_file.write(output_resp)
    rtp_file.close()"""


sql = SQL_Helper(priv_cts.HOST, priv_cts.USER, priv_cts.SQL_PASSWORD, 'RTP')
sql.open_connection()

print('starting table deletion')
commands = sql.get_commands_from_script('/home/eric/PycharmProjects/ir_standings_analyzer/SQL Files & Scripts/table_deletion.sql')
# print(commands)
for command in commands:
    try:
        if command.strip() != '':
            query_result = sql.execute_query(command)
            if query_result:
                print('printing')
                print(query_result)
    except IOError as msg:
        print('Command Skipped:  ', msg)

print('completed table deletion, starting table creation')
commands = sql.get_commands_from_script('/home/eric/PycharmProjects/ir_standings_analyzer/SQL Files & Scripts/table_creation.sql')
# print(commands)
for command in commands:
    try:
        if command.strip() != '':
            query_result = sql.execute_query(command)
            if query_result:
                print('printing')
                print(query_result)
    except IOError as msg:
        print('Command Skipped:  ', msg)

print('completed table creation, starting table data loading')
commands = sql.get_commands_from_script('/home/eric/PycharmProjects/ir_standings_analyzer/SQL Files & Scripts/table_dataloading.sql')
# print(commands)
for command in commands:
    try:
        if command.strip() != '':
            query_result = sql.execute_query(command)
            if query_result:
                print('printing')
                print(query_result)
    except IOError as msg:
        print('Command Skipped:  ', msg)

#query_result = sql.execute_query(db, query1)
#print(query_result)

sql.close_connection()
