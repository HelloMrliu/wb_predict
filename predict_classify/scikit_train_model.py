# coding=utf-8
from __future__ import unicode_literals
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split


width_train_data_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'train_data', 'width_train.csv')
depth_train_data_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'train_data', 'depth_train.csv')
is_width = 1


if is_width == 1:
    data = pd.read_csv(depth_train_data_path)
    weight_dict = {
        1: 0.5,
        2: 0.35,
        3: 0.15,
    }
else:
    data = pd.read_csv(width_train_data_path)
    weight_dict = {
        1: 0.35,
        2: 0.3,
        3: 0.2,
        4: 0.1,
        5: 0.05
    }

train_data, test_data = train_test_split(data, test_size=0.1)

train_id = train_data['Id']
test_id = test_data['Id']

train_x = train_data.drop(['Id', 'label'], axis=1)
train_y = train_data['label']
test_x = test_data.drop(['Id', 'label'], axis=1)
test_y = test_data['label']

if is_width == 1:
    model = RandomForestClassifier(n_estimators=2000, max_depth=None, min_samples_split=2, class_weight=weight_dict).fit(train_x, train_y)
else:
    model = RandomForestClassifier(n_estimators=2000, max_depth=None, min_samples_split=2, class_weight=weight_dict).fit(train_x, train_y)
predict_y = model.predict(test_x)

new_predict_y = list()
for val in predict_y:
    new_predict_y.append(int(val))
test_y = list(test_y)
length = len(test_y)

good = 0
bad = 0
count = 0
for index in range(length):
    error = new_predict_y[index] - test_y[index]
    if error < 0:
        good += 1
    elif error > 0:
        bad += 1
    else:
        count += 1

print good
print bad
print count
