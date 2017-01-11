#Tamer
import csv
import pymongo
import requests

db = pymongo.MongoClient('localhost', port=27017).mozilla

# find all documents
results = db.RRboard_3.names()


with open('datain/RRboard_3.csv', 'w') as csvfile:
    fieldnames = ["_id", "faults", "review_req_id", "bugs", "code", "documentation", "error", "message"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for item in db.RRboard_3.find():
        #del item["_id"]
        writer.writerow(item)
