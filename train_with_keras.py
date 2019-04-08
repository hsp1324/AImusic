from keras.layers import Dense, LSTM, Dropout, Activation, Input, merge
from keras.models import Model, Sequential, load_model
from keras.optimizers import RMSprop
import numpy as np
import Vecterize as vec
from music21 import *
import tensorflow as tf
from fractions import Fraction
import copy
from os import listdir
from keras.utils import multi_gpu_model


maxlen = 1000
bundle_size = 16
onehot_size = vec.onehot_size
slide_size = 4
score_dir = 'score'
scores = listdir(score_dir)
num_of_scores = len(scores)
# sparkle = "score/Sparkle.mxl"
# first_love = "score/First_Love.mxl"
# one_summers_day = "score/One_Summers_Day.mxl"
# river_flows_in_you = "score/River_Flows_In_You.mxl"


# summer = "score/Summer_Joe_Hisaishi.mxl"
# first_love = converter.parse(first_love)
# part = first_love.getElementsByClass('Part')[0]
# measures = part.getElementsByClass('Measure')
# all_notes = measures[0].recurse().notes
# fmajor = chord.Chord("F A C")
# fmajor.pitchedCommonName
# key_ = vec.get_key(part)
# vector = vec.vectorize(part, 2, key_.sharps)

input_ = np.empty(shape=[0, bundle_size, vec.onehot_size])
output_ = np.empty(shape=[0, bundle_size, vec.onehot_size])

sum_input_size = 0

for score_name in scores:
  # if sum_input_size == 3:
  #   sum_input_size += 1
  #   continue
  # if sum_input_size == 1:
  #   break
  print(score_name)
  # file_name = "score/First_Love.mxl"
  file_name = score_dir + '/' + score_name
  treble_input, treble_output = vec.mxl_to_vector(file_name, measure_size=1, bundle_size=bundle_size, slide_size=slide_size, maxlen=maxlen, clef="treble")
  # bass_input, bass_output = vec.mxl_to_vector(file_name, measure_size=1, bundle_size=bundle_size, slide_size=slide_size, maxlen=maxlen, clef="bass")
  print("len(treble_input): ", len(treble_input))
  input_ = np.append(input_, treble_input, axis=0)
  print("len(input_): ", len(input_))
  # input_ = np.append(input_, bass_input, axis=0)
  output_ = np.append(output_, treble_output, axis=0)
  # output_ = np.append(output_, bass_output, axis=0)
  print("treble_input.shape: ", treble_input.shape)
  sum_input_size += 1
  print()

print("input_.shape: ", input_.shape)

model = Sequential()
model.add(LSTM(256, input_shape=(None, onehot_size), return_sequences=True))
model.add(Dropout(0.3))
model.add(Dense(256))
model.add(Dropout(0.3))
model.add(LSTM(512, return_sequences=True))
model.add(Dropout(0.3))
model.add(Dense(256))
model.add(Dropout(0.3))
model.add(LSTM(512, return_sequences=True))
model.add(Dense(256))
model.add(Dropout(0.3))
model.add(Dense(onehot_size))
model.add(Activation('softmax'))
optimizer = RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=1e-6)
# treble_model = multi_gpu_model(treble_model, gpus=4)

model.compile(loss='categorical_crossentropy', optimizer=optimizer)
model.fit(input_, output_, nb_epoch=100000, batch_size=num_of_scores, verbose=2)





predict_notes = vec.generate_music(model, bundle_size=5)
s = vec.notes_to_stream(predict_notes)
s.show()



# sample_index = 3

# a = treble_input[sample_index]
# a = a.reshape([1, bundle_size, onehot_size])
# s = vec.vector_to_stream(a)
# s.show()

# a = treble_output[sample_index]
# a = a.reshape([1, bundle_size, onehot_size])
# s = vec.vector_to_stream(a)
# s.show()