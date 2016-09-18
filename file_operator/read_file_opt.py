# coding=utf-8
from __future__ import unicode_literals
import codecs


def read_file(data_dir):
    result_dict = dict()
    with codecs.open(data_dir, 'r', 'utf-8') as file_data:
        for data in file_data:
            info_list = data.strip('\n').split('\t')
            weibo_id = info_list[0]
            weibo_len_list = info_list[1].split(',')
            result_dict[weibo_id] = weibo_len_list
    return result_dict


def read_case_file(data_dir):
    case_set = set()
    with codecs.open(data_dir, 'r', 'utf-8') as file_data:
        for data in file_data:
            info_list = data.strip('\n').split('\t')
            weibo_id = info_list[0]
            case_set.add(weibo_id)
    return case_set
