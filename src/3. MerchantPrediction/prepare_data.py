#!/usr/bin/env python
#coding:utf-8
#@Time: 2017/12/28下午9:46
#@Author: wangximei
#@File: prepare_data.py
#@describtion:generate dic

import csv

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
            if (user,merchant) in user_merchant_key_dic:
                print (user,merchant)
                pur_list = user_merchant_key_dic[(user,merchant)]
                pur_list.append(line)
                user_merchant_key_dic[(user,merchant)] = pur_list
            else:
                user_merchant_key_dic[(user,merchant)] = [line]

            ## user_key_dic
            if user in user_key_dic:
                pur_list = user_key_dic[user]
                pur_list.append(line)
                user_key_dic[user] = pur_list
            else:
                user_key_dic[user] = [line]

            ## merchant_key_dic
            if merchant in merchant_key_dic:
                pur_list = merchant_key_dic[merchant]
                pur_list.append(line)
                merchant_key_dic[merchant] = pur_list
            else:
                merchant_key_dic[merchant] = [line]
    return user_merchant_key_dic,user_key_dic,merchant_key_dic

def read_user_info(user_path):
    user_fea = {}
    with open(user_path) as data_file:
        headers = next(data_file)
        lines = csv.reader(data_file)
        for line in lines:
            user_fea[line[0]] = line[1:]
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

import os
if __name__ == "__main__":
    pre_path = os.path.dirname(os.path.dirname(os.getcwd()))
    user_path = pre_path + "/data/original_data/user_info_format1.csv"
    user_fea = read_user_info(user_path)

    log_path = pre_path + "/data/original_data/user_log_format1.csv"
    user_merchant_key_dic, user_key_dic, merchant_key_dic = generate_dic(log_path)

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

