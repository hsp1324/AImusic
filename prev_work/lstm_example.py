from keras.models import Sequential
from keras.layers import Dense, LSTM
import numpy as np

data = np.array([[i for i in range(100)], [i for i in range(200,300)], [i for i in range(400, 500)]], dtype=float).reshape(3,1,100)
target = np.array([[i for i in range(1,101)], [i for i in range(201,301)], [i for i in range(401,501)]], dtype=float).reshape(3,1,100)
# reshape = (number of training set, height, weight)


x_test = np.array([i for i in range(100,200)], dtype=float).reshape(1,1,100)
y_test = np.array([i for i in range(101,201)], dtype=float).reshape(1,1,100)


model = Sequential()
model.add(LSTM(50, input_shape=(1,100), return_sequences=True))
#input_shape = (height, weight)

model.add(Dropout(0.2))
model.add(Dense(100))
model.add(LSTM(100, input_shape=(1,100), return_sequences=True))
model.add(Dropout(0.2))
model.add(Dense(100))

model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['accuracy'])
model.fit(data, target, nb_epoch=1000, batch_size=1, verbose=2, validation_data=(x_test, y_test))


predict = model.predict(x_test)