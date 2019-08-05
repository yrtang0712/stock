import pandas as pd
import numpy as np
from load_data import get_data

import keras.backend.tensorflow_backend as ktf
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.optimizers import Adam
import tensorflow as tf
from keras.callbacks import EarlyStopping

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)
ktf.set_session(session)

model = Sequential()
model.add(LSTM(256,return_sequences=True, input_shape=(735, 10))
model.add(LSTM(256))
model.add(Dense(1))

early_stopping = EarlyStopping('loss', 0.0001, 5)
model.compile(loss='mse', optimizer=Adam(1e-4))

p = []
for i in range(0, 66, 5):
    x_train, y_train, x_test, y_test = get_data(i)

    model.fit(x_train, y_train, batch_size=256, epochs=100, callbacks=[early_stopping])

    y_pred = model.predict(x_test, batch_size=500)

    r = pd.DataFrame({'change': y_test.flatten(), 'pred': y_pred.flatten()})

    for j in range(3):
        p.append(r[j::3].corr().values[0, 1])

    df = pd.DataFrame({'p': np.array(p)})
    df.to_csv('result.csv')
