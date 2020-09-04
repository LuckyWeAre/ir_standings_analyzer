from ir_webstats_rc_09012020 import constants as cts
from ir_webstats_rc_09012020.client import iRWebStats
from ir_webstats_rc_09012020.util import clean

file_var = open('../Private_Info.txt', 'r')
all_lines_var = file_var.readlines()

email = all_lines_var[1]
pswd = all_lines_var[2]

print(email)
print(pswd)

irw = iRWebStats()
irw.login(email, pswd)
if not irw.logged:
    print("INVALID CREDENTIALS")
    exit()

# res = irw.season_standings(season=2721, carclass=71, page=1)

# print(res)
# print(res[0][0]['displayname'])

# print()
print()

url1 = 'https://members.iracing.com/memberstats/member/GetSeasonStandings?format=csv&seasonid=2721&carclassid=71' \
       '&clubid=-1&raceweek=-1&division=-1&start=1&end=25&sort=points&order=desc'
resp = irw.download_csv(url1)
print(resp)
print(type(resp))
rtp_all_file = open('/home/eric/Desktop/00_Current.csv', 'w')
wrtr = rtp_all_file.write(resp)
rtp_all_file.close()

"""
for pg in range(67):
    print(pg)
    print((pg + 1))
    resu, totres = irw.season_standings(season=2721, carclass=71, page=(pg + 1))
    print(totres)
    print(resu)
    print(resu[0]['displayname'])
"""
"""
result_page, num_rows = irw.season_standings(season=2721, carclass=71)
print(result_page)

last_page = (int(num_rows / 25)) + 1
next_page = 2

while next_page < last_page:
    result_page, num_rows = irw.season_standings(season=2721, carclass=71, page=next_page)
    print(result_page[0]['displayname'])
"""
