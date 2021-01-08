# Imports
from ir_webstats_rc_09012020 import constants as cts
from ir_webstats_rc_09012020.client import iRWebStats
from ir_webstats_rc_09012020.util import clean
import private_constants as priv_cts
from SQL_Helper.helper import SQL_Helper

# Main
"""Get CSV files from iRacing stats page for RTP series and write them to respective files"""

# Setting log in information for iRacing website
email = priv_cts.EMAIL
pswd = priv_cts.IRACING_PASSWORD

# logging into iRacing site using Rob Crouch's fork of ir_webstats
iracing = iRWebStats()
iracing.login(email, pswd)
if not iracing.logged:
    print("INVALID CREDENTIALS")
    exit()

# Specifying names of files for the CSVs downloaded
old_file_names = ['00_Current', '01_Daytona', '02_Rockingham', '03_Homestead', '04_Atlanta',
              '05_CharlotteRoval', '06_Michigan', '07_Richmond', '08_Darlington', '09_Dover',
              '10_LasVegas', '11_CanadianTire', '12_Texas', '13_Martinsville', '14_Phoenix']

file_names = ['01_Daytona', '02_Rockingham', '03_Homestead', '04_Atlanta',
              '05_CharlotteRoval', '06_Michigan', '07_Richmond', '08_Darlington', '09_Dover',
              '10_LasVegas', '11_CanadianTire', '12_Texas', '13_Martinsville', '14_Phoenix']

# Pulling all CSV files for the given series (Road To Pro 2020 is id=2721) by looping through iRacing site requests
#   after each site is grabbed, writing the returned CSV file to its respective name from the list
num_races = 14
for i in range(1, num_races + 1):
    print(i)
    if i == 0:
        output_resp = iracing.get_output_csv(2721, 71)
    else:
        output_resp = iracing.get_output_csv(2721, 71, race_week=i)

    rtp_file = open('/home/eric/PycharmProjects/ir_standings_analyzer/Generated CSVs/' + file_names[i - 1] + '.csv', 'w')
    rtp_file.write(output_resp)
    rtp_file.close()

# Logging into local SQL database for storage of data for later analytics use
sql = SQL_Helper(priv_cts.HOST, priv_cts.USER, priv_cts.SQL_PASSWORD, 'RTP')
sql.open_connection()

# Deleting previous tables in Database to start with freshly loaded tables (will update to use already created tables
#   in a later iteration of this code)
print('starting table deletion')  # Debug
# Pulling sql commands from .sql file
commands = sql.get_commands_from_script(
    '/home/eric/PycharmProjects/ir_standings_analyzer/SQL Files & Scripts/table_deletion.sql')
# print(commands)
# Looping through to execute each command from the file
for command in commands:
    try:
        if command.strip() != '':
            query_result = sql.execute_query(command)
            if query_result:
                print('printing')
                print(query_result)
    except IOError as msg:
        print('Command Skipped:  ', msg)

# Creating new tables for use in the DB to hold and manipulate data (will be updated in a later iteration to utilize
#   existing tables rather than creating new ones)
print('completed table deletion, starting table creation')  # Debug
# Pulling sql commands from .sql file
commands = sql.get_commands_from_script(
    '/home/eric/PycharmProjects/ir_standings_analyzer/SQL Files & Scripts/table_creation.sql')
# print(commands)
# Looping through to execute each command from the file
for command in commands:
    try:
        if command.strip() != '':
            query_result = sql.execute_query(command)
            if query_result:
                print('printing')
                print(query_result)
    except IOError as msg:
        print('Command Skipped:  ', msg)

# Loading data into the newly created tables
print('completed table creation, starting table data loading')  # Debug
# Pulling sql commands from .sql file
commands = sql.get_commands_from_script(
    '/home/eric/PycharmProjects/ir_standings_analyzer/SQL Files & Scripts/table_dataloading.sql')
# print(commands)
# Looping through to execute each command from the file
for command in commands:
    try:
        if command.strip() != '':
            query_result = sql.execute_query(command)
            if query_result:
                print('printing')
                print(query_result)
    except IOError as msg:
        print('Command Skipped:  ', msg)

# Committing the executed queries to the Database after successful completion of queries
sql.execute_query('commit')

# Getting customer IDs and Names of drivers from the Road To Pro Series
result = sql.execute_query('SELECT CustomerID, Name FROM 00_Current ORDER BY Points DESC;')
#print(result)   # Debug to ensure select statement got proper data


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
        #if index != 0:
            # get points for that id from that event file
            result = sql.execute_query('SELECT Points FROM ' + name + ' WHERE CustomerID=' + str(id) + ';')
            # if there are no points, it's 0, otherwise the points from that event
            if result:
                pts_by_id.setdefault(id, []).append(result[0][0])
            else:
                pts_by_id.setdefault(id, []).append(0)
    # break  # breaking after first id for debug purposes

print(pts_by_id)
print()
print(pts_by_id.get(ids[0])[0])
print()

# Now take data and write it to csv for upload to DB
point_data_file = open('/home/eric/PycharmProjects/ir_standings_analyzer/Generated CSVs/RTP_Points_Table.csv', 'w')
point_data_file.write('\"custID\",\"Name\",\"DaytonaPts\",\"RockinghamPts\",\"HomesteadPts\",\"AtlantaPts\", '
                      '\"CharlotteRovalPts\",\"MichiganPts\",\"RichmondPts\",\"DarlingtonPts\",\"DoverPts\", '
                      '\"LasVegasPts\",\"CanadianTirePts\",\"TexasPts\",\"MartinsvillePts\",\"PhoenixPts\"\n')
"""point_data_file.write('\"' + str(ids[0]) + '\",\"' + str(pts_by_id.get(ids[0])[0]) + '\",\"' +
                      str(pts_by_id.get(ids[0])[1]) + '\",\"' + str(pts_by_id.get(ids[0])[2]) +
                      str(pts_by_id.get(ids[0])[3]) + '\",\"' + str(pts_by_id.get(ids[0])[4]) + '\",\"' +
                      str(pts_by_id.get(ids[0])[5]) + str(pts_by_id.get(ids[0])[6]) + '\",\"' +
                      str(pts_by_id.get(ids[0])[7]) + '\",\"' + str(pts_by_id.get(ids[0])[8]) +
                      str(pts_by_id.get(ids[0])[9]) + '\",\"' + str(pts_by_id.get(ids[0])[10]) + '\",\"' +
                      str(pts_by_id.get(ids[0])[11]) + str(pts_by_id.get(ids[0])[12]) + '\",\"' +
                      str(pts_by_id.get(ids[0])[13]) + '\"\n')"""

for i in range(len(ids)):
    print(i)
    new_line = '\"' + str(ids[i]) + '\",\"' + str(names[i]) + '\",\"'
    for x in range(num_races):
        print(x)
        new_line += str(pts_by_id.get(ids[i])[x])
        if x == 13:
            new_line += '\"\n'
        else:
            new_line += '\",\"'

    # print(new_line)
    point_data_file.write(new_line)
    # break

point_data_file.close()

commands = sql.get_commands_from_script(
    '/home/eric/PycharmProjects/ir_standings_analyzer/SQL Files & Scripts/table_racechart_creation.sql')
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

commands = sql.get_commands_from_script(
    '/home/eric/PycharmProjects/ir_standings_analyzer/SQL Files & Scripts/table_racechart_dataloading.sql')
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

result = sql.execute_query('SELECT * FROM Races_Chart;')
print(result)

# Close DB connection at end of program
sql.close_connection()
