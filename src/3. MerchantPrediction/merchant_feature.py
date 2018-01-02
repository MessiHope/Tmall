from enum import Enum
import os
import feature

class M(Enum):
    purchased_11_ratio = 1
    repeat_user_ratio = 2
    repeat_user_before_11_ratio = 3
    regular_user_ratio = 4
    clicked_num = 5
    added_to_cart_num = 6
    purchased_num = 7
    faved_num = 8


# ----------------merchant feature------------------

def purchased_11_ratio(merchant_log):
    purchase_11_num = 0
    purchase_all_num = 0
    for item in merchant_log:
        action_type = item[-1] if len(item[-1]) > 0 else None
        if action_type is None:
            continue
        if action_type != '2':
            continue
        time_stamp = item[-2] if len(item[-1]) > 0 else None
        if time_stamp is None:
            continue
        purchase_all_num += 1
        if time_stamp == '1111':
            purchase_11_num += 1
    if purchase_all_num == 0:
        return 0.0
    else:
        return purchase_11_num / float(purchase_all_num)


def repeat_purchased_ratio(merchant_log):
    user2purchase = {}
    total_purchased_num = 0
    for item in merchant_log:
        action_type = item[-1] if len(item[-1]) > 0 else None
        if action_type is None:
            continue
        if action_type != '2':
            continue
        total_purchased_num += 1
        user = int(item[0])
        if user2purchase.get(user) is None:
            user2purchase[user] = []
        else:
            user2purchase[user].append(int(action_type))
    repeat_purchased_num = 0
    for key in user2purchase.keys():
        repeat_purchased_num += len(user2purchase[key]) - 1
    if total_purchased_num == 0:
        return 0.0
    return repeat_purchased_num / float(total_purchased_num)


def repeat_purchased_before_11_ratio(merchant_log):
    user2purchase = {}
    total_purchased_num = 0
    for item in merchant_log:
        action_type = item[-1] if len(item[-1]) > 0 else None
        time_stamp = item[-2] if len(item[-2]) > 0 else None
        if action_type is None or time_stamp is None:
            continue
        if action_type != '2' and time_stamp >= '1111':
            continue
        total_purchased_num += 1
        user = int(item[0])
        if user2purchase.get(user) is None:
            user2purchase[user] = []
        else:
            user2purchase[user].append(int(action_type))
    repeat_purchased_num = 0
    for key in user2purchase.keys():
        repeat_purchased_num += len(user2purchase[key]) - 1
    if total_purchased_num == 0:
        return 0.0
    return repeat_purchased_num / float(total_purchased_num)


def regular_user_ratio(merchant_log):
    user2purchase = {}
    for item in merchant_log:
        action_type = item[-1] if len(item[-1]) > 0 else None
        if action_type is None:
            continue
        if action_type != '2':
            continue
        user = int(item[0])
        if user2purchase.get(user) is None:
            user2purchase[user] = []
        else:
            user2purchase[user].append(int(action_type))
    regular_user_num = 0
    for key in user2purchase.keys():
        if len(user2purchase[key]) >= 2:
            regular_user_num += 1
    if len(user2purchase.keys()) == 0:
        return 0.0
    return regular_user_num / float(len(user2purchase.keys()))

def clicked_num(merchant_log):
    total = 0
    for item in merchant_log:
        action_type = item[-1] if len(item[-1]) > 0 else None
        if action_type is None:
            continue
        if action_type == '0':
            total += 1
    return total


def added_to_cart_num(merchant_log):
    total = 0
    for item in merchant_log:
        action_type = item[-1] if len(item[-1]) > 0 else None
        if action_type is None:
            continue
        if action_type == '1':
            total += 1
    return total


def purchased_num(merchant_log):
    total = 0
    for item in merchant_log:
        action_type = item[-1] if len(item[-1]) > 0 else None
        if action_type is None:
            continue
        if action_type == '2':
            total += 1
    return total


def faved_num(merchant_log):
    total = 0
    for item in merchant_log:
        action_type = item[-1] if len(item[-1]) > 0 else None
        if action_type is None:
            continue
        if action_type == '2':
            total += 1
    return total


# TODO merchant
#  add more features of merchant


if __name__ == "__main__":
    # todo the following code is just for test
    pre_path = os.path.dirname(os.getcwd())
    ##  prepare data
    user_dic_path = pre_path + "/../data/prepare_data/user_result.csv"
    merchant_dic_path = pre_path + "/../data/prepare_data/merchant_result.csv"
    user_merchant_dic_path = pre_path + "/../data/prepare_data/user_merchant_result.csv"
    user_info_path = pre_path + "/../data/original_data/user_info_format1.csv"
    generate_fea = feature.GenerateFeatures()
    generate_fea.gen_dic(user_dic_path, merchant_dic_path, user_merchant_dic_path, user_info_path)


    merchant_log = generate_fea.merchant_key_dic[1]  # 1 10

    print(purchased_11_ratio(merchant_log))
    print(regular_user_ratio(merchant_log))
    print(clicked_num(merchant_log))
    print(added_to_cart_num(merchant_log))
    print(purchased_num(merchant_log))
    print(faved_num(merchant_log))


