__author__ = 'tamer'

import pymongo
import requests

db = pymongo.MongoClient('localhost', port=27017).mozilla
db.rr_diffs.drop()
# extract the diffs from review request review board

with open('datain/rr_unique_closed.txt') as f:
    lines = f.read().splitlines()

baseurl = 'https://reviewboard.mozilla.org/api/review-requests/'
suburl = '/diffs/'

for counter in lines:
    url = baseurl + counter + suburl
    # test_list = []
    maxy = 200
    url = url + '?max-results=' + str(maxy)
    c = 1
    i = 0
    while c:
        url2 = url + '&start=' + str(i * maxy)
        r = requests.get(url2)
        r_json = r.json()
        print(url2)
        rr_list = r_json.get('diffs', [])
        for rr in rr_list:
            #if 'extra_data' in rr:
             #   del rr['extra_data']
            db.rr_diffs.insert(rr)
        c = len(rr_list)
        print(len(rr_list))
        i += 1