#!/usr/bin/env python
#coding:utf-8
#@Time: 2017/12/27下午8:38
#@Author: wangximei
#@File: user_classify.py
#@describtion:

import csv
import os
def merchant_to_user(data_path):
    merchant_user = {}
    # purchase_items = []
    with open(data_path) as data_file:
        headers = next(data_file)
        lines = csv.reader(data_file)
        for line in lines:
            if (line[-1] == '2'):
                # purchase_items.append(line)
                # user_id, item_id, cat_id, seller_id, brand_id, time_stamp, action_type
                seller_id = line[3]
                user_id = line[0]
                if seller_id in merchant_user:
                    pur_list = merchant_user[seller_id]
                    pur_list.append(user_id)
                    merchant_user[seller_id] = pur_list
                else:
                    merchant_user[seller_id] = [user_id]
    return merchant_user

def user_to_fea(data_path):
    user_fea = {}
    with open(data_path) as data_file:
        headers = next(data_file)
        lines = csv.reader(data_file)
        for line in lines:
            user_fea[line[0]] = line[1:]
    return user_fea

def merchant_to_fea(merchant_user,user_fea):
    result = []
    for merchant,users in merchant_user.items():
        for user in users:
            if user in user_fea:
                fea = user_fea[user]
                res = [merchant,fea[0],fea[1]]
                result.append(res)
            else:
                print user
    return result

def cal_num(result):
    fea_to_num = {}
    for item in result:
        key = item[0] + "_" + item[1] + "_" + item[2]
        if key in fea_to_num:
            fea_to_num[key] += 1
        else:
            fea_to_num[key] = 1

    fea_num = []
    for key,num in fea_to_num.items():
        item = key.split("_")
        item.append(num)
        fea_num.append(item)
    return fea_num

def save_result(result,out_path,headers):
    with open(out_path,'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(headers)
        writer.writerows(result)

if __name__ == "__main__":
    pre_path = os.path.dirname(os.path.dirname(os.getcwd()))
    log_path = pre_path + "/data/user_log_format1.csv"
    # start_time = time.time()
    merchant_user = merchant_to_user(log_path)

    user_path = pre_path + "/data/user_info_format1.csv"
    user_fea = user_to_fea(user_path)

    result = merchant_to_fea(merchant_user, user_fea)

    out_path = pre_path + "/data/merchant_fea.csv"
    headers = ['merchant', 'age_range', 'gender']
    save_result(result, out_path,headers)

    fea_num = cal_num(result)
    out_path = pre_path + "/data/merchant_fea_num.csv"
    headers = ['merchant', 'age_range', 'gender','num']
    save_result(fea_num, out_path,headers)