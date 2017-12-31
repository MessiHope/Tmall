from enum import Enum


class M(Enum):
    purchased_11_ratio = 1
    repeat_user_ratio = 2
    repeat_user_before_11_ratio = 3
    regular_user_ratio = 4
    clicked_num = 5
    faved_num = 6
    added_to_cart_num = 7
    purchased_num = 8


# ----------------merchant feature------------------

def cal_purchase_11_rate(merchant_log):
    purchase_11_num = 0
    purchase_all_num = 0
    for item in merchant_log:
        action_type = item[-1]
        if action_type != "2":
            continue
        time_stamp = item[-2]
        purchase_all_num += 1
        if time_stamp == "1111":
            purchase_11_num += 1
    if purchase_all_num == 0:
        return 0.0
    else:
        return purchase_11_num / float(purchase_all_num)


# TODO def merchant_
#  add more features of merchant


if __name__ == "__main__":
    print("hello")

