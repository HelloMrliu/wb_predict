# coding=utf-8
from __future__ import unicode_literals


def get_biggest_diff(data_dict, same_weibo_id_set):
    gap = 0
    for index in range(288):
        val_list = list()
        for weibo_id in same_weibo_id_set:
            temp_list = data_dict[weibo_id]
            val_list.append(int(temp_list[index]))
        val_list = sorted(val_list)
        if val_list[0] == 0:
            gap += 0
        else:
            gap += (int(val_list[-1]) - int(val_list[0]) )/ int(val_list[0])
    return gap


def cal_predict_list(data_dict, same_weibo_id_set):
    predict_list = [0] * 288
    for weibo_id in same_weibo_id_set:
        temp_list = data_dict[weibo_id]
        for index in range(288):
            predict_list[index] += int(temp_list[index])
    for index in range(288):
        predict_list[index] = predict_list[index] / len(same_weibo_id_set)
    return predict_list


def cal_predict_list_by_middle(data_dict, same_weibo_id_set):
    predict_list = list()
    for index in range(288):
        predict_list.append(list())
    for weibo_id in same_weibo_id_set:
        temp_list = data_dict[weibo_id]
        for index in range(288):
            predict_list[index].append(int(temp_list[index]))

    for index in range(288):
        predict_list[index] = sorted(predict_list[index])

    new_predict_list = list()
    for index in range(288):
        temp_list = predict_list[index]
        if len(temp_list) / 2 >= 3:
            new_predict_list.append(temp_list[len(temp_list) / 2 - 3])
        else:
            new_predict_list.append(temp_list[len(temp_list) / 2])
    return new_predict_list


def cal_predict_list_by_small(data_dict, same_weibo_id_set):
    predict_list = list()
    for index in range(288):
        predict_list.append(list())
    for weibo_id in same_weibo_id_set:
        temp_list = data_dict[weibo_id]
        for index in range(288):
            predict_list[index].append(int(temp_list[index]))

    for index in range(288):
        predict_list[index] = sorted(predict_list[index])

    new_predict_list = list()
    for index in range(288):
        temp_list = predict_list[index]
        new_predict_list.append(temp_list[0])

    return new_predict_list


def cal_predict_list_by_diff(data_dict, same_weibo_id_set, divide_area_num):
    predict_list = list()
    for index in range(288):
        predict_list.append(list())
    for weibo_id in same_weibo_id_set:
        temp_list = data_dict[weibo_id]
        for index in range(288):
            predict_list[index].append(int(temp_list[index]))

    for index in range(288):
        predict_list[index] = sorted(predict_list[index])

    new_predict_list = list()
    for index in range(288):
        temp_list = predict_list[index]
        new_predict_list.append(temp_list[0])
    return new_predict_list


def judge_cal_predict_by_condition_small_val(data_dict, same_weibo_id_set):
    max_gap_per = get_biggest_diff(data_dict, same_weibo_id_set)
    if max_gap_per > 7000:
        predict_list = cal_predict_list_by_diff(data_dict, same_weibo_id_set, 10)
    else:
        predict_list = cal_predict_list_by_middle(data_dict, same_weibo_id_set)

    return max_gap_per, predict_list


def judge_cal_predict_by_condition_big_val(data_dict, same_weibo_id_set):
    max_gap_per = get_biggest_diff(data_dict, same_weibo_id_set)
    predict_list = cal_predict_list_by_middle(data_dict, same_weibo_id_set)
    return max_gap_per, predict_list