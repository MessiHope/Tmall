#!/usr/bin/env python
#coding:utf-
#@Time: //下午:
#@Author: wangximei
#@File: feature.py
#@describtion:

import os
from multiprocessing import Pool

import base
import prepare_data


class GenerateFeatures:
    def __init__(self):
        self.user_merchant_key_dic = {}
        self.user_key_dic = {}
        self.merchant_key_dic = {}
        self.user_info = {}
    def gen_dic(self,log_path,user_path):
        user_merchant_key_dic, user_key_dic, merchant_key_dic = prepare_data.generate_dic(log_path)
        self.user_merchant_key_dic = user_merchant_key_dic
        self.user_key_dic = user_key_dic
        self.merchant_key_dic = merchant_key_dic
        self.user_info = prepare_data.read_user_info(user_path)

    ##----------------user feature------------------
    def is_new_user(self,user_log):
        is_new_user_flag = 0
        for item in user_log:
            time_stamp = item[-2]
            if(time_stamp < "1111"):
                is_new_user_flag = 1
                break
        return is_new_user_flag
    # TODO def user_ ……
    ##  add more features of user





    ##----------------merchant feature------------------
    def cal_purchase_11_rate(self,merchant_log):
        purchase_11_num = 0
        purchase_all_num = 0
        for item in merchant_log:
            action_type = item[-1]
            if (action_type != "2"):
                continue
            time_stamp = item[-2]
            purchase_all_num += 1
            if (time_stamp == "1111"):
                purchase_11_num += 1
        if purchase_all_num == 0:
            return 0.0
        else:
            return purchase_11_num / float(purchase_all_num)
    # TODO def merchant_ ……
    ##  add more features of merchant



    ##----------------user_merchant feature------------------
    def cal_action_num(self,user_merchant_log):
        # action_type:
        # 0 is for click, 1 is for add-to-cart, 2 is for purchase and 3 is for add-to-favourite.
        click_num = 0
        add_to_cart_num = 0
        purchase_num = 0
        add_to_favourite_num = 0

        for item in user_merchant_log:
            action_type = item[-1]
            if(action_type == "0"):
                click_num += 1
            elif(action_type == "1"):
                add_to_cart_num += 1
            elif(action_type == "2"):
                purchase_num += 1
            elif(action_type == "3"):
                add_to_favourite_num += 1
        return click_num,add_to_cart_num,purchase_num,add_to_favourite_num
    # TODO def merchant_ ……
    ##  add more features of merchant

    def extract_user_feature(self, purchase, fv):
        ## user info
        target_user_info  = self.user_info[purchase.user]
        fv.insert_real_value(self, target_user_info[0], "age_range")
        fv.insert_real_value(self, target_user_info[1], "gender")

        ## user_log
        user_log = self.user_key_dic[purchase.user]
        is_new_user_flag = self.is_new_user(user_log)
        fv.insert_real_value(self, is_new_user_flag, "is_new_user_flag")

    def extract_merchant_feature(self,purchase,fv):
        ## merchant_log
        merchant_log = self.merchant_key_dic[purchase.merchant]
        cal_purchase_11_rate = self.cal_purchase_11_rate(merchant_log)
        fv.insert_real_value(self, cal_purchase_11_rate, "purchase_11_rate")

    def extract_user_merchant_feature(self, purchase, fv):
        ## user_merchant_log
        user_merchant_log = self.user_merchant_key_dic[(purchase.user,purchase.merchant)]
        click_num, add_to_cart_num, purchase_num, add_to_favourite_num = self.cal_action_num(user_merchant_log)
        fv.insert_real_value(self, click_num, "click_num")
        fv.insert_real_value(self, add_to_cart_num, "add_to_cart_num")
        fv.insert_real_value(self, purchase_num, "purchase_num")
        fv.insert_real_value(self, add_to_favourite_num, "add_to_favourite_num")

    def extract_all(self, line):
        fv = base.FeatureVector()
        purchase = base.Purchase(line[0], line[1], line[2])
        self.extract_user_feature(purchase, fv)
        self.extract_merchant_feature(purchase, fv)
        self.extract_user_merchant_feature(purchase, fv)
        return purchase.label, fv

    def extract_fstr(self,line):
        label, fv = self.extract_all(line)
        if label is None:
            return fv.to_str()
        else:
            return "%d %s" % (label, fv.to_str())

if __name__ == "__main__":
    pre_path = os.path.dirname(os.getcwd())
    ##  prepare data
    log_path = pre_path + "/data/user_log_format1.csv"
    user_path = pre_path + "/data/user_info_format1.csv"
    generate_fea = GenerateFeatures()
    generate_fea.gen_dic(log_path,user_path)

    ## generate features
    in_path = pre_path + "/data/train_format.csv"
    out_path = pre_path + "/data/features.csv"
    num_process = 48
    print "Building feature from %s to %s..." % (in_path, out_path)

    with open(in_path) as in_file, \
        open(out_path, 'w') as out_file, \
        open(out_path + "_column_names", 'w') as out_column_file:

        head_line = in_file.readline()

        lines = [line for line in in_file]
        if num_process > 1:
            p = Pool(num_process)
            fvstrs = p.map(generate_fea.extract_fstr, lines)
        else:
            fvstrs = map(generate_fea.extract_fstr, lines)

        for fvstr in fvstrs:
            out_file.write('%s\n' % fvstr)

        for name in head_line:
            out_column_file.write('%s\n' % name)

