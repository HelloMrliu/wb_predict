# coding=utf-8
from __future__ import unicode_literals


def cal_predict_list(data_dict, same_weibo_id_set):
    predict_list = [0] * 288
    for weibo_id in same_weibo_id_set:
        temp_list = data_dict[weibo_id]
        for index in range(288):
            predict_list[index] += int(temp_list[index])
    for index in range(288):
        predict_list[index] = predict_list[index] / len(same_weibo_id_set)
    return predict_list
