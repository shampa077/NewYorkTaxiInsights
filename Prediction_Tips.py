# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 21:20:05 2017

@author: shampa
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from calendar import weekday, day_name
from datetime import datetime
import math
col_names = ['VendorID','tpep_pickup_datetime','tpep_dropoff_datetime','passenger_count','trip_distance','pickup_longitude','pickup_latitude',
	'RatecodeID',
	'store_and_fwd_flag',
	'dropoff_longitude',
	'dropoff_latitude',
	'payment_type',
	'fare_amount',
	'extra',
	'mta_tax',
	'tip_amount',
	'tolls_amount',
	'improvement_surcharge',
	'total_amount',
   'trip_duration',
    'trip_day',
    'trip_hour_start',
    'trip_hour_end']
feature_cols = ['trip_day', 'payment_type','VendorID','passenger_count','trip_distance','pickup_longitude','pickup_latitude',
	'RatecodeID',
	'dropoff_longitude',
	'dropoff_latitude',
	'extra',
	'mta_tax',
	'tolls_amount',
	'improvement_surcharge',
	'total_amount',
   'trip_duration',
    'trip_hour_start',
    'trip_hour_end','fare_amount']

feature_cols = ['trip_day' ,'payment_type','pickup_longitude','pickup_latitude',
	'dropoff_longitude',
	'dropoff_latitude',
    'trip_hour_start',
    'trip_hour_end']

# X is a matrix, hence we use [] to access the features we want in feature_cols
X = datasetNew[feature_cols].values
y = datasetNew['tip_amount'].values

# Encoding categorical data
# Encoding the Independent Variable
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X = LabelEncoder()
X[:,0] = labelencoder_X.fit_transform(X[:,0])
X[:,1] = labelencoder_X.fit_transform(X[:,1])

onehotencoder = OneHotEncoder(categorical_features = [0,1])
#onehotencoder = OneHotEncoder(categorical_features = [0])
X = onehotencoder.fit_transform(X).toarray()

# Avoiding the Dummy Variable Trap
X = X[:, 1:]


# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 0)


# Fitting Multiple Linear Regression to the Training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Predicting the Test set results
y_pred = regressor.predict(X_test)

#The explained_variance_score computes the explained variance regression score.
from sklearn.metrics import explained_variance_score, mean_absolute_error, mean_squared_error,median_absolute_error,r2_score
explained_variance_score(y_test, y_pred)  
mean_squared_error(y_test, y_pred)
median_absolute_error(y_test, y_pred)
r2_score(y_test, y_pred) 

value=[]
for i in range(0,len(y_pred)):
    value.append(int(i))

# Visualising the Test set results
plt.cla()
plt.scatter(value, y_test, color = 'blue',label='original tips')
#plt.plot(value, valueDumy, color = 'black',label='original sell')
plt.scatter(value, y_pred, color = 'red',label='predicted tips')
plt.title('Tips Predict')
plt.xlabel('Index')
plt.ylabel('Tips')
legend = plt.legend(loc='upper left', shadow=True)
plt.show()