from enum import Enum


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
        time_stamp = item[-2]
        if time_stamp < "1111":
            is_new_user_flag = 1
            break
    return is_new_user_flag

def repeat_buy_ratio(user_log):


# TODO def user
# add more features of user


if __name__ == "__main__":
    print("hello")