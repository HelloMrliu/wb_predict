# coding=utf-8
from __future__ import unicode_literals


def del_bad_test_case(weibo_dict, case_set):
    test_dict = dict()
    for weibo_id in case_set:
        test_dict[weibo_id] = weibo_dict[weibo_id]
        weibo_dict.pop(weibo_id)
    return weibo_dict, test_dict