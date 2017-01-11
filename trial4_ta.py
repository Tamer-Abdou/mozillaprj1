__author__ = 'tamer'

import pymongo
import requests
from bs4 import BeautifulSoup
import urllib.request

db = pymongo.MongoClient('localhost', port=27017).mozilla
db.rr_showclosed.drop()
# extract the diffs from review request review board

with open('datain/unique_pages.txt') as f:
    lines = f.read().splitlines()

baseurl = 'https://reviewboard.mozilla.org/r/?sort=review_id&datagrid-id=datagrid-0&columns=review_id&show-closed=1&page='



idlst = []

counter = 1
while counter <= 926:
#for counter in range(1,10):
    print(counter)
    url = baseurl + str(counter)
    html = urllib.request.urlopen(url)  # Insert your URL to extract
    bsObj = BeautifulSoup(html.read(), 'lxml')
    divs = bsObj.findAll("table", {"class": "datagrid-body"})
    rows = bsObj.findAll('td')


    for item in range(50):
        row = rows[item].find('a')
        obj = [row['href']]
        #print(obj)
        idlst.extend(obj)
        #print(idlst)
    counter += 1

import csv
outfile = open("C:/Users/tamer/PycharmProjects/mozillaprj1/rr_closed_id.csv", "w", newline='',encoding='utf-8')
writer = csv.writer(outfile)
header = ['id']
writer.writerow(header)

rows = zip(idlst)
print(rows)
for row in rows:
    writer.writerow(row)

