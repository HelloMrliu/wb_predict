# coding=utf-8
from __future__ import unicode_literals
import xgboost as xgb
import pandas as pd
import os
from sklearn.cross_validation import train_test_split


width_train_data_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'train_data', 'width_train.csv')

param = {
    'max_depth':7,
    'eta':0.05,
    'silent':1,
    'objective':'multi:softmax',
    'num_class':6,
    'nthread':5
}

data = pd.read_csv(width_train_data_path)

train_data, test_data = train_test_split(data, test_size=0.1)

train_id = train_data['Id']
test_id = test_data['Id']

train_x = train_data.drop(['Id', 'label'], axis=1)
train_y = train_data['label']
test_x = test_data.drop(['Id', 'label'], axis=1)
test_y = test_data['label']


train_matrix = xgb.DMatrix(train_x, label=train_y)
test_matrix = xgb.DMatrix(test_x, label=test_y)

watchlist = [(train_matrix,'train'),(test_matrix,'val')]

model = xgb.train(param, train_matrix, num_boost_round=1000, evals=watchlist)

result = model.predict(test_matrix)

print list(test_y)
new_result = list()
for val in result:
    new_result.append(int(val))
print new_result


