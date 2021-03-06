#!/usr/bin/env python
#coding:utf-8
#@Time: 2018/1/2下午11:47
#@Author: wangximei
#@File: 1.py
#@describtion:

#!/usr/bin/env python
#coding:utf-8
#@Time: 2017/12/25下午4:33
#@Author: wangximei
#@File: get_frequent_items.py
#@describtion:


import testfpgrowth
import csv
import pandas as pd
def read_dataset_pandas(data_path):
    data = pd.read_csv(data_path)
    purchase_items = data[data.action_type =='2']
    print data.head()
    return purchase_items

def read_dataset_csv(data_path):
    purchase_group = {}
    # purchase_items = []
    with open(data_path) as data_file:
        headers = next(data_file)
        lines = csv.reader(data_file)
        for line in lines:
            if(line[-1] == '2'):
                # purchase_items.append(line)
                item_id = line[1]
                time_stamp = line[-2]
                if time_stamp in purchase_group:
                    pur_list = purchase_group[time_stamp]
                    pur_list.append(item_id)
                    purchase_group[time_stamp] = pur_list
                else:
                    purchase_group[time_stamp] = [item_id]
    return purchase_group

def to_transactions(purchase_group):
    transactions = []
    for time_stamp,pur_list in purchase_group.items():
        transactions.append(pur_list)
    return transactions

import os
import time
import sys
if __name__ == "__main__":
    sys.setrecursionlimit(1000000)
    pre_path = os.path.dirname(os.path.dirname(os.getcwd()))
    data_path = pre_path + "/data/original_data/user_log_sample.csv"
    purchase_group = read_dataset_csv(data_path)

    start_time = time.time()
    transactions = to_transactions(purchase_group)
    end_time_1 = time.time()
    print "mining pattern running time :",end_time_1-start_time
    print len(transactions)
    support_threshold = int(float(len(transactions))*0.03)
    print support_threshold
    min_prob = 0.9
    testfpgrowth.run_fpgrowth(transactions, support_threshold, min_prob)
    end_time_2 = time.time()
    print "mining rules running time :",end_time_1-start_time

