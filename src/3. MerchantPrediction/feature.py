#!/usr/bin/env python
# coding:utf-
# @Time: //下午:
# @Author: wangximei
# @File: feature.py
# @describtion:

import os
from multiprocessing import Pool
import base
import csv
import prepare_data
import user_feature
import merchant_feature
import user_merchant_feature
import pickle


class GenerateFeatures:
    def __init__(self):
        self.merchant2similar_dic = {}
        self.user_merchant_key_dic = {}
        self.user_key_dic = {}
        self.merchant_key_dic = {}
        self.user_info = {}

    def read_user_dic(self, user_dic_path):
        user_key_dic = {}
        with open(user_dic_path) as file:
            head_line = next(file)
            lines = csv.reader(file)
            cur_user = None
            for line in lines:
                user = line[0]
                if (user != cur_user):
                    user_key_dic[int(user)] = [line]
                else:
                    pur_list = user_key_dic[int(user)]
                    pur_list.append(line)
                    user_key_dic[int(user)] = pur_list
                cur_user = user
        return user_key_dic

    def read_merchant_dic(self, merchant_dic_path):
        merchant_key_dic = {}
        with open(merchant_dic_path) as file:
            head_line = next(file)
            lines = csv.reader(file)
            cur_merchant = None
            for line in lines:
                merchant = line[3]
                if (merchant != cur_merchant):
                    merchant_key_dic[int(merchant)] = [line]
                else:
                    pur_list = merchant_key_dic[int(merchant)]
                    pur_list.append(line)
                    merchant_key_dic[int(merchant)] = pur_list
                cur_merchant = merchant
        return merchant_key_dic

    def read_user_merchant_dic(self, user_merchant_dic_path):
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


    def gen_dic(self, user_dic_path, merchant_dic_path, user_merchant_dic_path, user_info_path, similar_merchant_path):
        f = open(similar_merchant_path, 'rb')
        self.merchant2similar_dic = pickle.load(f)
        self.user_merchant_key_dic = self.read_user_merchant_dic(user_merchant_dic_path)
        self.user_key_dic = self.read_user_dic(user_dic_path)
        self.merchant_key_dic = self.read_merchant_dic(merchant_dic_path)
        self.user_info = prepare_data.read_user_info(user_info_path)


    def extract_user_feature(self, purchase, fv):
        # user info
        if self.user_info.__contains__(purchase.user):
            target_user_info = self.user_info[purchase.user]
            age_range = target_user_info[0] if len(target_user_info[0]) > 0 else None
            gender = target_user_info[1] if len(target_user_info[1]) > 0 else None
            fv.insert_real_value(age_range, user_feature.U.age_range)
            fv.insert_real_value(gender, user_feature.U.gender)

        # user_log
        if self.user_key_dic.__contains__(purchase.user):
            user_log = self.user_key_dic[purchase.user]
            is_new_user_flag = user_feature.is_new_user(user_log)
            repeat_buy_ratio = user_feature.repeat_buy_ratio(user_log)
            repeat_buy_before_11_ratio = user_feature.repeat_buy_before_11_ratio(user_log)
            action_days = user_feature.action_days(user_log)
            daily_action_factor = user_feature.daily_action_factor(user_log)
            click_ratio_in11= user_feature.click_ratio_in11(user_log)
            add_to_cart_ratio_in11= user_feature.add_to_cart_ratio_in11(user_log)
            purchase_ratio_in11 = user_feature.purchase_ratio_in11(user_log)
            fav_ratio_in11 = user_feature.fav_ratio_in11(user_log)
            action_ratio_in11 = user_feature.action_ratio_in11(user_log)

            fv.insert_real_value(is_new_user_flag, user_feature.U.is_new_user)
            fv.insert_real_value(repeat_buy_ratio, user_feature.U.repeat_buy_ratio)
            fv.insert_real_value(repeat_buy_before_11_ratio, user_feature.U.repeat_buy_before_11_ratio)
            fv.insert_real_value(action_days, user_feature.U.action_days)
            fv.insert_real_value(daily_action_factor, user_feature.U.daily_action_factor)
            fv.insert_real_value(click_ratio_in11, user_feature.U.click_ratio_in11)
            fv.insert_real_value(add_to_cart_ratio_in11, user_feature.U.add_to_cart_ratio_in11)
            fv.insert_real_value(purchase_ratio_in11, user_feature.U.purchase_ratio_in11)
            fv.insert_real_value(fav_ratio_in11, user_feature.U.fav_ratio_in11)
            fv.insert_real_value(action_ratio_in11, user_feature.U.action_ratio_in11)

    def extract_merchant_feature(self, purchase, fv):
        # merchant_log
        if not self.merchant_key_dic.__contains__(purchase.merchant):
            return
        merchant_log = self.merchant_key_dic[purchase.merchant]

        purchased_11_ratio = merchant_feature.purchased_11_ratio(merchant_log)
        repeat_user_ratio = merchant_feature.repeat_user_ratio(merchant_log)
        repeat_user_before_11_ratio = merchant_feature.repeat_user_before_11_ratio(merchant_log)
        regular_user_ratio = merchant_feature.regular_user_ratio(merchant_log)
        clicked_num = merchant_feature.clicked_num(merchant_log)
        added_to_cart_num = merchant_feature.added_to_cart_num(merchant_log)
        purchased_num = merchant_feature.purchased_num(merchant_log)
        faved_num = merchant_feature.faved_num(merchant_log)

        fv.insert_real_value(purchased_11_ratio, merchant_feature.M.purchased_11_ratio)
        fv.insert_real_value(repeat_user_ratio, merchant_feature.M.repeat_user_ratio)
        fv.insert_real_value(repeat_user_before_11_ratio, merchant_feature.M.repeat_user_before_11_ratio)
        fv.insert_real_value(regular_user_ratio, merchant_feature.M.regular_user_ratio)
        fv.insert_real_value(clicked_num, merchant_feature.M.clicked_num)
        fv.insert_real_value(added_to_cart_num, merchant_feature.M.added_to_cart_num)
        fv.insert_real_value(purchased_num, merchant_feature.M.purchased_num)
        fv.insert_real_value(faved_num, merchant_feature.M.faved_num)

    def extract_user_merchant_feature(self, purchase, fv):
        # user_merchant_log
        if not self.user_merchant_key_dic.__contains__((purchase.user, purchase.merchant)):
            return
        user_merchant_log = self.user_merchant_key_dic[(purchase.user, purchase.merchant)]
        click_num, add_to_cart_num, purchase_num, add_to_favourite_num = \
            user_merchant_feature.cal_action_num(user_merchant_log, self.merchant2similar_dic)
        click_11,add_to_cart_11,purchase_11,add_to_favourite_11 = \
            user_merchant_feature.cal_action_ration_in11(user_merchant_log)
        fv.insert_real_value(click_num, user_merchant_feature.UM.click_num)
        fv.insert_real_value(add_to_cart_num, user_merchant_feature.UM.add_to_cart_num)
        fv.insert_real_value(purchase_num, user_merchant_feature.UM.purchase_num)
        fv.insert_real_value(add_to_favourite_num, user_merchant_feature.UM.add_to_favourite_num)

        fv.insert_real_value(click_11, user_merchant_feature.UM.click_11)
        fv.insert_real_value(add_to_cart_11, user_merchant_feature.UM.add_to_cart_11)
        fv.insert_real_value(purchase_11, user_merchant_feature.UM.purchase_11)
        fv.insert_real_value(add_to_favourite_11, user_merchant_feature.UM.add_to_favourite_11)

        # similar_merchant_id(similar_set)
        # similar_merchant_num(similar_set)

    def extract_all(self, line):
        fv = base.FeatureVector()
        purchase = base.Purchase(line)
        #self.extract_user_feature(purchase, fv)
        #self.extract_merchant_feature(purchase, fv)
        self.extract_user_merchant_feature(purchase, fv)
        return purchase.label, fv

    def extract_fstr(self, line):
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
    similar_merchant_path = pre_path + "/../data/prepare_data/similar_merchant.txt"
    generate_fea = GenerateFeatures()
    generate_fea.gen_dic(user_dic_path, merchant_dic_path, user_merchant_dic_path, user_info_path, similar_merchant_path)

    in_path = pre_path + "/../data/original_data/train_format1.csv"
    out_path = pre_path + "/../data/features.csv"
    with open(in_path) as in_file, \
        open(out_path, 'w') as out_file, \
        open(out_path.split(".csv")[0] + "_column_names", 'w') as out_column_file:
        headers = in_file.readline()
        lines = csv.reader(in_file)

        head_line = next(lines)
        head_line[0] = "186568"
        head_line[1] = "3467"
        _, head_fv = generate_fea.extract_all(head_line)
        for name in head_fv.column_names():
            out_column_file.write('%s\n' % name)

        for line in lines:
            fvstr = generate_fea.extract_fstr(line)
            out_file.write('%s\n' % fvstr)
            print(fvstr)

