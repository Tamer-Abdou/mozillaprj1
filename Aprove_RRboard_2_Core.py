__author__ = 'behjat'

import pymongo

db = pymongo.MongoClient('localhost', port=27017).mozilla

# Approv_RRboard_2_Core was only for Mozilla Core, Approv_RRboard_3_Core_Fire is for Mozilla Core,
# Firefox and Firefox for Android

# db.Approv_RRboard_2_Core.drop()
db.Approv_RRboard_3_Core_Fire_Andr.drop()

'''
# first store rr that correspond with Core product
list1 = []
for item in db.Ap_bug_info_2.find({"bugs": {"$exists": True}}):
    if item['bugs'][0]['product'] == 'Core':
        list1.append(item['review_req_id'])


for item in db.Approv_RRboard_2.find():
    if item['id'] in list1:
        db.Approv_RRboard_2_Core.insert(item)
'''
l = 0
# same approach as above with slight changes to extract review requests for all Core, Firefox and Firefox for android
for item in db.Ap_bug_info_3.find({"bugs": {"$exists": True}}):
    if item['bugs'][0]['product'] == 'Core' or item['bugs'][0]['product'] == 'Firefox for Android' or item['bugs'][0]['product'] == 'Firefox':
        item_final = db.Approv_RRboard_3.find_one({"id": item['review_req_id']})
        item_final["product"] = item['bugs'][0]['product']
        if db.Approv_RRboard_3_Core_Fire_Andr.find_one({'_id': item_final['_id']}):
            l += 1
            print (l, item_final["id"])
        else:
            db.Approv_RRboard_3_Core_Fire_Andr.insert(item_final)
