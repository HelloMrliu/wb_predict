# coding=utf-8
from __future__ import unicode_literals
import os
from file_operator import read_file_opt, write_file_opt
from common_tools import error_calculate, generate_classify, predict_data_cal, select_data, delete_badcase

weibo_width_dir = os.path.join(os.pardir, os.pardir, 'wb_data', 'middle_data', 'weibo_time_width.txt')
weibo_testcase_width_dir = os.path.join(os.pardir, os.pardir, 'wb_data', 'badcase_testcase_data', 'weibo_testcase_width.txt')
weibo_badcase_width_dir = os.path.join(os.pardir, os.pardir, 'wb_data', 'badcase_testcase_data', 'weibo_badcase_width.txt')
weibo_classify_file_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'classify_data', 'weibo_width_classify_data.txt')
predict_classify_file_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'classify_data', 'predict_weibo_width_classify_data.txt')
weibo_id_classify = dict()


def get_classify_dict(data_dict, test_dict, length, low_gap, high_gap, min_gap, min_num, classify_number, is_small):
    count = 0
    error = 0

    test_dict = select_data.select_testcase_with_con(test_dict, low_gap, high_gap)
    test_classify_dict = generate_classify.get_classify(predict_classify_file_path)

    test_number = len(test_dict)
    print test_number

    for test_weibo_id in test_dict:
        test_list = test_dict[test_weibo_id]

        same_weibo_id_set = select_data.get_same_set_according_average_val(data_dict, test_list, min_gap, min_num)
        old_same_weibo_id_set = same_weibo_id_set

        same_weibo_id_set = generate_classify.select_same_classify_by_the_classifer(test_classify_dict[test_weibo_id], same_weibo_id_set, weibo_classify_file_path)
        #same_weibo_id_set = generate_classify.select_same_classify(test_weibo_id, same_weibo_id_set, weibo_classify_file_path)

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

    length = 100
    low_gap = 0
    high_gap = 24
    min_gap = 3
    min_num = 10
    classify_number = 5
    is_small = 1

    get_classify_dict(width_depth_dict, test_dict, length, low_gap, high_gap, min_gap, min_num, classify_number, is_small)

    # 25->  1068/1325  0.23035 平均数
    # 0.750466678034



