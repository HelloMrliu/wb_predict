# coding=utf-8
from __future__ import unicode_literals
import os
from file_operator import read_file_opt
from common_tools import error_calculate, generate_classify, predict_data_cal, select_data, delete_badcase
import codecs

weibo_width_dir = os.path.join(os.pardir, os.pardir, 'wb_data', 'middle_data', 'weibo_time_width.txt')
weibo_testcase_width_dir = os.path.join(os.pardir, os.pardir, 'wb_data', 'badcase_testcase_data', 'weibo_testcase_width.txt')
weibo_badcase_width_dir = os.path.join(os.pardir, os.pardir, 'wb_data', 'badcase_testcase_data', 'weibo_badcase_width.txt')
weibo_classify_file_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'classify_data', 'weibo_width_classify_data.txt')
predict_classify_file_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'classify_data', 'predict_weibo_width_classify_data.txt')
feature_dir = os.path.join(os.pardir, os.pardir, 'wb_data', 'train_data', 'train_width.txt')

weibo_id_classify = dict()


def select_same_classify(std_weibo_id, same_weibo_id_set, weibo_classify_file_path, data_dict, std_list):
    id_feature_dict = dict()
    with codecs.open(feature_dir, 'r', 'utf-8') as feature_file:
        for feature in feature_file:
            features = feature.strip('\n').split(',')
            weibo_id = features[0]
            feature_one = int(features[1])
            feature_two = int(features[2])
            id_feature_dict[weibo_id] = (feature_one, feature_two)

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
    same_classify_dict = dict()
    for weibo_id in same_weibo_id_set:
        if weibo_classify_dict[weibo_id] == std_classify:
            new_result_set.add(weibo_id)
        if weibo_classify_dict[weibo_id] in same_classify_dict:
            same_classify_dict[weibo_classify_dict[weibo_id]].add(weibo_id)
        else:
            same_classify_dict[weibo_classify_dict[weibo_id]] = set()
            same_classify_dict[weibo_classify_dict[weibo_id]].add(weibo_id)

    feature_list = id_feature_dict[std_weibo_id]

    for classify in same_classify_dict:
        same_set = same_classify_dict[classify]
        error = 0
        for same_id in same_set:
            same_list = id_feature_dict[same_id]
            e1 = abs(same_list[0] - feature_list[0])
            e2 = abs(same_list[1] - feature_list[1])
            if e1 == 0:
                error += 1
            if e2 == 0:
                error += 1
        print str(std_classify) + ' , ' + str(classify) + ': ' + str(error)
    return new_result_set


def select_same_classify_new(std_weibo_id, same_weibo_id_set, weibo_classify_file_path, data_dict, std_list):
    id_feature_dict = dict()
    with codecs.open(feature_dir, 'r', 'utf-8') as feature_file:
        for feature in feature_file:
            features = feature.strip('\n').split(',')
            weibo_id = features[0]
            feature_one = int(features[1])
            feature_two = int(features[2])
            id_feature_dict[weibo_id] = (feature_one, feature_two)


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
            error += error_calculate.error_cal(std_list, same_list)
        if error < min_error:
            min_error = error
            min_classify = classify

    print min_classify
    new_result_set = set()
    for weibo_id in same_weibo_id_set:
        if weibo_classify_dict[weibo_id] == min_classify:
            new_result_set.add(weibo_id)

    return new_result_set


def get_classify_dict(data_dict, test_dict, length, low_gap, high_gap, min_gap, min_num, classify_number, is_small):
    count = 0
    error = 0
    test_dict = select_data.select_testcase_with_con(test_dict, low_gap, high_gap)
    test_number = len(test_dict)
    print test_number

    for test_weibo_id in test_dict:
        test_list = test_dict[test_weibo_id]

        same_weibo_id_set = select_data.get_same_set_according_average_val(data_dict, test_list, min_gap, min_num)
        old_same_weibo_id_set = same_weibo_id_set

        same_weibo_id_set = select_same_classify(test_weibo_id, same_weibo_id_set, weibo_classify_file_path, data_dict, test_list)

        if len(same_weibo_id_set) == 0:
            same_weibo_id_set = old_same_weibo_id_set

        if is_small == 1:
            max_gap, predict_list = predict_data_cal.judge_cal_predict_by_condition_small_val(data_dict, same_weibo_id_set)
        else:
            max_gap, predict_list = predict_data_cal.judge_cal_predict_by_condition_big_val(data_dict, same_weibo_id_set)

        temp_error = error_calculate.error_cal(test_list, predict_list)
        if temp_error > 1.0:
            print str(test_weibo_id) + '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
            error += temp_error
        else:
            error += temp_error

        print str(test_weibo_id) + " : " + str(temp_error) + ' len: ' + str(len(same_weibo_id_set)) + ' gap: ' + str(max_gap) + ' divide: ' +  str(max_gap / len(same_weibo_id_set))

        if count > length:
            break
        count += 1

    print error / count


if __name__ == "__main__":
    width_depth_dict = read_file_opt.read_file(weibo_width_dir)
    test_case_set = read_file_opt.read_case_file(weibo_testcase_width_dir)
    bad_case_set = read_file_opt.read_case_file(weibo_badcase_width_dir)

    width_depth_dict, test_dict = delete_badcase.del_bad_test_case(width_depth_dict, test_case_set)
    width_depth_dict, bad_dict = delete_badcase.del_bad_test_case(width_depth_dict, bad_case_set)

    length = 200
    low_gap = 0
    high_gap = 24
    min_gap = 3
    min_num = 10
    classify_number = 5
    is_small = 1

    get_classify_dict(width_depth_dict, test_dict, length, low_gap, high_gap, min_gap, min_num, classify_number, is_small)

    # 25->  1068/1325  0.23035 平均数
    # 0.750466678034



