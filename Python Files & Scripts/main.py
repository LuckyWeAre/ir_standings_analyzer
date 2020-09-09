# Imports
from ir_webstats_rc_09012020 import constants as cts
from ir_webstats_rc_09012020.client import iRWebStats
from ir_webstats_rc_09012020.util import clean
import private_constants as priv_cts
from SQL_Helper.helper import SQL_Helper

# Main
"""Get CSV files from iRacing stats page for RTP series and write them to respective files"""

# logging into iRacing site using Rob Crouch's fork of ir_webstats
email = priv_cts.EMAIL
pswd = priv_cts.IRACING_PASSWORD

iracing = iRWebStats()
iracing.login(email, pswd)
if not iracing.logged:
    print("INVALID CREDENTIALS")
    exit()

# Specifying names of files for the CSVs downloaded
file_names = ['00_Current', '01_Daytona', '02_Rockingham', '03_Homestead', '04_Atlanta',
              '05_CharlotteRoval', '06_Michigan', '07_Richmond', '08_Darlington', '09_Dover',
              '10_LasVegas', '11_CanadianTire', '12_Texas', '13_Martinsville', '14_Phoenix']

# Pulling all CSV files for the given series (Road To Pro 2020 is id=2721) by looping through iRacing site requests
#   after each site is grabbed, writing the returned CSV file to its respective name from the list
num_races = 14
for i in range(num_races + 1):
    if i == 0:
        output_resp = iracing.get_output_csv(2721, 71)
    else:
        output_resp = iracing.get_output_csv(2721, 71, race_week=i)

    rtp_file = open('/home/eric/PycharmProjects/ir_standings_analyzer/Generated CSVs/' + file_names[i] + '.csv', 'w')
    rtp_file.write(output_resp)
    rtp_file.close()

# Logging into local SQL database for storage of data for later analytics use
sql = SQL_Helper(priv_cts.HOST, priv_cts.USER, priv_cts.SQL_PASSWORD, 'RTP')
sql.open_connection()

print('starting table deletion')  # Debug
commands = sql.get_commands_from_script(
    '/home/eric/PycharmProjects/ir_standings_analyzer/SQL Files & Scripts/table_deletion.sql')
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

print('completed table deletion, starting table creation')  # Debug
commands = sql.get_commands_from_script(
    '/home/eric/PycharmProjects/ir_standings_analyzer/SQL Files & Scripts/table_creation.sql')
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
commands = sql.get_commands_from_script(
    '/home/eric/PycharmProjects/ir_standings_analyzer/SQL Files & Scripts/table_dataloading.sql')
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

sql.execute_query('commit')

result = sql.execute_query('SELECT CustomerID, Name FROM 00_Current ORDER BY Points DESC;')
print(result)

ids = []
names = []
for i in range(len(result)):
    ids.append(result[i][0])

print(ids)

for i in range(len(result)):
    names.append(result[i][1])

print(names)

pts_by_id = {}
for id in ids:
    pts_by_id[id] = []
    for index, name in enumerate(file_names):
        if index != 0:
            # get points for that id from that event file
            result = sql.execute_query('SELECT Points FROM ' + name + ' WHERE CustomerID=' + str(id) + ';')
            # if there are no points, it's 0, otherwise the points from that event
            if result:
                pts_by_id.setdefault(id, []).append(result[0][0])
            else:
                pts_by_id.setdefault(id, []).append(0)
    # break  # breaking after first id for debug purposes

print(pts_by_id)

# Close DB connection at end of program
sql.close_connection()
