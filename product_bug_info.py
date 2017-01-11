import pymongo
import requests
import datetime
import pprint

db = pymongo.MongoClient('localhost', port=27017).mozilla

# create Ap_bug_info_3
# create all bug info, not only approved one: bug_info_3

#db.Ap_bug_info_3.drop()
db.bug_info_3.drop()

i = 0
notBug = []
for item in db.RRboard_3.find(no_cursor_timeout=True):
    i += 1
    if i % 200 == 0:
        print(i)
    if len(item["bugs_closed"]) != 0:
        bug_id = item["bugs_closed"][0]
        url = 'https://bugzilla.mozilla.org/rest/bug/' + bug_id
        A = requests.get(url)
        A_json = A.json()
        A_json["review_req_id"] = item["id"]
        db.bug_info_3.insert(A_json)
    else:
        notBug.append(item['id'])
print ("list of rr with no Bugid, number of them: ", notBug, len(notBug))


'''
# number of distinct products
dict1 = {}
for item in db.Ap_bug_info_3.find({'bugs': {'$exists': True}}):
    dict1[item['bugs'][0]['product']] = 1

print ('number of different products:', len(dict1))
pprint.pprint(dict1)


'

# how many items of each products?

Firefox_count = 0
Firefox_Graveyard_count = 0
Firefox_Health_Report_count = 0
Firefox_OS_count = 0
Firefox_for_Android_count = 0
Core_count = 0
dic1 = {}
for item in db.Ap_bug_info_3.find({'bugs': {'$exists': True}}):
        if item['bugs'][0]['keywords']:
            if item['bugs'][0]['keywords'] != "":
                for k in item['bugs'][0]['keywords']:
                    dic1[k] = 1
            if item['bugs'][0]['keywords'] == 'enhancement':
                Firefox_count += 1
        if item['bugs'][0]['product'] == 'Firefox Graveyard':
            Firefox_Graveyard_count =+ 1
        if item['bugs'][0]['product'] == 'Firefox Health Report':
            Firefox_Health_Report_count += 1
        if item['bugs'][0]['product'] == 'Firefox OS':
            Firefox_OS_count += 1
        if item['bugs'][0]['product'] == 'Firefox for Android':
            Firefox_for_Android_count += 1
        if item['bugs'][0]['product'] == 'Firefox':
            Firefox_count += 1
        if item['bugs'][0]['product'] == 'Core':
            Core_count += 1



print ('number of items of Firefox: ', Firefox_count)
print dic1
print len(dic1)
print ('number of items of Firefox Graveyard: ', Firefox_Graveyard_count)
print ('number of items of Firefox_Health_Report: ', Firefox_Health_Report_count)
print ('number of items of Firefox_OS_count: ', Firefox_OS_count)
print ('number of items of Firefox_for_Android_count: ', Firefox_for_Android_count)
print ('number of items of Core_count: ', Core_count)
print ('number of items of Firefox_count: ', Firefox_count)

'''