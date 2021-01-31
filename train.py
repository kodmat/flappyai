from tensorflow.python import keras
from tensorflow.python.keras.layers import Dense, Dropout
import tensorflow
import numpy as np

x_train = np.load('datas.npy').reshape(-1, 10)
y_train = np.load('outs.npy').reshape(-1,)

y1 = [i for i in range(len(y_train)) if y_train[i] == 1]
y0 = [i for i in range(len(y_train)) if y_train[i] == 0]
y0 = y0[:len(y0):len(y0) // len(y1)]


x_train = np.concatenate((x_train[y1],x_train[y0]))
y_train = np.concatenate((y_train[y1],y_train[y0])).reshape(-1,)

model = tensorflow.keras.models.Sequential()


model.add(Dense(1024, activation='relu', input_shape=(10,)))
model.add(Dropout(0.3))
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(1, activation='sigmoid'))

adam = keras.optimizers.Adam(lr=0.00001)
model.compile(loss='binary_crossentropy', optimizer=adam, metrics=['accuracy'])

model.summary()

model.fit(x_train, y_train, epochs=95, batch_size= 80)

model.save("model.h5")


import play