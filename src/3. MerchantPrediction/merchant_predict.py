#!/usr/bin/env python
#coding:utf-8
#@Time: 2017/12/27下午9:04
#@Author: wangximei
#@File: merchant_predict.py
#@describtion:

import csv
def read_data(data_path):
    ori_data = []
    with open(data_path) as data_file:
        headers = next(data_file)
        lines = csv.reader(data_file)
        for line in lines:
            ori_data.append(line)
    return ori_data

def generate_feature(ori_data):

    a = 0


import os
if __name__ == "__main__":
    ## user_id,merchant_id,label
    pre_path = os.path.dirname(os.getcwd())
    train_path = pre_path + "/data/original_data/train_format1.csv"
    ori_data = read_data(train_path)
