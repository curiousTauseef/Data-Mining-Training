"""Question 3, 11/23/16, Sajad Azami"""

import pandas as pd
import numpy as np
import re

__author__ = 'sajjadaazami@gmail.com (Sajad Azami)'


# Reads train data from csv, returns pandas DF
def read_train(path):
    data = pd.read_csv(path)
    return data


# Reads train and splits the TIME to HOUR, MINUTE and SECOND
def read_train_split_time():
    data = pd.read_csv('../data_set/data_train.csv')
    time = data.get('TIME')
    data = data.drop('TIME', axis=1)
    hours = []
    minutes = []
    seconds = []
    for i in range(0, len(time)):
        time_str = re.split(':', time[i])
        hours.append(time_str[0])
        minutes.append(time_str[1])
        seconds.append(time_str[2])
    data['HOUR'] = hours
    data['MINUTE'] = minutes
    data['SECOND'] = seconds
    return data


# Reads test data
# default path: '../data_set/data_test.csv'
def read_test(path):
    return pd.read_csv(path)


def get_k_fold_train_test(path):
    data = read_train(path)
    test = data.sample(frac=0.1)
    train = data.sample(frac=1)
    return train, test


# Gets a DF of train data with all frauds duplicated n times in train data
def duplicate_fraudulent(data, n):
    print('Data length before duplication: ', len(data))
    data = data.sort_values('Is Fraud', ascending=False)
    df_temp = pd.DataFrame()
    for index, row in data.iterrows():
        if row['Is Fraud'] == 1:
            df_temp = df_temp.append(row)
        else:
            break
    print('Fraudulent data length: ', len(df_temp))
    for i in range(0, n):
        data = data.append(df_temp)
    print('Data length after duplicating ', n, 'times', len(data))
    return data
