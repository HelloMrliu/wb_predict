# coding=utf-8
from __future__ import unicode_literals
import xgboost as xgb
import pandas as pd
import os


train_data_path = os.path.join(os.pardir, os.pardir, 'wb_data', 'train_data', 'data.csv')
param = {
    'max_depth':4,
    'eta':0.1,
    'silent':1,
    'objective':'multi:softmax',
    'num_class':4,
    'nthread':1
}

data = pd.read_csv(train_data_path)

Id = data['ID']
y = data['VAL']
x = data.drop(['ID', 'VAL'], axis=1)

data = xgb.DMatrix(data, label=y)

bst = xgb.train(param, data, 100)




