# coding=utf-8
from __future__ import unicode_literals
import codecs
from file_operator import read_file_opt
from common_tools import error_calculate


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


def get_classify(predict_classify_file_path):
    weibo_classify_dict = read_file_opt.read_classify(predict_classify_file_path)
    return weibo_classify_dict


def select_same_classify(std_weibo_id, same_weibo_id_set, weibo_classify_file_path):
    weibo_classify_dict = dict()
    with codecs.open(weibo_classify_file_path, 'r', 'utf-8') as classify_file:
        for data in classify_file:
            data_list = data.strip('\n').split('\t')
            weibo_id = data_list[0]
            weibo_classify = data_list[1]
            weibo_classify_dict[weibo_id] = weibo_classify

    if std_weibo_id in weibo_classify_dict:
        std_classify = weibo_classify_dict[std_weibo_id]
    else:
        print 'std_id not in same_set'
        return same_weibo_id_set

    new_result_set = set()
    for weibo_id in same_weibo_id_set:
        if weibo_classify_dict[weibo_id] == std_classify:
            new_result_set.add(weibo_id)

    return new_result_set


def select_same_classify_by_the_classifer(std_classify, same_weibo_id_set, weibo_classify_file_path):
    weibo_classify_dict = dict()
    with codecs.open(weibo_classify_file_path, 'r', 'utf-8') as classify_file:
        for data in classify_file:
            data_list = data.strip('\n').split('\t')
            weibo_id = data_list[0]
            weibo_classify = data_list[1]
            weibo_classify_dict[weibo_id] = weibo_classify

    new_result_set = set()
    for weibo_id in same_weibo_id_set:
        if weibo_classify_dict[weibo_id] == std_classify:
            new_result_set.add(weibo_id)

    return new_result_set


def select_same_classify_new(std_id, same_weibo_id_set, weibo_classify_file_path, data_dict, std_list):
    weibo_classify_dict = dict()
    with codecs.open(weibo_classify_file_path, 'r', 'utf-8') as classify_file:
        for data in classify_file:
            data_list = data.strip('\n').split('\t')
            weibo_id = data_list[0]
            weibo_classify = data_list[1]
            weibo_classify_dict[weibo_id] = weibo_classify

    same_classify_dict = dict()
    for weibo_id in same_weibo_id_set:
        if weibo_classify_dict[weibo_id] in same_classify_dict:
            same_classify_dict[weibo_classify_dict[weibo_id]].add(weibo_id)
        else:
            same_classify_dict[weibo_classify_dict[weibo_id]] = set()
            same_classify_dict[weibo_classify_dict[weibo_id]].add(weibo_id)

    min_error = 1000000
    min_classify = 0

    for classify in same_classify_dict:
        same_set = same_classify_dict[classify]
        error = 0
        for same_id in same_set:
            same_list = data_dict[same_id]
            for index in range(4):
                error += abs(int(same_list[index]) - int(std_list[index]))
        if error < min_error:
            min_error = error
            min_classify = classify

    print min_classify + ':' + weibo_classify_dict[std_id]
    new_result_set = set()
    for weibo_id in same_weibo_id_set:
        if weibo_classify_dict[weibo_id] == min_classify:
            new_result_set.add(weibo_id)

    return new_result_set
