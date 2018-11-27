from keras.layers import Dense, LSTM, Dropout, Activation, Input
from keras.models import Model, Sequential, load_model
from keras.optimizers import RMSprop
import numpy as np
import Vecterize as vec
from music21 import *
import tensorflow as tf
from fractions import Fraction
import copy

maxlen = 1000
bundle_size = 30
onehot_size = vec.onehot_size
summer = "Summer_Joe_Hisaishi.mxl"
sparkle = "Sparkle.mxl"
first_love = "First_Love.mxl"
one_summers_day = "One_Summers_Day.mxl"
river_flows_in_you = "River_Flows_In_You.mxl"


# summer = converter.parse(first_love)
# part = summer.getElementsByClass('Part')[0]
# key_ = vec.get_key(part)
# vector = vec.vectorize(part, 2, key_.sharps)



summer_treble_input, summer_treble_output = vec.mxl_to_vector(summer, measure_size=1, bundle_size=bundle_size, maxlen=maxlen, clef="treble")
summer_bass_input, summer_bass_output = vec.mxl_to_vector(summer, measure_size=1, bundle_size=bundle_size, maxlen=maxlen, clef="bass")

first_love_treble_input, first_love_treble_output = vec.mxl_to_vector(first_love, measure_size=1, bundle_size=bundle_size, maxlen=maxlen, clef="treble")
first_love_bass_input, first_love_bass_output = vec.mxl_to_vector(first_love, measure_size=1, bundle_size=bundle_size, maxlen=maxlen, clef="bass")

one_summers_day_treble_input, one_summers_day_treble_output = vec.mxl_to_vector(one_summers_day, measure_size=1, bundle_size=bundle_size, maxlen=maxlen, clef="treble")
one_summers_day_bass_input, one_summers_day_bass_output = vec.mxl_to_vector(one_summers_day, measure_size=1, bundle_size=bundle_size, maxlen=maxlen, clef="bass")

river_flows_in_you_treble_input, river_flows_in_you_treble_output = vec.mxl_to_vector(river_flows_in_you, measure_size=1, bundle_size=bundle_size, maxlen=maxlen, clef="treble")
river_flows_in_you_bass_input, river_flows_in_you_bass_output = vec.mxl_to_vector(river_flows_in_you, measure_size=1, bundle_size=bundle_size, maxlen=maxlen, clef="bass")

# sparkle_treble_input, sparkle_treble_output = vec.mxl_to_vector(sparkle, measure_size=1, maxlen=maxlen, clef="treble")
# sparkle_bass_input, sparkle_bass_output = vec.mxl_to_vector(sparkle, measure_size=1, maxlen=maxlen, clef="bass")


input_ = np.empty(shape=[0, bundle_size, vec.onehot_size])

input_ = np.append(input_, summer_treble_input, axis=0)
input_ = np.append(input_, first_love_treble_input, axis=0)
input_ = np.append(input_, one_summers_day_treble_input, axis=0)
input_ = np.append(input_, river_flows_in_you_treble_input, axis=0)

input_ = np.append(input_, summer_bass_input, axis=0)
input_ = np.append(input_, first_love_bass_input, axis=0)
input_ = np.append(input_, one_summers_day_bass_input, axis=0)
input_ = np.append(input_, river_flows_in_you_bass_input, axis=0)



output_ = np.empty(shape=[0, bundle_size, vec.onehot_size])

output_ = np.append(output_, summer_treble_output, axis=0)
output_ = np.append(output_, first_love_treble_output, axis=0)
output_ = np.append(output_, one_summers_day_treble_output, axis=0)
output_ = np.append(output_, river_flows_in_you_treble_output, axis=0)

output_ = np.append(output_, summer_bass_output, axis=0)
output_ = np.append(output_, first_love_bass_output, axis=0)
output_ = np.append(output_, one_summers_day_bass_output, axis=0)
output_ = np.append(output_, river_flows_in_you_bass_output, axis=0)


# input_ = np.empty([10, maxlen, onehot_size])
# output_ = np.empty([10, maxlen, onehot_size])

# input_[0] = summer_treble_input[0]
# input_[1] = first_love_treble_input[0]
# input_[2] = one_summers_day_treble_input[0]
# input_[3] = river_flows_in_you_treble_input[0]
# input_[4] = sparkle_treble_input[0]
# input_[5] = summer_bass_input[0]
# input_[6] = first_love_bass_input[0]
# input_[7] = one_summers_day_bass_input[0]
# input_[8] = river_flows_in_you_bass_input[0]
# input_[9] = sparkle_bass_input[0]

# output_[0] = summer_treble_output[0]
# output_[1] = first_love_treble_output[0]
# output_[2] = one_summers_day_treble_output[0]
# output_[3] = river_flows_in_you_treble_output[0]
# output_[4] = sparkle_treble_output[0]
# output_[5] = summer_bass_output[0]
# output_[6] = first_love_bass_output[0]
# output_[7] = one_summers_day_bass_output[0]
# output_[8] = river_flows_in_you_bass_output[0]
# output_[9] = sparkle_bass_output[0]


model = Sequential()
model.add(LSTM(256, input_shape=(None, onehot_size), return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(512, return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(256, return_sequences=True))
model.add(Dense(256))
model.add(Dropout(0.3))
model.add(Dense(onehot_size))
model.add(Activation('softmax'))
optimizer = RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=1e-6)
model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
model.fit(input_, output_, nb_epoch=10000, batch_size=10, verbose=2)



predict_notes = vec.generate_music(model, bundle_size=bundle_size)
s = vec.notes_to_stream(predict_notes)
s.show()









# This is  another way from https://blog.keras.io/a-ten-minute-introduction-to-sequence-to-sequence-learning-in-keras.html
# encoder = LSTM(onehot_size, input_shape=(seq_length,onehot_size), return_state=True)  # I guess seq_length suppose to be None??
# encoder_inputs = tf.convert_to_tensor(vector, dtype='float32')
# encoder_outputs, state_h, state_c = encoder(encoder_inputs)
# encoder_states = [state_h, state_c]


# decoder_inputs = Input(shape=(None, seq_length))
# decoder_lstm = LSTM(onehot_size, return_sequences=True, return_state=True)
# decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)
# decoder_dense = Dense(seq_length, activation='softmax')

# model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
