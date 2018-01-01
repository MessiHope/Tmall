from enum import Enum


class UM(Enum):
    click_num = 1
    add_to_cart_num = 2
    purchase_num = 3
    add_to_favourite_num = 4
    click_ratio_in11 = 5
    add_to_cart_ratio_in11 = 6
    purchase_ratio_in11 = 7
    add_to_favourite_ratio_in11 = 8

# ----------------user_merchant feature------------------


def cal_action_num(user_merchant_log):
    # action_type:
    # 0 is for click, 1 is for add-to-cart, 2 is for purchase and 3 is for add-to-favourite.
    click_num = 0
    add_to_cart_num = 0
    purchase_num = 0
    add_to_favourite_num = 0

    for item in user_merchant_log:
        action_type = item[-1] if len(item[-1]) > 0 else None
        if action_type is None:
            continue
        if action_type == '0':
            click_num += 1
        elif action_type == '1':
            add_to_cart_num += 1
        elif action_type == '2':
            purchase_num += 1
        elif action_type == '3':
            add_to_favourite_num += 1
    return click_num, add_to_cart_num, purchase_num, add_to_favourite_num


def cal_action_ration_in11(user_merchant_log):
    click_11 = 0
    add_to_cart_11 = 0
    purchase_11 = 0
    add_to_favourite_11 = 0
    click_total = 0
    add_to_cart_total = 0
    purchase_total = 0
    add_to_favourite_total = 0
    for item in user_merchant_log:
        action_type = item[-1] if len(item[-1]) > 0 else None
        time_stamp = item[-2] if len(item[-1]) > 0 else None

        if action_type is None or time_stamp is None:
            continue

        if time_stamp == '1111':
            if action_type == '0':
                click_11 += 1
            elif action_type == '1':
                add_to_cart_11 += 1
            elif action_type == '2':
                purchase_11 += 1
            elif action_type == '3':
                add_to_favourite_11 += 1

        if action_type == '0':
            click_total += 1
        elif action_type == '1':
            add_to_cart_total += 1
        elif action_type == '2':
            purchase_total += 1
        elif action_type == '3':
            add_to_favourite_total += 1
    return click_11 / float(click_total) if click_total > 0 else None, \
           add_to_cart_11 / float(add_to_cart_total) if add_to_cart_total > 0 else None, \
           purchase_11 / float(purchase_total) if purchase_total > 0 else None, \
           add_to_favourite_11 / float(add_to_favourite_total) if add_to_favourite_total > 0 else None


if __name__ == "__main__":
    print("hello")

