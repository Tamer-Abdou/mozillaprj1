__author__ = 'behjat'

import pprint
import pymongo
import requests

db = pymongo.MongoClient('127.0.0.1', port=27017).mozilla

#this is only for core system, which gets for loop on : for item in db.Approv_RRboard_2_Core.find(no_cursor_timeout=True):
#db.extract_churn_2_Core.drop()

#then we change it for core firefoc android
db.extract_churn_3_Core_Fire_Andr.drop()

c = 0
for item in db.Approv_RRboard_3_Core_Fire_Andr.find(no_cursor_timeout=True):
    c += 1
    if c % 50 == 0:
        print(c)
    url1 = 'https://reviewboard.mozilla.org/api/review-requests/'+str(item["id"])+'/diffs/'
    #url1 = 'https://reviewboard.mozilla.org/api/review-requests/91674/diffs/'
    r1 = requests.get(url1)
    r1_json = r1.json()
    i = len(r1_json["diffs"])
    r2_json = {}
    url2 = 'https://reviewboard.mozilla.org/api/review-requests/'+str(item["id"])+'/diffs/'+str(i)+'/files/'
    #url2 = 'https://reviewboard.mozilla.org/api/review-requests//91674/diffs/' + str(i) + '/files/'
    r2 = requests.get(url2)
    r2_json = r2.json()
    r2_json["review_request_id"] = item["id"]
    r2_json["last_updated"] = item["last_updated"]
    r2_json["submitter"] = item["links"]["submitter"]['title']
    r2_json["bugs_closed"] = item["bugs_closed"]
    r2_json["product"] = item["product"]
    r2_json["reviewer"] = [t['title'] for t in item["target_people"]]

    db.extract_churn_3_Core_Fire_Andr.insert(r2_json)
