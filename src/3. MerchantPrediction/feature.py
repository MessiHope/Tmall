#!/usr/bin/env python
#coding:utf-
#@Time: //下午:
#@Author: wangximei
#@File: feature.py
#@describtion:

import os
from multiprocessing import Pool
import base
import csv
import prepare_data
import user_feature
import merchant_feature
import user_merchant_feature


class GenerateFeatures:
    def __init__(self):
        self.user_merchant_key_dic = {}
        self.user_key_dic = {}
        self.merchant_key_dic = {}
        self.user_info = {}

    def read_user_dic(self,user_dic_path):
        user_key_dic = {}
        with open(user_dic_path) as file:
            head_line = next(file)
            lines = csv.reader(file)
            cur_user = None
            for line in lines:
                user = line[0]
                if(user != cur_user):
                    user_key_dic[int(user)] = [line]
                else:
                    pur_list = user_key_dic[int(user)]
                    pur_list.append(line)
                    user_key_dic[int(user)] = pur_list
                cur_user = user
        return user_key_dic

    def read_merchant_dic(self,merchant_dic_path):
        merchant_key_dic = {}
        with open(merchant_dic_path) as file:
            head_line = next(file)
            lines = csv.reader(file)
            cur_merchant = None
            for line in lines:
                merchant = line[3]
                if(merchant != cur_merchant):
                    merchant_key_dic[int(merchant)] = [line]
                else:
                    pur_list = merchant_key_dic[int(merchant)]
                    pur_list.append(line)
                    merchant_key_dic[int(merchant)] = pur_list
                cur_merchant = merchant
        return merchant_key_dic

    def read_user_merchant_dic(self,user_merchant_dic_path):
        user_merchant_key_dic = {}
        with open(user_merchant_dic_path) as file:
            head_line = next(file)
            lines = csv.reader(file)
            cur_user = None
            cur_merchant = None
            for line in lines:
                user = line[0]
                merchant = line[3]
                if user != cur_user or merchant != cur_merchant:
                    user_merchant_key_dic[(int(user), int(merchant))] = [line]
                else:
                    pur_list = user_merchant_key_dic[(int(user), int(merchant))]
                    pur_list.append(line)
                    user_merchant_key_dic[(int(user), int(merchant))] = pur_list
                cur_user = user
                cur_merchant = merchant
        return user_merchant_key_dic

    def gen_dic(self,user_dic_path,merchant_dic_path,user_merchant_dic_path,user_info_path):

        self.user_merchant_key_dic = self.read_user_merchant_dic(user_merchant_dic_path)
        self.user_key_dic = self.read_user_dic(user_dic_path)
        self.merchant_key_dic = self.read_merchant_dic(merchant_dic_path)
        self.user_info = prepare_data.read_user_info(user_info_path)

    # ----------------user_merchant feature------------------
    def cal_action_num(self,user_merchant_log):
        # action_type:
        # 0 is for click, 1 is for add-to-cart, 2 is for purchase and 3 is for add-to-favourite.
        click_num = 0
        add_to_cart_num = 0
        purchase_num = 0
        add_to_favourite_num = 0

        for item in user_merchant_log:
            action_type = item[-1]
            if action_type == "0":
                click_num += 1
            elif action_type == "1":
                add_to_cart_num += 1
            elif action_type == "2":
                purchase_num += 1
            elif action_type == "3":
                add_to_favourite_num += 1
        return click_num,add_to_cart_num,purchase_num,add_to_favourite_num
    # TODO def user_merchant_
    # add more features of user_merchant

    def extract_user_feature(self, purchase, fv):
        # user info
        if self.user_info.__contains__(purchase.user):
            target_user_info = self.user_info[purchase.user]
            age_range = int(target_user_info[0]) if len(target_user_info[0]) > 0 else None
            gender = int(target_user_info[1]) if len(target_user_info[1]) > 0 else None
            fv.insert_real_value(age_range, user_feature.U.age_range.value)
            fv.insert_real_value(gender, user_feature.U.gender.value)

        # user_log
        if self.user_key_dic.__contains__(purchase.user):
            user_log = self.user_key_dic[purchase.user]
            is_new_user_flag = user_feature.is_new_user(user_log)
            fv.insert_real_value(is_new_user_flag, user_feature.U.isNew)

    def extract_merchant_feature(self,purchase, fv):
        # merchant_log
        if not self.merchant_key_dic.__contains__(purchase.merchant):
            return
        merchant_log = self.merchant_key_dic[purchase.merchant]
        cal_purchase_11_rate = merchant_feature.cal_purchase_11_rate(merchant_log)
        fv.insert_real_value(cal_purchase_11_rate, merchant_feature.M.purchased_11_ratio)

    def extract_user_merchant_feature(self, purchase, fv):
        # user_merchant_log
        if not self.user_merchant_key_dic.__contains__((purchase.user, purchase.merchant)):
            return
        user_merchant_log = self.user_merchant_key_dic[(purchase.user, purchase.merchant)]
        click_num, add_to_cart_num, purchase_num, add_to_favourite_num = self.cal_action_num(user_merchant_log)
        fv.insert_real_value(click_num, user_merchant_feature.UM.click_num)
        fv.insert_real_value(add_to_cart_num, user_merchant_feature.UM.add_to_cart_num)
        fv.insert_real_value(purchase_num, user_merchant_feature.UM.purchase_num)
        fv.insert_real_value(add_to_favourite_num, user_merchant_feature.UM.add_to_favourite_num)

    def extract_all(self, line):
        fv = base.FeatureVector()
        purchase = base.Purchase(line[0].split(','))
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
    user_dic_path = pre_path + "/../data/prepare_data/user_result.csv"
    merchant_dic_path = pre_path + "/../data/prepare_data/merchant_result.csv"
    user_merchant_dic_path = pre_path + "/../data/prepare_data/user_merchant_result.csv"
    user_info_path = pre_path + "/../data/original_data/user_info_format1.csv"
    generate_fea = GenerateFeatures()
    generate_fea.gen_dic(user_dic_path,merchant_dic_path,user_merchant_dic_path,user_info_path)

    in_path = pre_path + "/../data/original_data/train_format.csv"
    with open(in_path) as in_file:
        head_line = in_file.readline()
        lines = [line for line in in_file]
        fvstrs = generate_fea.extract_fstr(lines)

    ## generate features
    """
    in_path = pre_path + "/data/original_data/train_format.csv"
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
    """

