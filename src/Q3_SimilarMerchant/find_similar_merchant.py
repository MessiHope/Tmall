import os
import csv
import operator
import pickle
import sys
from collections import Counter


def dumpclean(mid, obj):
    print('merchant_id,\t sim_merchant_id,\t count')
    isFirst = True
    for item in obj:
        if isFirst:
            print('%s\t %s\t %s' % (mid, item[0], item[1]))
            isFirst = False
        else:
            print('\t %s\t %s' % (item[0], item[1]))


def dump(dic):
    for x in dic:
        print(x)
        for y in dic[x]:
            print(y, ':', dic[x][y])


def find_similar_merchant(mid, merchant2similar_dic):
    return merchant2similar_dic[mid]


def generate_user_and_merchant_dic(log_path):
    user_key_dic = {}
    merchant_key_dic = {}
    with open(log_path) as file:
        next(file)
        lines = csv.reader(file)
        for line in lines:
            user = line[0]
            merchant = line[3]

            # user_key_dic
            if int(user) in user_key_dic:
                pur_list = user_key_dic[int(user)]
                pur_list.append(line)
                user_key_dic[int(user)] = pur_list
            else:
                user_key_dic[int(user)] = [line]

            # merchant_key_dic
            if int(merchant) in merchant_key_dic:
                pur_list = merchant_key_dic[int(merchant)]
                pur_list.append(line)
                merchant_key_dic[int(merchant)] = pur_list
            else:
                merchant_key_dic[int(merchant)] = [line]
    return user_key_dic, merchant_key_dic


def compute_similar_merchant(user_key_dic, merchant_key_dic):
    mid2uid = {}
    uid2mid = {}
    for item in merchant_key_dic.items():
        mid = int(item[0])
        for log in item[1]:
            if mid2uid.get(mid) is None:
                mid2uid[mid] = set()
            uid = int(log[0])
            mid2uid[mid].add(uid)

    for item in user_key_dic.items():
        uid = int(item[0])
        for log in item[1]:
            if uid2mid.get(uid) is None:
                uid2mid[uid] = set()
            mid = int(log[3])
            uid2mid[uid].add(mid)
    similar_merchant = {}
    for mid in mid2uid.keys():
        user_set = mid2uid[mid]
        merchant_list = []
        for uid in user_set:
            merchant_list.extend(list(uid2mid[uid]))
        merchants_dict = Counter(merchant_list)

        sorted_merchants = sorted(merchants_dict.items(), key=operator.itemgetter(1), reverse=True)
        sorted_merchants = sorted_merchants[:6]
        for item in sorted_merchants:
            if item[0] == mid:
                sorted_merchants.remove(item)
        merchants = set(sorted_merchants)

        similar_merchant[mid] = merchants

    return similar_merchant


if __name__ == "__main__":
    mid = sys.argv[1]
    pre_path = os.path.dirname(os.path.dirname(os.getcwd()))
    similar_merchant_path = pre_path + "/../data/prepare_data/similar_merchant.txt"
    merchant2similar_dic = {}
    if os.path.exists(similar_merchant_path):
        merchant2similar_dic = pickle.load(similar_merchant_path)
    else:
        log_path = pre_path + "/data/original_data/user_log_sample.csv"
        user_key_dic, merchant_key_dic = generate_user_and_merchant_dic(log_path)
        merchant2similar_dic = compute_similar_merchant(user_key_dic, merchant_key_dic)
    merchants = {}
    merchants = find_similar_merchant(mid, merchant2similar_dic)
    dumpclean(mid, merchants)


