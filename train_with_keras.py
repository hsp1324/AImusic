from keras.layers import Dense, LSTM, Dropout, Activation, Input
from keras.models import Model, Sequential
import numpy as np
import Vecterize as vec
from music21 import *
import tensorflow as tf
from fractions import Fraction
import copy

maxlen = 500


summer = converter.parse("Summer_Joe_Hisaishi.mxl")
part0 = summer.getElementsByClass('Part')[0]
vector = vec.vectorize(part0)

origin_length, one_hot_length = vector.shape


output = vec.make_output(vector)

vector = vec.pad_sequences(vector, maxlen=maxlen)
output = vec.pad_sequences(output, maxlen=maxlen)

seq_length, one_hot_length = vector.shape

vector = vector.reshape(1, maxlen, one_hot_length)   #(number of training data, sequence length, one_hot_vector length)

output = output.reshape(1, maxlen, one_hot_length) 




### This is One way

model = Sequential()
model.add(LSTM(256, input_shape=(None, one_hot_length), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(512, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(512, return_sequences=True))
model.add(Dropout(0.1))
model.add(Dense(one_hot_length))
model.add(Activation('softmax'))

model.compile(loss = 'categorical_crossentropy', optimizer='rmsprop')

model.fit(vector, output, nb_epoch=10000, batch_size=1, verbose=2)



# model = Sequential()
# model.add(LSTM(256, input_shape=(maxlen, one_hot_length), return_sequences=True))
# model.add(Dropout(0.3))
# model.add(LSTM(512, return_sequences=True))
# model.add(Dropout(0.3))
# model.add(LSTM(256))
# model.add(Dense(256))
# model.add(Dropout(0.3))
# model.add(Dense(one_hot_length))
# model.add(Activation('softmax'))
# model.compile(loss = 'categorical_crossentropy', optimizer='rmsprop')

# model.fit(vector, output, nb_epoch=100, batch_size=1, verbose=2)

first_note = vector[0, 5]
first_note = first_note.reshape(1, 1, 40)
outcome = model.predict(first_note)
predict_notes = vec.vector_to_note(outcome)
predict_one_hots = vec.output_to_one_hot(outcome.reshape([40])).reshape([1,1,40])



for i in range(6, origin_length):
	print(i, "/", origin_length)
	outcome = model.predict(predict_one_hots)
	predict_note = vec.vector_to_note(outcome[0, -1].reshape(1,1,40))
	predict_notes.extend(predict_note)
	latest_outcomt = outcome[0, -1]
	predict_one_hot = vec.output_to_one_hot(latest_outcomt)
	predict_one_hots = np.append(predict_one_hots[0], predict_one_hot.reshape(1, 40), axis=0)
	len_so_far, no = predict_one_hots.shape
	predict_one_hots = predict_one_hots.reshape(1, len_so_far, 40)




s = stream.Stream()
for i in predict_notes:
	if i.duration.quarterLength not in [Fraction(1,10)]:
		s.append(i)

s.show()
### One way end




# This is  another way from https://blog.keras.io/a-ten-minute-introduction-to-sequence-to-sequence-learning-in-keras.html
# encoder = LSTM(one_hot_length, input_shape=(seq_length,one_hot_length), return_state=True)  # I guess seq_length suppose to be None??
# encoder_inputs = tf.convert_to_tensor(vector, dtype='float32')
# encoder_outputs, state_h, state_c = encoder(encoder_inputs)
# encoder_states = [state_h, state_c]


# decoder_inputs = Input(shape=(None, seq_length))
# decoder_lstm = LSTM(one_hot_length, return_sequences=True, return_state=True)
# decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)
# decoder_dense = Dense(seq_length, activation='softmax')

# model = Model([encoder_inputs, decoder_inputs], decoder_outputs)







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