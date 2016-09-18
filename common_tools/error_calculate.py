# coding=utf-8
from __future__ import unicode_literals


def error_cal(standard_list, predict_list):
    error = 0.0
    for index in range(288):
        if int(standard_list[index]) == 0:
            error += 0
        else:
            temp_error = float(abs(int(standard_list[index]) - int(predict_list[index]))) / int(standard_list[index])
            error += temp_error
    error /= 288
    return error
