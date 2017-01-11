__author__ = 'tamer'

import pymongo
import requests

db = pymongo.MongoClient('localhost', port=27017).mozilla
db.rr_bugs.drop()
# extract the diffs from review request review board

with open('datain/bb_unique.txt') as f:
    lines = f.read().splitlines()


baseurl = 'https://bugzilla.mozilla.org/rest/bug/'

for counter in lines:
    print(counter)
    url = baseurl + counter
    # test_list = []
    maxy = 200
    #url = url + '?max-results=' + str(maxy)
    #c = 1
    #i = 0
    #while c:
        #url2 = url + '&start=' + str(i * maxy)
    r = requests.get(url)
    r_json = r.json()
    print(url)
    rr_list = r_json.get('bugs', [])
    for rr in rr_list:
        print(rr)
            #if 'extra_data' in rr:
            #     del rr['extra_data']
        db.rr_bugs.insert(rr)
    #c = len(rr_list)
    print(len(rr_list))



    #i += 1