"""from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://members.iracing.com/membersite/member/SeriesStandings.do?season=2721&carid=123')"""

#import csv
#import requests

#url2 = 'https://members.iracing.com/memberstats/member/GetSeasonStandings?format=csv&seasonid=2721&carclassid=71' \
      '&clubid=-1&raceweek=-1&division=-1&start=1&end=25&sort=points&order=desc '
#url1 = 'https://members.iracing.com/membersite/member/Home.do'    #this worked properly with authentication
# resp = requests.get(url, auth=('email', 'password'))

#ses = requests.Session()

#ses.post(url1, auth=('email', 'password'))

#resp1 = ses.get(url1)

#print(resp1.text)

#resp2 = ses.get(url2, cookies=resp1.cookies)

#print(resp2.text)

"""May need to use lib other than requests to create a session that emulates clicking the Output CSV button.
    Do further research into options to achieve downloading the csv from the site. Perhaps selenium..."""

"""with open('out.csv', 'w') as f:
    writer = csv.writer(f)
    for line in resp.iter_lines():
        writer.writerow(line.decode('utf-8').split(','))"""

import ir_webstats
from ir_webstats.client import iRWebStats
