from _typeshed import SupportsAnyComparison
import numpy as np

import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

#Turorial following: https://www.youtube.com/watch?v=4rG8IsKdC3U

data = [[]] #read the data from the csv time series and divide them in vectors of inputs
target = [[]] #se here all the outputs we want, so heating, cooling, electricity 
data = np.array(data)
target = np.array(target)

#now the reshaping
data = data.reshape(()) # (len(target, 1, len(variable_used)))
target = target.reshape(())

model = Sequential()
model.add(LSTM( ,input_shape = (), return_sequence = True)) #first field
model.add(Dense())
model.compile(loss = 'mean_absolute_error', optimizer = 'adam', metrics = ['accuracy'])
model.fit(data, target, np_epochs = 10000, batch_size = 1, verbose = 2, validation_data = ())

prediction = model.predict()

#also this can be useful
#https://machinelearningmastery.com/how-to-develop-lstm-models-for-multi-step-time-series-forecasting-of-household-power-consumption/

#this is the one suggested by davide
model = Sequential()
model.add(LSTM(units=100,
              return_sequences=True,
              input_shape=(None, num_x_signals,)))
model.add(Dropout(0.2))
model.add(Bidirectional(LSTM(units=80,return_sequences=True)))
model.add(Dropout(0.2))
model.add(Dense(num_y_signals, activation='sigmoid'))
#which is very similar to: https://towardsdatascience.com/machine-learning-recurrent-neural-networks-and-long-short-term-memory-lstm-python-keras-example-86001ceaaebc