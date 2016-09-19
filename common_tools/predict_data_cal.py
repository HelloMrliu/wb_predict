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
        new_predict_list.append(temp_list[len(temp_list) / 2])
    return new_predict_list
