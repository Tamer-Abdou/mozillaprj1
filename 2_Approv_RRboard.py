__author__ = 'behjat'

import pymongo
import requests
import unicodecsv as csv

db = pymongo.MongoClient('localhost', port=27017).mozilla
# db.Approv_RRboard_3.drop()
''''
c = 0
for item in db.RRboard_3.find():
    if item["approved"] == True:
        db.Approv_RRboard_3.insert(item)
    c += 1
    if c % 100 == 0:
        print c
'''

with open('datain/bug_info_3.csv', 'w') as csvfile:
    fieldnames = ["_id", "faults", "review_req_id", "bugs", "code", "documentation", "error", "message"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for item in db.bug_info_3.find():
        #del item["_id"]
        writer.writerow(item)
