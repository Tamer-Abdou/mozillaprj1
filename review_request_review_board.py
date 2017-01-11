__author__ = 'tamer'

import pprint
import pymongo
import requests

db = pymongo.MongoClient('localhost', port=27017).mozilla
db.RRboard_3.drop()                   #### is commented to not drop dataset accidently


# extract review request review board
# https://reviewboard.mozilla.org/r/?show-closed=1
baseurl = 'https://reviewboard.mozilla.org/'
suburl = '/api/review-requests/'
url = baseurl + suburl
# test_list = []

maxy = 100
url = url + '?max-results=' +  str(maxy)
c = 1
i = 0

while c:
    url2 = url + '&start=' + str(i * maxy)
    r = requests.get(url2)
    r_json = r.json()

    print(r_json.keys())
    print(r_json['links'])
    print(r_json['stat'])
    print(r_json['total_results'])
    print(url2)
    rr_list = r_json.get('review_requests', [])
    # pprint.pprint(rr_list[0])
    for rr in rr_list:
        #if 'extra_data' in rr:
        #    del rr['extra_data']
        print(rr)
        db.RRboard_3.insert(rr, check_keys=False)
        # for key in rr:
        #     if key not in test_list:
        #         test_list.append(key)


    c = len(rr_list)
    print(len(rr_list))
    # pprint.pprint(rr[-1])
    i += 1
# print test_list