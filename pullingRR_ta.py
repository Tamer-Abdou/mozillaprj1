__author__ = 'tamer'

import pymongo
import requests

db = pymongo.MongoClient('localhost', port=27017).mozilla
db.rr_closed_pending.drop()
# extract the diffs from review request review board

with open('datain/rr_unique_closed.txt') as f:
    lines = f.read().splitlines()

baseurl = 'https://reviewboard.mozilla.org/api/review-requests/'
suburl = '/'

for counter in lines:
    print(counter)
    url = baseurl + counter + suburl
    print(url)
    # test_list = []
    #maxy = 200
    #url = url + '?max-results=' + str(maxy)
    #c = 1
    #i = 0
    #while c:
        #url2 = url + '&start=' + str(i * maxy)
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        r.status_code = "Connection refused"
    #r = requests.get(url)
    r_json = r.json()
    print(r_json)
    rr_list = [r_json.get('review_request', [])]
    print(rr_list)
    #print(rr_list[1])
    for rr in rr_list:
        print(rr)
        db.rr_closed_pending.insert(rr, check_keys=False)
    #c = len(rr_list)
    print(len(rr_list))