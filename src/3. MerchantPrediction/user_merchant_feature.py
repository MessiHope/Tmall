from enum import Enum


class UM(Enum):
    click_num = 1
    add_to_cart_num = 2
    purchase_num = 3
    add_to_favourite_num = 4


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


# TODO def user_merchant
#  add more features of user merchant


if __name__ == "__main__":
    print("hello")

