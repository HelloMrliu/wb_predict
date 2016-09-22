# coding=utf-8
from __future__ import unicode_literals
import os
from file_operator import read_file_opt, write_file_opt
from common_tools import error_calculate, generate_classify, predict_data_cal, select_data, delete_badcase
import codecs


weibo_width_dir = os.path.join(os.pardir, os.pardir, 'wb_data', 'middle_data', 'weibo_time_width.txt')
weibo_testcase_width_dir = os.path.join(os.pardir, os.pardir, 'wb_data', 'badcase_testcase_data', 'weibo_testcase_width.txt')
weibo_badcase_width_dir = os.path.join(os.pardir, os.pardir, 'wb_data', 'badcase_testcase_data', 'weibo_badcase_width.txt')
weibo_classify_file_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'classify_data', 'weibo_width_classify_data.txt')
predict_classify_file_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'classify_data', 'predict_weibo_width_classify_data.txt')

feature_dir = os.path.join(os.pardir, os.pardir, 'wb_data', 'train_data', 'train_width.txt')
weibo_id_classify = dict()


def select_same_classify(std_id, std_list, same_weibo_id_set, data_dict):
    id_feature_dict = dict()
    with codecs.open(feature_dir, 'r', 'utf-8') as feature_file:
        for feature in feature_file:
            features = feature.strip('\n').split(',')
            weibo_id = features[0]
            feature_one = int(features[1])
            feature_two = int(features[2])
            id_feature_dict[weibo_id] = (feature_one, feature_two)

    for same_id in same_weibo_id_set:
        same_list = data_dict[same_id]
        error = 0
        for other_id in same_weibo_id_set:
            other_list = data_dict[other_id]
            temp_error = error_calculate.error_cal(same_list, other_list)
            error += temp_error
        print same_id + ' , ' + str(error)


    std_feature = id_feature_dict[std_id]

    new_result_set = set()
    for same_id in same_weibo_id_set:
        same_feature = id_feature_dict[same_id]
        same_list = data_dict[same_id]
        temp_error = error_calculate.error_cal(std_list, same_list)
        e1 = abs(same_feature[0] - std_feature[0])
        e2 = abs(same_feature[1] - std_feature[1])
        if e1 == 0 or e2 == 0:
            if e1 <= 1 and e2 <= 1:
                new_result_set.add(same_id)
        print same_id + ':' + str(abs(same_feature[0] - std_feature[0])) + ' , ' + str(abs(same_feature[1] - std_feature[1])) + ' , ' + str(temp_error)

    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    return same_weibo_id_set


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

        same_weibo_id_set = select_same_classify(test_weibo_id, test_list, same_weibo_id_set, data_dict)

        if len(same_weibo_id_set) == 0:
            same_weibo_id_set = old_same_weibo_id_set

        if is_small == 1:
            max_gap, predict_list = predict_data_cal.judge_cal_predict_by_condition_small_val(data_dict, same_weibo_id_set)
        else:
            max_gap, predict_list = predict_data_cal.judge_cal_predict_by_condition_big_val(data_dict, same_weibo_id_set)

        temp_error = error_calculate.error_cal(test_list, predict_list)
        if temp_error > 1.0:
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

    length = 10
    low_gap = 25
    high_gap = 25000
    min_gap = 3
    min_num = 10
    classify_number = 5
    is_small = 0

    get_classify_dict(width_depth_dict, test_dict, length, low_gap, high_gap, min_gap, min_num, classify_number, is_small)
