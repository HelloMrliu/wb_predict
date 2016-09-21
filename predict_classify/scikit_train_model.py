# coding=utf-8
from __future__ import unicode_literals
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
import codecs


width_train_data_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'train_data', 'train_width.csv')
depth_train_data_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'train_data', 'train_depth.csv')
width_test_data_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'train_data', 'test_width.csv')
depth_test_data_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'train_data', 'test_depth.csv')

width_save_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'classify_data', 'predict_weibo_width_classify_data.txt')
depth_save_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'classify_data', 'predict_weibo_depth_classify_data.txt')
is_width = 1


if is_width == 0:
    data = pd.read_csv(depth_train_data_path)
    test_data = pd.read_csv(depth_test_data_path)
    weight_dict = {
        1: 0.5,
        2: 0.35,
        3: 0.15,
    }
else:
    data = pd.read_csv(width_train_data_path)
    test_data = pd.read_csv(width_test_data_path)
    weight_dict = {
        1: 0.4,
        2: 0.3,
        3: 0.15,
        4: 0.1,
        5: 0.05
    }

train_data, val_data = train_test_split(data, test_size=0.1)

train_id = train_data['Id']
val_id = val_data['Id']
test_id = test_data['Id']

train_x = train_data.drop(['Id', 'label'], axis=1)
train_y = train_data['label']
val_x = val_data.drop(['Id', 'label'], axis=1)
val_y = val_data['label']
test_x = test_data.drop(['Id'], axis=1)

if is_width == 0:
    model = RandomForestClassifier(n_estimators=2000, max_depth=None, min_samples_split=2, class_weight=weight_dict).fit(train_x, train_y)
else:
    model = RandomForestClassifier(n_estimators=1000, max_depth=None, min_samples_split=5, class_weight=weight_dict).fit(train_x, train_y)

'''
test_y = model.predict(test_x)


if is_width == 0:
    save_path = depth_save_path
else:
    save_path = width_save_path
    
with codecs.open(save_path, 'w', 'utf-8') as write_file:
    length = len(test_id)
    for index in range(length):
        write_file.write(str(test_id[index]) + '\t' + str(int(test_y[index])))
        write_file.write('\n')


'''

predict_y = model.predict(val_x)
new_predict_y = list()
for val in predict_y:
    new_predict_y.append(int(val))
test_y = list(val_y)
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

