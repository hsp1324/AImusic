# $ source activate tensorflow  // in Mac
# $ activate tensorflow  // in my window7
# copy All and paste in python3.6 instead execute python3 train_with_keras,
# becasue you want to generate music in the middle of training and retrain without losing data


from keras.layers import Dense, LSTM, Dropout, Activation, Input, merge
from keras.models import Model, Sequential, load_model
from keras.optimizers import RMSprop
import numpy as np
import Vectorize as vec
import music21
import tensorflow as tf
from fractions import Fraction
import copy
from os import listdir
from keras.utils import multi_gpu_model
from keras.callbacks import ModelCheckpoint


maxlen = 1000
bundle_size = 10
measure_bundle_size = 8
onehot_size = vec.onehot_size
slide_size = 1
score_dir = 'score'
scores = listdir(score_dir)
num_of_scores = len(scores)

print("num_of_scores: ", num_of_scores)

# sparkle = "score/Sparkle.mxl"
# first_love = "score/First_Love.mxl"
# one_summers_day = "score/One_Summers_Day.mxl"
# river = "score/River_Flows_In_You.mxl"


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

measures_input_ = np.empty(shape=[0, measure_bundle_size, vec.number_of_names])
measures_output_ = np.empty(shape=[0, measure_bundle_size, vec.number_of_names])

index = 0



for score_name in scores:
  print(index, "/", len(scores), "  ", score_name)
  if score_name[-4:] != '.mxl':
    print("Invalid Score")
    print()
    index += 1
    continue
  file_name = score_dir + '/' + score_name
  note_input, note_output, measure_input, measure_output = vec.mxl_to_vector(file_name, measure_size=1, bundle_size=bundle_size, slide_size=slide_size, clef="treble")
  input_ = np.append(input_, note_input, axis=0)
  output_ = np.append(output_, note_output, axis=0)
  measures_input_ = np.append(measures_input_, measure_input, axis=0)
  measures_output_ = np.append(measures_output_, measure_output, axis=0)
  index += 1
  print("note_input / accum_note:", len(note_input), "/", len(input_))
  print("measure_input / accum_measure:", len(measure_input), "/", len(measures_input_))
  print()


np.save("input_output/input_"+str(num_of_scores)+"_songs", input_)
np.save("input_output/output_"+str(num_of_scores)+"_songs", output_)
np.save("input_output/measures_input_"+str(num_of_scores)+"_songs", measures_input_)
np.save("input_output/measures_output_"+str(num_of_scores)+"_songs", measures_output_)

input_ = np.load("input_output/output_"+str(num_of_scores)+"_songs.npy")
output_ = np.load("input_output/input_"+str(num_of_scores)+"_songs.npy")
measures_input_ = np.load("input_output/measures_input_"+str(num_of_scores)+"_songs.npy")
measures_output_ = np.load("input_output/measures_output_"+str(num_of_scores)+"_songs.npy")

model = vec.load_train("saved_model/model2.h5")

print("input_.shape: ", input_.shape)
print("measures_input_.shape: ", measures_input_.shape)




def train_note_model():
  model = Sequential()
  model.add(LSTM(256, input_shape=(None, onehot_size), return_sequences=True))
  model.add(Dropout(0.15))
  model.add(Dense(256))
  model.add(Dropout(0.15))
  model.add(LSTM(512, return_sequences=True))
  model.add(Dropout(0.15))
  model.add(Dense(256))
  model.add(Dropout(0.15))
  model.add(LSTM(512, return_sequences=True))
  model.add(Dense(256))
  model.add(Dropout(0.15))
  model.add(Dense(onehot_size))
  model.add(Activation('softmax'))
  optimizer = RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=1e-6)
  # treble_model = multi_gpu_model(treble_model, gpus=4)
  # model.load_weights(temp_model.hdf5)
  model.compile(loss='categorical_crossentropy', optimizer=optimizer)
  filepath="saved_model/note_epoch{epoch:02d}-loss{loss:.2f}.hdf5"
  checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=0, save_best_only=True, mode='min', period=10)
  callbacks_list = [checkpoint]
  model.fit(input_, output_, nb_epoch=100000, batch_size=512, callbacks=callbacks_list, verbose=2)



def train_chord_model():
chord_model = Sequential()
chord_model.add(LSTM(256, input_shape=(None, 12), return_sequences=True))
chord_model.add(Dropout(0.15))
chord_model.add(Dense(256))
chord_model.add(Dropout(0.15))
chord_model.add(LSTM(512, return_sequences=True))
chord_model.add(Dropout(0.15))
chord_model.add(Dense(256))
chord_model.add(Dropout(0.15))
chord_model.add(LSTM(512, return_sequences=True))
chord_model.add(Dense(256))
chord_model.add(Dropout(0.15))
chord_model.add(Dense(12))
chord_model.add(Activation('softmax'))
optimizer = RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=1e-6)
# chord_model.load_weights(filepath)
chord_model.compile(loss='categorical_crossentropy', optimizer=optimizer)
filepath="saved_model/chord_epoch{epoch:02d}-loss{loss:.2f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=0, save_best_only=True, mode='min', period=100)
callbacks_list = [checkpoint]
chord_model.fit(measures_input_, measures_output_, nb_epoch=10000, batch_size=512, callbacks=callbacks_list, verbose=2)




new_model = load_model("model.h5")

chord_model = None


predict_notes = vec.generate_music(model, chord_model=None, bundle_size=bundle_size, total_length=400)
s = vec.notes_to_stream(predict_notes)
s.show()



def test_score():
  index = 0
  for score_name in scores:
    file_name = score_dir + '/' + score_name
    print(index, "/", len(scores), "Score Name: ", score_name)
    if score_name[-4:] != '.mxl':
      print("Invalid Score")
      print()
      continue
    check_song = music21.converter.parse(file_name)
    index += 1
    print()


# sample_index = 3

# a = treble_input[sample_index]
# a = a.reshape([1, bundle_size, onehot_size])
# s = vec.vector_to_stream(a)
# s.show()

# a = treble_output[sample_index]
# a = a.reshape([1, bundle_size, onehot_size])
# s = vec.vector_to_stream(a)
# s.show()