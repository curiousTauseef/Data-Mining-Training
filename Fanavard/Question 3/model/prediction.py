"""DMC16, 11/9/16, Sajad Azami"""

import xgboost as xgb
import pandas as pd

from data_preparation import preprocessing

__author__ = 'sajjadaazami@gmail.com (Sajad Azami)'

# Load the data, using 1/10 of the data as validation
train_df, test_df = preprocessing.get_k_fold_train_test()

print(train_df.info())
print(test_df.info())

feature_columns_to_use = ['PS ID', 'PROVINCE ID', 'COUNTY ID', 'Date', 'AMOUNT']

# Join the features from train and test together before imputing missing values,
# in case their distribution is slightly different
big_X = train_df[feature_columns_to_use].append(test_df[feature_columns_to_use])

# Prepare the inputs for the model
train_X = big_X[0:train_df.shape[0]].as_matrix()
test_X = big_X[train_df.shape[0]::].as_matrix()
train_y = train_df['Is Fraud']

# Learn model
gbm = xgb.XGBClassifier(max_depth=3, n_estimators=300, learning_rate=0.05).fit(train_X, train_y)
predictions = gbm.predict(test_X)

print(predictions)
print(len(predictions))
print(type(predictions))

# Create submission file
submission = pd.DataFrame({'Transaction ID': test_df['Transaction ID'],
                           'Is Fraud': predictions})
submission.to_csv('submission.csv', index=False)
validation_df = test_df.loc[:, [3, 5]]
validation_df.to_csv('validation.csv', index=False)
