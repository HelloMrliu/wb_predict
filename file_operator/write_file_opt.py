# coding=utf-8
from __future__ import unicode_literals
import codecs


def save_id_classify(save_file_path, weibo_classify_dict):
    with codecs.open(save_file_path, 'w', 'utf-8') as save_file:
        for weibo_id in weibo_classify_dict:
            classify_list = weibo_classify_dict[weibo_id]
            classify_list = sorted(classify_list)
            classify = classify_list[len(classify_list) / 2]
            save_file.write(str(weibo_id) + '\t' + str(classify) + '\n')


def save_id_classify_small(save_file_path, weibo_classify_dict):
    with codecs.open(save_file_path, 'w', 'utf-8') as save_file:
        for weibo_id in weibo_classify_dict:
            classify_list = weibo_classify_dict[weibo_id]
            classify_list = sorted(classify_list)
            classify = classify_list[0]
            save_file.write(str(weibo_id) + '\t' + str(classify) + '\n')