#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 14:18:44 2021

@author: sandeep
"""
# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# importing the dataset
dataset = pd.read_csv('Churn_Modelling.csv')
X = dataset.iloc[:,3:13]
y = dataset.iloc[:,13]


# Create dummy variables
geography = pd.get_dummies(X['Geography'],drop_first=True)
gender = pd.get_dummies(X['Gender'],drop_first=True)


## Concatente the data frames

X = pd.concat([X,geography,gender],axis = 1)


## Drop Unnecessary columns

X = X.drop(['Geography','Gender'],axis = 1)

# Splitting the data into the Training set and Test set

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.2,random_state = 0)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

## It's time to make ANN
# Importing the keras libraries and Packages

import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout

# initialising the ANN
classifier = Sequential()

# Adding the Input Layer And the first hidden layer
classifier.add(Dense(units = 6,kernel_initializer = 'he_uniform',activation='relu',input_dim = 11))
classifier.add(Dense(units = 6,kernel_initializer = 'he_uniform',activation='relu'))
classifier.add(Dense(units = 1,kernel_initializer='glorot_uniform',activation = 'sigmoid'))

# compling the ANN
classifier.compile(optimizer = 'Adamax',loss = 'binary_crossentropy',metrics=['accuracy'])

# Fitting the ANN to the Training set

model_history=classifier.fit(X_train, y_train,validation_split=0.33, batch_size = 10, nb_epoch = 100)



# Predicting the Test set results
y_pred = classifier.predict(X_test)
y_pred = (y_pred > 0.5)


# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

# Calculate the Accuracy
from sklearn.metrics import accuracy_score
score=accuracy_score(y_pred,y_test)