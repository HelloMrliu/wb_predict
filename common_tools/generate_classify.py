# coding=utf-8
from __future__ import unicode_literals


def make_classify(standard_list, predict_list, same_weibo_id_set, data_dict, weibo_id_classify, classify_number):
    dis_value_list = list()
    for same_id in same_weibo_id_set:
        if same_id in data_dict:
            temp_list = data_dict[same_id]
        else:
            temp_list = standard_list

        temp_dis = 0
        for index in range(288):
            temp_dis += int(temp_list[index]) - int(predict_list[index])
        dis_value_list.append(temp_dis)

    sorted_list = sorted(dis_value_list)
    sorted_list_length = len(sorted_list)

    for same_id in same_weibo_id_set:
        if same_id in data_dict:
            temp_list = data_dict[same_id]
        else:
            temp_list = standard_list

        temp_dis = 0
        for index in range(288):
            temp_dis += int(temp_list[index]) - int(predict_list[index])

        gap = sorted_list_length / classify_number
        classify = 1
        index_gap = gap * classify

        while temp_dis > sorted_list[index_gap]:
            classify += 1
            if classify >= classify_number:
                break
            index_gap += gap

        if same_id in weibo_id_classify:
            weibo_id_classify[same_id].append(classify)
        else:
            weibo_id_classify[same_id] = list()
            weibo_id_classify[same_id].append(classify)

