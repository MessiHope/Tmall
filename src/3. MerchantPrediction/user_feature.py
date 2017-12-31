from enum import Enum
import os
import feature


# action_type  is an enumerated type {0, 1, 2, 3},
# where 0 is for click, 1 is for add-to-cart, 2 is
# for purchase and 3 is for add-to-favourite.
class U(Enum):
    age_range = 1
    gender = 2
    is_new_user = 3
    repeat_buy_ratio = 4
    repeat_buy_before_11_ratio = 5
    action_days = 6
    daily_action_factor = 7
    click_ratio_in11 = 8
    add_to_cart_ratio_in11 = 9
    purchase_ratio_in11 = 10
    fav_ratio_in11 = 11


# ----------------user feature------------------


def is_new_user(user_log):
    is_new_user_flag = 0
    for item in user_log:
        time_stamp = item[-2] if len(item[-1]) > 0 else None
        if time_stamp is None:
            continue
        if time_stamp < '1111':
            # 1 represents !is_new_user
            is_new_user_flag = 1
            break
    return is_new_user_flag


def repeat_buy_ratio(user_log):
    merchant_purchased = []
    for item in user_log:
        merchant_id = item[3] if len(item[3]) > 0 else None
        action_type = item[-1] if len(item[-1]) > 0 else None
        if merchant_id is None or action_type is None:
            continue
        if action_type == '2':
            merchant_purchased.append(merchant_id)
    repeat_buy_num = 0
    identity_merchant = set(merchant_purchased)
    for i in identity_merchant:
        if merchant_purchased.count(i) > 1:
            repeat_buy_num = repeat_buy_num + 1
    if merchant_purchased == 0:
        return 0.0
    return repeat_buy_num / float(len(identity_merchant))


def repeat_buy_before_11_ratio(user_log):
    merchant_purchased = []
    for item in user_log:
        merchant_id = item[3] if len(item[3]) > 0 else None
        action_type = item[-1] if len(item[-1]) > 0 else None
        time_stamp = item[-2] if len(item[-2]) > 0 else None
        if merchant_id is None or action_type is None or time_stamp is None:
            continue
        if action_type == '2' and time_stamp < '1111':
            merchant_purchased.append(merchant_id)
    repeat_buy_num = 0
    identity_merchant = set(merchant_purchased)
    for i in identity_merchant:
        if merchant_purchased.count(i) > 1:
            repeat_buy_num = repeat_buy_num + 1
    if merchant_purchased == 0:
        return 0.0
    return repeat_buy_num / float(len(identity_merchant))


def action_days(user_log):
    days = set()
    for item in user_log:
        time_stamp = item[-2] if len(item[-2]) > 0 else None
        if time_stamp is None:
            continue
        days.add(time_stamp)
    return len(days)


def daily_action_factor(user_log):
    # we assign weght by
    # 8 -> purchase, 4-> add_to_cart,
    # 2 -> add_to_favorite, 1-> click
    weight_sum = 0
    for item in user_log:
        action_type = item[-1] if len(item[-1]) > 0 else None
        if action_type is None:
            continue
        tmp = int(action_type)
        sup = tmp
        if tmp == 3: # add-to-favorite action
            sup = 1
        elif tmp == 2: # purchase action
            sup = 3
        elif tmp == 1: # add-to-cart action
            sup = 2
        weight_sum = weight_sum + pow(2, sup)
    return weight_sum


def click_ratio_in11(user_log):
    subtotal = 0
    total = 0
    for item in user_log:
        action_type = item[-1] if len(item[-1]) > 0 else None
        time_stamp = item[-2] if len(item[-2]) > 0 else None
        if time_stamp is None or action_type is None:
            continue
        if action_type == '0' and time_stamp < '1111':
            subtotal = subtotal + 1
        elif action_type == '0':
            total = total + 1
    return subtotal / float(total) if total > 0 else 0.0


def add_to_cart_ratio_in11(user_log):
    subtotal = 0
    total = 0
    for item in user_log:
        action_type = item[-1] if len(item[-1]) > 0 else None
        time_stamp = item[-2] if len(item[-2]) > 0 else None
        if time_stamp is None or action_type is None:
            continue
        if action_type == '1' and time_stamp < '1111':
            subtotal = subtotal + 1
        elif action_type == '1':
            total = total + 1
    return subtotal / float(total) if total > 0 else 0.0


def purchase_ratio_in11(user_log):
    subtotal = 0
    total = 0
    for item in user_log:
        action_type = item[-1] if len(item[-1]) > 0 else None
        time_stamp = item[-2] if len(item[-2]) > 0 else None
        if time_stamp is None or action_type is None:
            continue
        if action_type == '2' and time_stamp < '1111':
            subtotal = subtotal + 1
        elif action_type == '2':
            total = total + 1
    return subtotal / float(total) if total > 0 else 0.0


def fav_ratio_in11(user_log):
    subtotal = 0
    total = 0
    for item in user_log:
        action_type = item[-1] if len(item[-1]) > 0 else None
        time_stamp = item[-2] if len(item[-2]) > 0 else None
        if time_stamp is None or action_type is None:
            continue
        if action_type == '3' and time_stamp < '1111':
            subtotal = subtotal + 1
        elif action_type == '3':
            total = total + 1
    return subtotal / float(total) if total > 0 else 0.0


def action_ratio_in11(user_log):
    subtotal = 0
    total = 0
    for item in user_log:
        action_type = item[-1] if len(item[-1]) > 0 else None
        time_stamp = item[-2] if len(item[-2]) > 0 else None
        if time_stamp is None or action_type is None:
            continue
        if time_stamp < '1111':
            subtotal = subtotal + 1
        else:
            total = total + 1
    return subtotal / float(total) if total > 0 else 0.0
# TODO def user
# add more features of user


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

    user_log = generate_fea.user_key_dic[122882]  # 122882 270336
    print(is_new_user(user_log))
    print(repeat_buy_ratio(user_log))
    print(repeat_buy_before_11_ratio(user_log))
    print(action_days(user_log))
    print(daily_action_factor(user_log))
    print(click_ratio_in11(user_log))
    print(add_to_cart_ratio_in11(user_log))
    print(purchase_ratio_in11(user_log))
    print(fav_ratio_in11(user_log))
    print(action_ratio_in11(user_log))

