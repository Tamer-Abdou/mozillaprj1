__author__ = 'behjat'

import pymongo
import requests
import datetime
import pprint
import math
import csv

db = pymongo.MongoClient('localhost', port=27017).mozilla


#db.Approv_RRboard_Metrics.drop()
#db.last_interact_files.drop()

#db.Approv_RRboard_Metrics_2_Core.drop()

## for all three Core, Firefox, Firefox for Android

#db.Approv_RRboard_Metrics_3.drop()
db.Approv_RRboard_Metrics_3_2.create_index([('REVIEW_REQ_ID', pymongo.ASCENDING)])
db.extract_churn_org_3_Core_Fire_Andr.create_index([('review_request_id', pymongo.ASCENDING)])
db.extract_churn_3_Core_Fire_Andr.create_index([('review_request_id', pymongo.ASCENDING)])
db.diff_comments_3.create_index([('REVIEW_REQ_ID', pymongo.ASCENDING)])

c = 0
no_bugs = 0

# # change the type of time in extract_churn_org_2_Core
# for item in db.extract_churn_org_3_Core_Fire_Andr.find():
#         t = datetime.datetime.strptime(item["last_updated"], "%Y-%m-%dT%H:%M:%SZ")
#         db.extract_churn_org_3_Core_Fire_Andr.update({"_id": item["_id"]}, {'$set': {"last_updated": t}})

# # add developer name to defective_file_patch database **
# for item in db.RRboard_3.find():
#     db.defective_file_path_2.update_many({"REVIEW_REQ_ID": item["id"]},
#                                          {"$set": {"submitter": item["links"]["submitter"]["title"]}})

#  find the min time of file modification for each file in each review request **
# for item in db.defective_file_path.find():
#     t = datetime.datetime.strptime(item["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
#     rr = item["REVIEW_REQ_ID"]
#     reviewer = item["user"]
#     u_file = item["defective_path"]
#     submitter = item["submitter"]
#     current = db.last_interact_files.find_one({"REVIEW_REQ_ID": rr, "user": reviewer, "defective_path": u_file})
#     if current:
#         if current["timestamp"] > t:
#             db.last_interact_files.update({"_id": current["_id"]}, {'$set': {"timestamp": t}})
#     else:
#         db.last_interact_files.insert({"REVIEW_REQ_ID": rr, "user": reviewer, "defective_path": u_file, "timestamp": t,
#                                        "submitter": submitter})


for item in db.Approv_RRboard_3_Core_Fire_Andr.find(no_cursor_timeout=True):
## age vojud dare dige nagire
    # if db.Approv_RRboard_Metrics_3_2.find_one({'REVIEW_REQ_ID': item['id']}):
    #     continue

    metrics = {}
    #    url_files = item["links"]["diff_context"]["href"]
    #   r = requests.get(url_files)
    #   r_json = r.json()

    # number of reviewers
    list_rev = []
    for item1 in db.extract_churn_org_3_Core_Fire_Andr.find({"review_request_id": item["id"]}):
        list_rev.extend(item1["reviewer"])

    list_rev = list(set(list_rev))
    metrics["number of reviewer"] = len(list_rev)

    # issue related metrics
    metrics["REVIEW_REQ_ID"] = item["id"]
    metrics["issue_open_count"] = item["issue_open_count"]
    metrics["issue_dropped_count"] = item["issue_dropped_count"]
    metrics["issue_resolved_count"] = item["issue_resolved_count"]
    # review time
    t1 = datetime.datetime.strptime(item["time_added"], "%Y-%m-%dT%H:%M:%SZ")
    t2 = datetime.datetime.strptime(item["last_updated"], "%Y-%m-%dT%H:%M:%SZ")
    duration = t2 - t1
    metrics["review_time_duration(sec)"] = duration.total_seconds()

    # number of comments
    total_number_comments = 0
    for N_Comment in db.diff_comments_3.find({"REVIEW_REQ_ID": item["id"]}):
        total_number_comments += N_Comment["total_results"]
    metrics["number_Reviewer_comments"] = total_number_comments

    # churn metrics

    Total_patch_LOC_n = 0
    LOC_added_n = 0
    LOC_deleted_n = 0
    LOC_replaced_n = 0

    churn_item = db.extract_churn_3_Core_Fire_Andr.find_one({"review_request_id": item["id"]})
    for files_item in churn_item["files"]:

        Total_patch_LOC_n += files_item["extra_data"].get("total_line_count", 0)
        LOC_added_n += files_item["extra_data"].get("raw_insert_count", 0)
        LOC_deleted_n += files_item["extra_data"].get("raw_delete_count", 0)
        LOC_replaced_n += files_item["extra_data"].get("replace_count", 0)

    metrics["size of patch (N_of_files)"] = churn_item["total_results"]
    metrics["Total_patch_LOC"] = Total_patch_LOC_n
    metrics["LOC_added"] = LOC_added_n
    metrics["LOC_deleted"] = LOC_deleted_n
    metrics["LOC_replaced"] = LOC_replaced_n

    # reviewer avg recency interaction
    # if they were in same month, last interact= 1, if last month = 1/2
    list1 = []
    list2 = []
    for current in db.extract_churn_org_3_Core_Fire_Andr.find({"review_request_id": item["id"]}):
        # print "avaliiiiiiiiiiiiiiiii"
        tss = []
        for comp__ in db.extract_churn_org_3_Core_Fire_Andr.find({"review_request_id": {'$ne': current["review_request_id"]},
                                                        "$or": [{"source_file": current["source_file"]},
                                                                {"dest_file": current["source_file"]}],
                                                        "$or": [{"reviewer": {"$in": current["reviewer"]}},
                                                                {"submitter": {"$in": current["reviewer"]}}],
                                                        "last_updated": {'$lt': current["last_updated"]}}):
            # print "dovomiiiiiiiiiiissssssssssssssss"
            tss.append(comp__['last_updated'])

        tss.sort(reverse=True)

        if tss:
            last_interact1 = current["last_updated"] - tss[0]
            list1.append(last_interact1.total_seconds())
            # print("list1", list1)

        for ts in tss:
            last_interact2 = current["last_updated"] - ts
            list2.append(last_interact2.total_seconds())
            # print("list2", list2)


    if len(list1) == 0:
        metrics["r_last_interact(month)"] = -1
    else:
        list1 = map(lambda x: 1.0 / math.ceil(x / (3600 * 24 * 30.0)), list1)
        metrics["r_last_interact(month)"] = sum(list1) / len(list1)

    if len(list2) == 0:
        metrics["r_Avg_interact(month)"] = -1
    else:
        list2 = map(lambda x: 1.0 / math.ceil(x / (3600 * 24 * 30.0)), list2)
        metrics["r_Avg_interact(month)"] = sum(list2) / len(list2)

    # developer avg recency interaction
    # if they were in same month, last interact= 1, if last month = 1/2

    list1 = []
    list2 = []
    for current in db.extract_churn_org_3_Core_Fire_Andr.find({"review_request_id": item["id"]}):
        tss = []

        for comp__ in db.extract_churn_org_3_Core_Fire_Andr.find({"review_request_id": {'$ne': current["review_request_id"]},
                                                        "$or": [{"source_file": current["source_file"]},
                                                                {"dest_file": current["source_file"]}],
                                                        "$or": [{"reviewer": current["submitter"]},
                                                                {"submitter": current["submitter"]}],
                                                        "last_updated": {'$lt': current["last_updated"]}}):
            tss.append(comp__['last_updated'])

        tss.sort(reverse=True)

        if tss:
            last_interact1 = current["last_updated"] - tss[0]
            list1.append(last_interact1.total_seconds())

        for ts in tss:
            last_interact2 = current["last_updated"] - ts
            list2.append(last_interact2.total_seconds())

    if len(list1) == 0:
        metrics["submitter_last_interact(month)"] = -1
    else:
        list1 = map(lambda x: 1.0 / math.ceil(x / (3600 * 24 * 30.0)), list1)
        metrics["submitter_last_interact(month)"] = sum(list1) / len(list1)

    if len(list2) == 0:
        metrics["submitter_Avg_interact(month)"] = -1
    else:
        list2 = map(lambda x: 1.0 / math.ceil(x / (3600 * 24 * 30.0)), list2)
        metrics["submitter_Avg_interact(month)"] = sum(list2) / len(list2)

        # bug-report related metrics
    for rr in db.Ap_bug_info_3.find({"review_req_id": item["id"]}):
        if "bugs" not in rr:
            no_bugs += 1
            # pprint.pprint(rr)
        else:
            metrics["bug_priority"] = rr["bugs"][0]["priority"]
            metrics["bug_severity"] = rr["bugs"][0]["severity"]

    # defective information (based on 1?? week)
    list_files_p = []
    dic_files_ch = {}
    for p_files in db.extract_churn_org_3_Core_Fire_Andr.find({"review_request_id": item["id"]}):
        list_files_p.append(p_files["dest_file"])
        # print("list_file_p and review request", list_files_p, item["id"])

        for ch_files in db.extract_churn_org_3_Core_Fire_Andr.find({"review_request_id": {"$ne": item["id"]}}):
            if ch_files["last_updated"] > p_files["last_updated"]:
                duration = ch_files["last_updated"] - p_files["last_updated"]
                if 0 < duration.total_seconds() < 3600 * 24 * 7:
                    dic_files_ch[(ch_files["source_file"], ch_files["review_request_id"])] = 1

    # pprint.pprint(dic_files_ch)
    # print list_files_p
    defect_count = 0
    # dic_f = [_x[0] for _x in dic_files_ch]

    dic_f = {}
    for _x in dic_files_ch:
        k = _x[0]
        v = _x[1]
        if k in dic_f:
            dic_f[k].append(v)
        else:
            dic_f[k] = [v]

    for lp in list_files_p:
        if lp in dic_f:

            for rr in dic_f[lp]:
                # print rr, lp
                for Ap_bug in db.Ap_bug_info_3.find({"review_req_id": rr}): #review_request_id
                    for bug_reason in Ap_bug["bugs"]:
                        if bug_reason["severity"] is not "enhancement":
                            defect_count += 1
                            break

    if defect_count == 0:
        metrics["defective"] = 0
    else:
        metrics["defective"] = 1

    db.Approv_RRboard_Metrics_3_2.insert(metrics)

print(no_bugs)


# update the result with complexity metrics
ratio = 0

for item in db.Approv_RRboard_Metrics_3_2.find():
    for item2 in db.extract_churn_org_3_Core_Fire_Andr.find({"review_request_id": item["REVIEW_REQ_ID"]}):
        comp = db.source_files_3.find_one({"$and": [{"review_request_id": item2["review_request_id"]}, {"source_file": item2["source_file"]}]})
        numerator = item2["extra_data"].get("raw_insert_count", 0) + item2["extra_data"].get("raw_delete_count", 0) + item2["extra_data"].get("replace_count", 0)
        ratio += numerator * (comp["cyclomatic_complexity"]) / item2["extra_data"].get("total_line_count", max(numerator, 1000))

    db.Approv_RRboard_Metrics_3_2.update({'_id': item['_id']},
                                            {'$set': {'Avg_cyclomatic_complexity': ratio}})





'''


# write metrics in a csv


with open('datain/raw3_corefire.csv', 'w') as csvfile:
    fieldnames = ['_id', 'number of reviewer', 'r_last_interact(month)', 'review_time_duration(sec)', 'defective', 'submitter_last_interact(month)',
                  'LOC_deleted', 'issue_resolved_count', 'size of patch (N_of_files)', 'LOC_replaced', 'issue_open_count',
                  'issue_dropped_count', 'REVIEW_REQ_ID', 'submitter_Avg_interact(month)', 'number_Reviewer_comments',
                  'Total_patch_LOC', 'r_Avg_interact(month)', 'LOC_added', 'bug_severity', 'bug_priority', "Avg_cyclomatic_complexity"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for item in db.Approv_RRboard_Metrics_3_2.find():
        del item["_id"]
        writer.writerow(item)







'''

'''
keyword filed in bugreport, that are nnot bugs:

"APIchange", "autoland", "bmo-big", "bmo-goal", "checkin-needed", "trunk",
                                              "clownshoes", "compat", "csectype-disclosure", "csectype-sop", "DBI-cust-Business",
                                              "DBI-cust-CloudServices", "DBI-cust-EngagementAndMarketing", "DBI-cust-Finance",
                                              "DBI-cust-Firefox", "DBI-cust-FirefoxOS", "DBI-cust-Foundation",
                                              "DBI-cust-InsightsAndStrategy", "DBI-cust-IT", "DBI-cust-Labs", "DBI-cust-Legal",
                                              "DBI-cust-Marketplace", "DBI-cust-People", "DBI-cust-Platform", "DBI-cust-SUMO",
                                              "event-discussion-needs-final-approval", "event-discussion-needs-review",
                                              "event-discussion-no-further-action", "event-discussion-pending-additional-information",
                                              "event-discussion-pending-fulfilment", "event-discussion-pre-approved-needs-final-approval",
                                              "event-request-no-further-action", "event-request-pending-fulfilment",
                                              "event-request-under-review", "feature", "mail-integration", "power",
                                              "productization", "productwanted", "qaurgent", "qaurgent", "sec-high", "sec-low",
                                              "sec-moderate", "sec-vector", "sec-want", "selenium", "technote", "testcase",
                                              "urwanted", "ux-affordance", "ux-consistency", "ux-control", "ux-discovery",
                                              "ux-efficiency", "ux-error-prevention", "ux-error-recovery", "ux-implementation-level",
                                              "ux-interruption", "ux-jargon	", "ux-minimalism", "ux-mode-error", "ux-natural-mapping",
                                              "ux-tone", "ux-undo", "ux-userfeedback", "ux-visual-hierarchy", "website-graveyard",
                                              "wsec-automation-attack", "wsec-bruteforce", "wsec-client", "wsec-crypto",
                                              "wsec-disclosure", "wsec-email", "wsec-headers", "wsec-impersonation", "wsec-injection",
                                              "wsec-objref", "wsec-oscmd", "wsec-selfxss", "wsec-sqli"
'''
