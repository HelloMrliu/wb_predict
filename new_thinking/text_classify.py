# coding=utf-8
from __future__ import unicode_literals
import os
from file_operator import read_file_opt, write_file_opt
import codecs
import jieba


weibo_train_proflie_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'source_data', 'train_profile.txt')
weibo_classify_file_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'classify_data', 'weibo_width_classify_data.txt')
word_classif_file_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'word_count')

weibo_width_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'middle_data', 'weibo_time_width.txt')
real_weibo_width_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'classify_data', 'weibo_width_classify_data.txt')
'''
profile_dict = dict()
with codecs.open(weibo_train_proflie_path, 'r', 'utf-8') as profile_file:
    for profile in profile_file:
        profile_info = profile.strip('\r\n').split('\001')
        weibo_id = profile_info[0]
        weibo_content = profile_info[3]
        profile_dict[weibo_id] = weibo_content

classify_dict = dict()
with codecs.open(weibo_classify_file_path, 'r', 'utf-8') as classify_file:
    for classify in classify_file:
        classify_info = classify.strip('\n').split('\t')
        weibo_id = classify_info[0]
        weibo_classify = classify_info[1]
        classify_dict[weibo_id] = weibo_classify


file_name = 'word_count_'
for index in range(1, 6):
    id_set = set()
    word_dict = dict()
    for weibo_id in classify_dict:
        if int(classify_dict[weibo_id]) == index:
            id_set.add(weibo_id)
    for weibo_id in id_set:
        text = profile_dict[weibo_id]
        word_list = jieba.cut(text, cut_all=False)
        for word in word_list:
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1
    print len(word_dict)

    word_classif_file = os.path.join(word_classif_file_path, file_name)
    word_classif_file += str(index)
    word_classif_file += '.txt'
    with codecs.open(word_classif_file, 'w', 'utf-8') as write_file:
        for word in word_dict:
            write_file.write(word + '\t' + str(word_dict[word]) + '\n')
'''
weibo_classify_dict = dict()
with codecs.open(weibo_width_path, 'r', 'utf-8') as width_file:
    for width in width_file:
        profile_info = width.strip('\n').split('\t')
        weibo_id = profile_info[0]
        weibo_width = profile_info[1].split(',')
        diff = int(weibo_width[-1]) - int(weibo_width[0])
        classify = 0
        if diff > 900:
            classify = 5
        elif diff > 600:
            classify = 4
        elif diff > 300:
            classify = 3
        elif diff > 100:
            classify = 2
        else:
            classify = 1
        weibo_classify_dict[weibo_id] = classify

real_weibo_classify_dict = dict()
with codecs.open(real_weibo_width_path, 'r', 'utf-8') as width_file:
    for width in width_file:
        profile_info = width.strip('\n').split('\t')
        weibo_id = profile_info[0]
        classify = profile_info[1]
        real_weibo_classify_dict[weibo_id] = classify

count = 0
for weibo_id in real_weibo_classify_dict:
    if weibo_id in weibo_classify_dict:
        if int(real_weibo_classify_dict[weibo_id]) == int(weibo_classify_dict[weibo_id]):
            count += 1

print count
print len(real_weibo_classify_dict)
print len(weibo_classify_dict)