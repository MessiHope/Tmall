#!/usr/bin/env python
#coding:utf-8
#@Time: 2017/12/25下午3:40
#@Author: wangximei
#@File: testfpgrowth.py
#@describtion:

import pyfpgrowth
def print_patterns(patterns):
    # print patterns
    for k, v in patterns.items():
        print "pattern: ", k, " support: ", v
def print_rules(rules):
    # print rules
    for k, v in rules.items():
        print k, "-->", v[0], ':  ', v[1]

def filter_patterns(patterns):
    filtered_patterns = {}
    for k, v in patterns.items():
        if(len(k)>1):
            filtered_patterns[k] = v
            print "pattern: ", k, " support: ", v
    return filtered_patterns

def run_fpgrowth(transactions,support_threshold,min_prob):
    patterns = pyfpgrowth.find_frequent_patterns(transactions, support_threshold)
    filtered_patterns = filter_patterns(patterns)
    # print_patterns(patterns)

    rules = pyfpgrowth.generate_association_rules(filtered_patterns, min_prob)
    print_rules(rules)


def gen_dataset():
    transactions = [[1, 2, 5],
                    [2, 4],
                    [2, 3],
                    [1, 2, 4],
                    [1, 3],
                    [2, 3],
                    [1, 3],
                    [1, 2, 3, 5],
                    [1, 2, 3]]
    return transactions

if __name__ == "__main__":
    transactions = gen_dataset()
    support_threshold = 5
    min_prob = 0.9
    run_fpgrowth(transactions, support_threshold, min_prob)



