#!/usr/bin/env python
#coding:utf-8
#@Time: 2017/12/28下午9:46
#@Author: wangximei
#@File: prepare_data.py
#@describtion:generate dic

import csv
from collections import Counter
import operator
import pickle


def generate_dic(log_path):
    user_merchant_key_dic = {}
    user_key_dic = {}
    merchant_key_dic = {}
    with open(log_path) as file:
        hearders = next(file)
        lines = csv.reader(file)
        for line in lines:
            user = line[0]
            merchant = line[3]

            ## user_merchant_key_dic
            if (int(user), int(merchant)) in user_merchant_key_dic:
                print(user, merchant)
                pur_list = user_merchant_key_dic[(int(user),int(merchant))]
                pur_list.append(line)
                user_merchant_key_dic[int(user), int(merchant)] = pur_list
            else:
                user_merchant_key_dic[(int(user), int(merchant))] = [line]

            ## user_key_dic
            if int(user) in user_key_dic:
                pur_list = user_key_dic[int(user)]
                pur_list.append(line)
                user_key_dic[int(user)] = pur_list
            else:
                user_key_dic[int(user)] = [line]

            ## merchant_key_dic
            if int(merchant) in merchant_key_dic:
                pur_list = merchant_key_dic[int(merchant)]
                pur_list.append(line)
                merchant_key_dic[int(merchant)] = pur_list
            else:
                merchant_key_dic[int(merchant)] = [line]
    merchant2similar_dic = compute_similar_merchant(user_key_dic, merchant_key_dic)
    return user_merchant_key_dic, user_key_dic, merchant_key_dic, merchant2similar_dic

def read_user_info(user_path):
    user_fea = {}
    with open(user_path) as data_file:
        headers = next(data_file)
        lines = csv.reader(data_file)
        for line in lines:
            user_fea[int(line[0])] = line[1:]
    return user_fea

def transfer(dic):
    result_array = []
    for key,v in dic.items():
        for item in v:
            result_array.append(item)
    return result_array


def save_result(result,out_path,headers):
    with open(out_path,'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(headers)
        writer.writerows(result)


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
        # merchants 为与mid商家拥有共同用户最多的5个商家以及对应的共同用户数
        merchants = set(sorted_merchants)

        similar_merchant[mid] = merchants

    return similar_merchant



import os
if __name__ == "__main__":
    # test compute_similar_merchat method
    ukd = {}
    ukd[1] = [[0, 0, 0, 1]]
    ukd[1].append([0, 0, 0, 3])
    ukd[2] = [[0, 0, 0, 1], [0, 0, 0, 2]]
    ukd[3] = [[0, 0, 0, 1], [0, 0, 0, 2]]
    ukd[4] = [[0, 0, 0, 3]]
    mkd = {}
    mkd[1] = [[1, 0, 0, 1], [2, 0, 0, 1], [3, 0, 0, 1]]
    mkd[2] = [[2, 0, 0, 2], [3, 0, 0, 2]]
    mkd[3] = [[1, 0, 0, 3], [4, 0, 0, 3]]
    compute_similar_merchant(ukd, mkd)

    pre_path = os.path.dirname(os.path.dirname(os.getcwd()))
    user_path = pre_path + "/data/original_data/user_info_format1.csv"
    user_fea = read_user_info(user_path)

    log_path = pre_path + "/data/original_data/user_log_sample.csv"
    user_merchant_key_dic, user_key_dic, merchant_key_dic, merchant2similar_dic = generate_dic(log_path)

    headers = ['user_id','item_id','cat_id','seller_id','brand_id','time_stamp','action_type']
    user_merchant_result = transfer(user_merchant_key_dic)
    user_merchant_path = pre_path + "/data/prepare_data/user_merchant_result.csv"
    save_result(user_merchant_result,user_merchant_path,headers)

    user_result = transfer(user_key_dic)
    user_path = pre_path + "/data/prepare_data/user_result.csv"
    save_result(user_result,user_path,headers)

    merchant_result = transfer(merchant_key_dic)
    merchant_path = pre_path + "/data/prepare_data/merchant_result.csv"
    save_result(merchant_result,merchant_path,headers)

    similar_merchant_path = pre_path + "/data/prepare_data/similar_merchant.txt"
    f = open(similar_merchant_path, 'wb')
    pickle.dump(merchant2similar_dic, f)
