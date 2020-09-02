# Imports
import pymysql
from pyracing.client import Client
import asyncio

file_var = open('/home/eric/Desktop/Login Info')
all_lines_var = file_var.readlines()

username = all_lines_var[1]
password = all_lines_var[2]

ir = Client(username, password)

# Helpers

"""def openConnection():
    myDB = pymysql.connect(host="localhost", user="root", passwd="Tpwifsql", db="RTP")
    return myDB

def getColumnHeaders(connection, tableName):
    getCH = connection.cursor()
    getCH.execute("DESC " + tableName)
    return getCH.fetchall()"""


async def main():
    """seasons_list = await ir.current_seasons()

    for season in seasons_list:
        if season.season_id == 2846:
            print(f'Schedule for {season.series_name_short}'
                  f'  ({season.season_year} S{season.season_quarter})')

            for t in season.tracks:
                print(f'\tWeek {t.race_week} will take place at {t.name} ({t.config})')"""

    # seasons_standings_list = await ir.season_standings(season_id=2721, result_num_low=0, result_num_high=50)
    # for i in range(len(seasons_standings_list)):
    # print(seasons_standings_list[i].display_name)

    # Total Number of participants in the season
    num_drivers_to_request = 250   #1641
    looking_range = int(num_drivers_to_request / 50) + 1
    print(looking_range)

    for x in range(looking_range):
        seasons_standings_list = await ir.season_standings(season_id=2721, result_num_low=(x * 50 + 1),
                                                           result_num_high=((x + 1) * 50))
        print('pos', '|', 'name', '|', 'points', '|', 'dropped', '|', 'club' '|', 'country', '|', 'irating', '|',
              'avgFin', '|', 'top5s', '|', 'starts', '|', 'lapsLed', '|', 'wins', '|', 'inc', '|', 'div', '|', 'week',
              '|', 'lapscomp', '|', 'poles', '|', 'avgStart', '|', 'custID')
        for i in range(len(seasons_standings_list)):
            print(seasons_standings_list[i].pos, '|',
                  seasons_standings_list[i].display_name, '|',
                  seasons_standings_list[i].points, '|',
                  seasons_standings_list[i].dropped, '|',
                  seasons_standings_list[i].club_name, '|',
                  seasons_standings_list[i].country_name, '|',
                  seasons_standings_list[i].irating, '|',
                  seasons_standings_list[i].pos_finish_avg, '|',
                  seasons_standings_list[i].top_fives, '|',
                  seasons_standings_list[i].starts, '|',
                  seasons_standings_list[i].laps_led, '|',
                  seasons_standings_list[i].wins, '|',
                  seasons_standings_list[i].incidents, '|',
                  seasons_standings_list[i].division, '|',
                  seasons_standings_list[i].week, '|',
                  seasons_standings_list[i].laps, '|',
                  seasons_standings_list[i].poles, '|',
                  seasons_standings_list[i].pos_start_avg, '|',
                  seasons_standings_list[i].cust_id)
            # print(seasons_standings_list[i].weeks_counted)


asyncio.run(main())

# Main

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
