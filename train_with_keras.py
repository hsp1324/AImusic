from keras.layers import Dense, LSTM, Dropout, Activation, Input
from keras.models import Model, Sequential
import numpy as np
import Vecterize as vec
from music21 import *
import tensorflow as tf
from fractions import Fraction
import copy

maxlen = 1000
one_hot_length = 40

summer = "Summer_Joe_Hisaishi.mxl"
sparkle = "Sparkle.mxl"
first_love = "First_Love.mxl"
one_summers_day = "One_Summers_Day.mxl"
river_flows_in_you = "River_Flows_In_You.mxl"



summer_treble_input, summer_treble_output = vec.mxl_to_vector(summer, maxlen=maxlen, clef="treble")
summer_bass_input, summer_bass_output = vec.mxl_to_vector(summer, maxlen=maxlen, clef="bass")

first_love_treble_input, first_love_treble_output = vec.mxl_to_vector(first_love, maxlen=maxlen, clef="treble")
first_love_bass_input, first_love_bass_output = vec.mxl_to_vector(first_love, maxlen=maxlen, clef="bass")

one_summers_day_treble_input, one_summers_day_treble_output = vec.mxl_to_vector(one_summers_day, maxlen=maxlen, clef="treble")
one_summers_day_bass_input, one_summers_day_bass_output = vec.mxl_to_vector(one_summers_day, maxlen=maxlen, clef="bass")

river_flows_in_you_treble_input, river_flows_in_you_treble_output = vec.mxl_to_vector(river_flows_in_you, maxlen=maxlen, clef="treble")
river_flows_in_you_bass_input, river_flows_in_you_bass_output = vec.mxl_to_vector(river_flows_in_you, maxlen=maxlen, clef="bass")

sparkle_treble_input, sparkle_treble_output = vec.mxl_to_vector(sparkle, maxlen=maxlen, clef="treble")
sparkle_bass_input, sparkle_bass_output = vec.mxl_to_vector(sparkle, maxlen=maxlen, clef="bass")





input_ = np.empty([5, maxlen, one_hot_length])
output_ = np.empty([5, maxlen, one_hot_length])


input_[0] = summer_treble_input[0]
input_[1] = first_love_treble_input[0]
input_[2] = one_summers_day_treble_input[0]
input_[3] = river_flows_in_you_treble_input[0]
input_[4] = sparkle_treble_input[0]

output_[0] = summer_treble_output[0]
output_[1] = first_love_treble_output[0]
output_[2] = one_summers_day_treble_output[0]
output_[3] = river_flows_in_you_treble_output[0]
output_[4] = sparkle_treble_output[0]



model = Sequential()
model.add(LSTM(256, input_shape=(None, one_hot_length), return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(512, return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(256, return_sequences=True))
model.add(Dense(256))
model.add(Dropout(0.3))
model.add(Dense(one_hot_length))
model.add(Activation('softmax'))
model.compile(loss = 'categorical_crossentropy', optimizer='rmsprop')
model.fit(input_, output_, nb_epoch=10000, batch_size=2, verbose=2)



first_note = summer_treble_input[0, 5]
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



s = vec.notes_to_stream(predict_notes)
s.show()





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
