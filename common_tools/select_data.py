# coding=utf-8
from __future__ import unicode_literals


def select_testcase_with_con(test_dict, low_val, high_val):
    result_dict = dict()
    for test_weibo_id in test_dict:
        test_list = test_dict[test_weibo_id]
        number = 0
        for index in range(4):
            number += int(test_list[index])
        if number >= low_val and number < high_val:
            result_dict[test_weibo_id] = test_list
    return result_dict


def get_same_set_according_average_val(data_dict, test_list, gap, min_num):
    same_weibo_id_set = set()
    while len(same_weibo_id_set) < min_num:
        same_weibo_id_set = set()
        for weibo_id in data_dict:
            value = 0
            data_list = data_dict[weibo_id]
            for index in range(4):
                temp_val = abs(int(test_list[index]) - int(data_list[index]))
                value += temp_val

            if value < gap:
                same_weibo_id_set.add(weibo_id)
        gap += 1
    return same_weibo_id_set


def get_same_set_according_diff_val(data_dict, test_list, gap, min_num):
    same_weibo_id_set = set()
    while len(same_weibo_id_set) < min_num:
        same_weibo_id_set = set()
        for weibo_id in data_dict:
            count = 0
            data_list = data_dict[weibo_id]
            for index in range(4):
                temp_val = abs(int(test_list[index]) - int(data_list[index]))
                if temp_val == 0:
                    count += 1

            if count >= gap:
                same_weibo_id_set.add(weibo_id)
        gap -= 1
    return same_weibo_id_set
