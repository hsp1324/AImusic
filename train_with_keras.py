from keras.layers import Dense, LSTM, Dropout, Activation
from keras.models import Sequential
import numpy as np
import Vecterize as vec
from music21 import *
import tensorflow as tf
from fractions import Fraction

summer = converter.parse("Summer_Joe_Hisaishi.mxl")
part0 = summer.getElementsByClass('Part')[0]
vector0 = vec.vectorize(part0)

vector = np.transpose(vector0)
vec_height, vec_weight = vector.shape

vector = vector.reshape(1, vec_height, vec_weight)   #(number of training data, sequence length, one_hot_vector length)



model = Sequential()
model.add(LSTM(vec_weight, input_shape=(vec_height,vec_weight), return_sequences=True))
model.add(Dropout(0.2))
model.add(Dense(vec_weight))
model.add(Activation('softmax'))

model.compile(loss = 'categorical_crossentropy', optimizer='rmsprop')

model.fit(vector, vector, nb_epoch=100, batch_size=1, verbose=2)

predict = model.predict(vector)

predict_notes = vec.vector_to_note(predict)

s = stream.Stream()
for i in predict_notes:
	if i.duration.quarterLength not in [Fraction(1,10)]:
		s.append(i)

#s.show()



# hidden_size = 500

# num_of_notes = len(vector0)  # 481
# hot_vec_len = len(vector0[0])

# model = Sequential()
# model.add(LSTM(hot_vec_len, return_sequences=True))
# model.add(Dropout(0.2))
# model.add(LSTM(hot_vec_len, return_sequences=False))
# model.add(Dropout(0.2))
# model.add(Dense(hot_vec_len))
# model.add(Activation('softmax'))

# model.compile(loss = 'categorical_crossentropy', optimizer='rmsprop')