# coding=utf-8
from __future__ import unicode_literals
import codecs
import os


weibo_train_feature_dir = os.path.join(os.pardir, os.pardir, 'wb_data', 'feature_data')
weibo_profile_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'source_data', 'WeiboProfile_train.txt')
width_file_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'classify_data', 'weibo_width_classify_data.txt')
depth_file_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'classify_data', 'weibo_depth_classify_data.txt')
weibo_feature_dir = weibo_train_feature_dir

feature_save_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'train_data', 'train_width.txt')


file_list = os.listdir(weibo_feature_dir)
id_feature_dict = dict()

with codecs.open(weibo_profile_path, 'r', 'utf-8') as weibo_profile_file:
    for profile in weibo_profile_file:
        weibo_id = profile.split('\001')[0]
        id_feature_dict[weibo_id] = list()

print len(id_feature_dict)

for file_name in file_list:
    file_path = os.path.join(weibo_train_feature_dir, file_name)
    print file_path
    temp_id_feature_dict = dict()
    length = 0
    with codecs.open(file_path, 'r', 'utf-8') as feature_file:
        for feature_data in feature_file:
            id_feature = feature_data.strip('\n').split('\t')
            weibo_id = id_feature[0]
            feature = id_feature[1].split(',')
            length = len(feature)
            if weibo_id in temp_id_feature_dict:
                temp_id_feature_dict[weibo_id].extend(feature)
            else:
                temp_id_feature_dict[weibo_id] = list()
                temp_id_feature_dict[weibo_id].extend(feature)

    print len(temp_id_feature_dict)

    for weibo_id in id_feature_dict:
        if weibo_id in temp_id_feature_dict:
            id_feature_dict[weibo_id].extend(temp_id_feature_dict[weibo_id])
        else:
            null_list = ['0'] * length
            id_feature_dict[weibo_id].extend(null_list)

with codecs.open(width_file_path, 'r', 'utf-8') as width_file:
        for feature_data in width_file:
            id_feature = feature_data.strip('\n').split('\t')
            weibo_id = id_feature[0]
            label = id_feature[-1]
            id_feature_dict[weibo_id].append(label)

'''
with codecs.open(depth_file_path, 'r', 'utf-8') as depth_file:
        for feature_data in depth_file:
            id_feature = feature_data.strip('\n').split('\t')
            weibo_id = id_feature[0]
            label = id_feature[-1]
            id_feature_dict[weibo_id].append(label)
'''

with codecs.open(feature_save_path, 'w', 'utf-8') as save_file:
    for weibo_id in id_feature_dict:
        if len(id_feature_dict[weibo_id]) == 8:
            save_file.write(str(weibo_id) + ',' + ','.join(id_feature_dict[weibo_id]))
            save_file.write('\n')
        else:
            pass


