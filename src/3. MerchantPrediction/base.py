#!/usr/bin/env python
#coding:utf-8
#@Time: 2017/12/28下午8:31
#@Author: wangximei
#@File: Purchase.py
#@describtion:

import pandas
class Purchase:
    def __init__(self,_user,_merchant,_label):
        self.user = _user
        self.merchant = _merchant
        self.label = _label

class FeatureVector:
    def __init__(self):
        self.idx2data_ = {}
        self.name2idx_ = {}
        self.next_idx_ = 0

    def insert_real_value(self, value, name):
        if name not in self.name2idx_:
            self.name2idx_[name] = self.next_idx_
            self.next_idx_ += 1
            offset = self.name2idx_[name]
            self.idx2data_[offset] = value

    def to_str(self):
        data = sorted(self.idx2data_.items())
        filter_data = filter(lambda x: x[1] is not None, data)
        str_data = map(lambda x: "%d:%s" % (x[0], x[1].__str__()), filter_data)
        return " ".join(str_data)

    def clear_data(self):
        self.idx2data_ = {}

    def column_names(self):
        L = [(idx, name) for name, idx in self.name2idx_.items()]
        names = [x[1] for x in sorted(L)]
        return names
