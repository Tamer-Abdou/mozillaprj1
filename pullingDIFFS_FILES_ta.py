__author__ = 'tamer'

import pymongo
import requests

db = pymongo.MongoClient('localhost', port=27017).mozilla
db.rr_diffs_files.drop()
# extract the diffs from review request review board

with open('datain/diff_files_links.txt') as f:
    lines = f.read().splitlines()


#baseurl = 'https://bugzilla.mozilla.org/rest/bug/'

for counter in lines:
    print(counter)
    url = counter
    # test_list = []
    maxy = 200
    #url = url + '?max-results=' + str(maxy)
    #c = 1
    #i = 0
    #while c:
        #url2 = url + '&start=' + str(i * maxy)
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        r.status_code = "Connection refused"

    r_json = r.json()
    print(url)
    rr_list = [r_json.get('files', [])]
    for rr in rr_list:
        print(rr)
            #if 'extra_data' in rr:
            #     del rr['extra_data']
        db.rr_diffs_files.insert(rr, check_keys=False)
    #c = len(rr_list)
    print(len(rr_list))



    #i += 1