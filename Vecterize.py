from music21 import *
import numpy as np
from fractions import Fraction
from collections import Counter
import copy
from keras.preprocessing import sequence

#c0 - b8
#onehot_size: 1(rest) + 9(number of octave) + 12(number of names) + 16(number of possible durations) Not using{+ 1(measure at) + 1(measure left)}

""" 
Duration
1/12, 0.0625, 0.125, 0.1875, 0.375, 0.625, 0.875,
1/6,  0.25, 1/3, 0.5, 2/3,  0.75, 5/6,  1, 7/6, 1.25, 4/3,  1.5, 5/3,  1.75, 11/6, 2,
13/6, 2.25, 7/3, 2.5, 8/3, 2.75, 17/6, 3, 19/6, 3.25, 10/3, 3.5, 11/3, 3.75, 23/6, 4, 6
"""



# onehot_size = 1 + 9 + 12 + 1 + 1 + 1
# measure_at_index = 1 + 12*9
MAX_NUM_NOTES = 25   # Max number of notes per Measure
sequence_length = 0
number_of_octave = 9
number_of_names = 12
number_of_possible_duration = 16
onehot_size = 1 + number_of_octave + number_of_names + number_of_possible_duration
octave_pos_in_vector = 1
name_pos_in_vector = octave_pos_in_vector + number_of_octave
duration_pos_in_vector = name_pos_in_vector + number_of_names


possible_duration = [0.0625, Fraction(1,10), Fraction(1,12), 0.125, Fraction(1,6), 0.25, Fraction(1,3),
						0.5, 0.75, 1.0, 1.5, 1.75, 2.0, 3.0, 4.0, 6.0]

name_dic = {0:'C', 1:'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F', 6: 'F#', 7: 'G',
				8: 'G#', 9: 'A', 10: 'A#', 11: 'B'}

sharps_to_diatonic_dic = {-1: -5, -2: 2, -3: -3, -4: 4, -5: -1, -6: -6,
													0: 0, 1: 5, 2: -2, 3: 3, 4: -4, 5: 1}

duration_dic = {}
for i in range(len(possible_duration)):
	duration_dic[i] = possible_duration[i]



def vectorize(part, sample_measure_size=1, scale_int=0):   # current scale in int,  C major = 0, D major = 2

	sequence_length = sample_measure_size * MAX_NUM_NOTES

	measures = part.getElementsByClass('Measure')
	total_num_measures = len(measures)
	# num_all_notes = count_notes(part)
	sample_size = total_num_measures - sample_measure_size + 1

	steps_to_move = sharps_to_diatonic_dic[scale_int]  # make every note in diatonic scale   scale_int = 0 for no transpose


	ret_vector = np.empty(shape=(0, sequence_length, onehot_size))
	sample_vector = np.zeros([1, sample_measure_size, MAX_NUM_NOTES, onehot_size])
	sample_index = 0


	for measure_index in range(len(measures)):
		iter_measure = measures[measure_index]
		measure_vector = np.zeros([MAX_NUM_NOTES, onehot_size])

		note_index = 0
		for iter_item in iter_measure:
			if(note_index > MAX_NUM_NOTES):
				print("WARNING!!!  note_index is bigger than MAX_NUM_NOTES:", MAX_NUM_NOTES)
				continue

			if type(iter_item) not in [note.Note, note.Rest, chord.Chord]:
				continue


			iter_onehot_vector = np.zeros(onehot_size)


			iter_note = None

			if type(iter_item) is note.Note:
				iter_note = iter_item.transpose(steps_to_move) # make note in diatonic scale
			elif type(iter_item) is chord.Chord:
				iter_note = iter_item[-1].transpose(steps_to_move)   # get the highest picth in the chord for now. We will get all notes in chord in the future
			elif type(iter_item) is note.Rest:
				iter_onehot_vector[0] = 1
				iter_duration = iter_item.duration.quarterLength
				duration_index = transform_duration_to_number(iter_duration)
				iter_onehot_vector[duration_pos_in_vector + duration_index] = 1
				note_index += 1
				continue

			iter_name = iter_note.name
			iter_octave = iter_note.octave
			iter_duration = iter_note.duration.quarterLength

			iter_name_number = transform_name_to_number(iter_name)
			iter_octave = get_octave(iter_octave)
			duration_index = transform_duration_to_number(iter_duration)

			if(iter_name_number < 0):  # Case of Cb
				if(iter_octave != 0):
					iter_octave -= 1
					iter_name_number = 12 + iter_name_number
				else:
					print("Invalid Note. Consider it as a Rest")
					iter_onehot_vector[0] = 1  
					iter_onehot_vector[duration_pos_in_vector + duration_index] = 1
					continue

			if(iter_octave > 9):
				print("Octave is too high. Consider it as a Rest")
				iter_onehot_vector[0] = 1  
				iter_onehot_vector[duration_pos_in_vector + duration_index] = 1
				continue

			iter_onehot_vector[octave_pos_in_vector+iter_octave] = 1
			iter_onehot_vector[name_pos_in_vector+iter_name_number] = 1
			iter_onehot_vector[duration_pos_in_vector+duration_index] = 1
			measure_vector[note_index] = iter_onehot_vector
			note_index += 1



		if(measure_index < sample_measure_size - 1):  # Normal Case
			sample_vector[0,measure_index] = measure_vector


		else:  # Last case
			sample_vector[0, -1] = measure_vector
			# need to add sample_vector to ret_vector after flatten
			flatten_sample_vector = flatten_measures_vector(sample_vector)
			ret_vector = np.append(ret_vector, flatten_sample_vector, axis=0)


			temp_sample_vector = np.zeros([1, sample_measure_size, MAX_NUM_NOTES, onehot_size])
			temp_sample_vector[0, :-1, : , : ] = copy.deepcopy(sample_vector[0, 1:, :, :])
			sample_vector = temp_sample_vector
		


	return ret_vector




def flatten_measures_vector(sample_vector):
	#the sample_vector.shape should be [1, sample_measure_size, 16, onehot_size]
	one_, sample_measure_size, max_num_note_in_measure, onehot_size_ = sample_vector.shape

	return sample_vector.reshape([one_, sample_measure_size * max_num_note_in_measure, onehot_size_])





def get_octave(octave):
	if(octave == None):
		return 4
	else:
		return octave





def transform_name_to_number(name):
	pos = 0
	half = 0
	aug = 0
	note_name = name[0]
	if(len(name) == 2):
		half = name[-1]
	elif(len(name) == 3):
		half = name[-2]
		aug = name[-1]

	if(note_name == 'C'):
		pos = 0
	elif(note_name == 'D'):
		pos = 2
	elif(note_name == 'E'):
		pos = 4
	elif(note_name == 'F'):
		pos = 5
	elif(note_name == 'G'):
		pos = 7
	elif(note_name == 'A'):
		pos = 9
	elif(note_name == 'B'):
		pos = 11
	else:
		print("transform_name_to_number is not in A to G")

	if(half != 0):
		if(half == '#'):
			pos += 1
		elif(half == '-'):
			pos -= 1
		else:
			print("weird half up or down detected", half)

	if(aug != 0):
		if(aug == '#'):
			pos += 1
		else:
			print("Weird Aug detected", aug)

	return pos




def transform_duration_to_number(duration):
	duration_index = 0
	try:
		duration_index = possible_duration.index(duration)
		return duration_index
	except:
		print("There is no such duration '" + str(duration) + "' in possible_duration list so I will return 1.0")
		return possible_duration.index(1.0)




def count_notes(part):
	note_cnt = 0
	rest_cnt = 0
	chord_cnt = 0
	measure_cnt = 0
	duration_cnt = 0
	measures = part.getElementsByClass('Measure')
	for measure in measures:
		measure_cnt += 1
		for item in measure:
			if type(item) is note.Note:
				note_cnt += 1
				duration_cnt += item.duration.quarterLength
			elif type(item) is note.Rest:
				rest_cnt += 1
				duration_cnt += item.duration.quarterLength
			elif type(item) is chord.Chord:
				chord_cnt += 1
				duration_cnt += item.duration.quarterLength
			duration_cnt = round(duration_cnt, 6)
		duration_cnt = round(duration_cnt, 5)
	return note_cnt + rest_cnt + chord_cnt



# c = {x:allDuration.count(x) for x in allDuration}

# summer = converter.parse("Summer_Joe_Hisaishi.mxl")
# part1 = summer.getElementsByClass('Part')[0]
# measures1 = part1.getElementsByClass('Measure')
# num_all_notes1 = measures1.recurse().notes
# vector1 = vectorize(part1)

# part2 = summer.getElementsByClass('Part')[1]
# measures2 = part2.getElementsByClass('Measure')
# vector2 = vectorize(part2)


# song = converter.parse("Spring.mxl")
# song_part = song.getElementsByClass('Part')
# song_notes = song_part.recurse().notes
# song_durations = [i.duration.quarterLength for i in song_notes]
# song_counter = Counter(song_durations)




def check_duration(name_of_song):
	song = converter.parse(name_of_song)
	song_part = song.getElementsByClass('Part')
	song_notes = song_part.recurse().notes
	song_durations = [i.duration.quarterLength for i in song_notes]
	song_counter = Counter(song_durations)
	return song_counter



"""
Duration
[0.0625, 1/10, 1/12, 0.125, 1/6, 0.25, 1/3, 0.5, 0.75, 1.0, 1.5, 1.75, 2.0, 3.0, 4.0, 6.0]
"""



def vector_to_note(vector):	
	choosen_notes = []
	vector = vector.reshape(len(vector[0,:]), len(vector[0,0,:]))
	length = vector.shape[0]
	for i in range(length):
		iter_vector = vector[i, :]
		octave = iter_vector[1:10]
		name = iter_vector[10:22]
		duration = iter_vector[22:38]
		is_rest_name = np.append(np.array(iter_vector[0]), iter_vector[10:22])
		if(is_rest_name.argmax() == 0):
			max_val = max(duration)
			if(max_val == 0):
				choosen_duration = 0.5
			else:
				choosen_duration = possible_duration[duration.argmax()]
			choosen_note = note.Rest(quarterLength = choosen_duration)
		else:
			# Probability octave
			sum_ = octave.sum()
			octave = octave / sum_
			choosen_value = np.random.choice(octave, p = octave)
			choosen_octave = str(np.where(octave == choosen_value)[0][0])
			# choosen_octave = str(octave.argmax())
			# Probability name
			sum_ = name.sum()
			name = name / sum_
			choosen_name_value = np.random.choice(name, p = name)
			choosen_name_index = np.where(name == choosen_name_value)[0][0]
			choosen_name = name_dic[choosen_name_index]
			# choosen_name = name_dic[name.argmax()]

			# Probability duration
			sum_ = duration.sum()
			duration = duration / sum_
			choosen_duration_value = np.random.choice(duration, p = duration)
			choosen_duration_index = np.where(duration == choosen_duration_value)[0][0]
			choosen_duration = possible_duration[choosen_duration_index]
			# choosen_duration = possible_duration[duration.argmax()]
			choosen_note = note.Note(choosen_name + choosen_octave, quarterLength = choosen_duration)
		choosen_notes.append(choosen_note)
	return choosen_notes



def output_to_one_hot(vector):
	# vecctor shape should be (38, )
	one_hot = np.zeros(onehot_size)
	octave = vector[1:10]
	name = vector[10:22]
	duration = vector[22:38]
	is_rest_name = np.append(np.array(vector[0]), vector[10:22])
	if(is_rest_name.argmax() == 0):
		one_hot[0] = 1
		best_index = duration.argmax()
		one_hot[22 + best_index] = 1
	else:
		one_hot[1 + octave.argmax()] = 1
		one_hot[10 + name.argmax()] = 1
		one_hot[22 + duration.argmax()] = 1
	return one_hot




def make_output(vector):
	# vector should shape in (sequence length, one_hot_vector length)
	output = np.zeros(vector.shape)

	
	# output[:,:-1,:] = copy.deepcopy(vector[:,1:,:])   # For measure slide

	output[:-1,:,:] = vector[1:,:,:]  # For notes slide

	return output



def pad_sequences(vector, maxlen=None):
	# vector should shape in (sequence length, one_hot_vector length)

	trans_vector = np.transpose(vector)
	pad_outcome = sequence.pad_sequences(trans_vector, maxlen=maxlen, padding='post')
	outcome = np.transpose(pad_outcome) 
	return outcome



def mxl_to_vector(mxl_file, measure_size=2, bundle_size=20, maxlen=600, clef="treble"):
	summer = converter.parse(mxl_file)
	parts = []
	part = None	

	if clef == "treble":
		part = summer.getElementsByClass('Part')[0]
	elif clef == "bass":
		part = summer.getElementsByClass('Part')[1]
	else:
		print("Clef is either treble or bass. Default is treble")
		part = summer.getElementsByClass('Part')[0]


	key_ = get_key(part)

	# vector = vectorize(part, measure_size, key_.sharps)   # Slide window by measure
	vector = slide_window(part, bundle_size=bundle_size, scale_int=key_.sharps)  # Slide window by notes


	output = make_output(vector)

	# vector = pad_sequences(vector, maxlen=maxlen)
	# output = pad_sequences(output, maxlen=maxlen)

	# seq_length, one_hot_length = vector.shape

	# vector = vector.reshape(1, maxlen, one_hot_length)   #(number of training data, sequence length, one_hot_vector length)

	# output = output.reshape(1, maxlen, one_hot_length) 

	return vector, output



def vector_to_stream(vector):
	notes = vector_to_note(vector)
	s = notes_to_stream(notes)
	return s



def notes_to_stream(notes):
	s = stream.Stream()
	for note in notes:
		if note.duration.quarterLength not in [Fraction(1,10)]:
			s.append(note)
	return s





def print_part(part):
	for i in range(len(part)):
		print(i, ":", part[i])
		try:
			for j in part[i]:
				print(j)
		except:
			continue
		print()



def get_key(part):
	for i in part:
		try:
			part_key = i.getElementsByClass('KeySignature')
			if(len(part_key) > 0):
				key_ = part_key[0]
				return key_
		except:
			continue








def vectorize(part, scale_int=0):
	measures = part.getElementsByClass('Measure')
	total_num_measures = len(measures)
	num_all_notes = count_notes(part)
	if(num_all_notes > 600):
		print("Number of Notes are bigger than maximum size: ", num_all_notes)
		return None
	vector = np.zeros([600, onehot_size]) 
	total_accum_duration = 0
	nth_index = -1
	measure_index = 0
	steps_to_move = sharps_to_diatonic_dic[scale_int]
	for measure in measures:
		measure_index += 1
		measure_accum_duration = 0
		for iter_item in measure:
			if type(iter_item) not in [note.Note, note.Rest, chord.Chord]:
				continue
			else:
				nth_index += 1

			iter_vector = vector[:][nth_index]
			# vector[0][nth_index][0] = 1  # Show that it is not rest
			iter_note = None
			if type(iter_item) is note.Note:
				iter_note = iter_item.transpose(steps_to_move)
			elif type(iter_item) is chord.Chord:
				iter_note = iter_item[-1].transpose(steps_to_move)   # get the hightst picth in the chord for now. We will get all notes in chord in the future
			elif type(iter_item) is note.Rest:
				iter_vector[0] = 1  # Might vector[nth_index][0] = 1
				iter_duration = iter_item.duration.quarterLength
				duration_index = transform_duration_to_number(iter_duration)
				iter_vector[duration_pos_in_vector + duration_index] = 1
				continue
			else:
				continue

			iter_name = iter_note.name
			iter_octave = iter_note.octave
			iter_duration = iter_note.duration.quarterLength

			iter_name_number = transform_name_to_number(iter_name)
			iter_octave = get_octave(iter_octave)
			duration_index = transform_duration_to_number(iter_duration)

			if(iter_name_number < 0):
				if(iter_octave != 0):
					iter_octave -= 1
					iter_name_number = 12 + iter_name_number
				else:
					print("Invalid Note. Consider it as a Rest")
					iter_vector[0] = 1  
					iter_vector[duration_pos_in_vector + duration_index] = 1
					continue

			if(iter_octave > 9):
				print("Octave is too high. Consider it as a Rest")
				iter_vector[0] = 1  
				iter_vector[duration_pos_in_vector + duration_index] = 1
				continue

			iter_vector[octave_pos_in_vector+iter_octave] = 1
			iter_vector[name_pos_in_vector+iter_name_number] = 1
			iter_vector[duration_pos_in_vector+duration_index] = 1


	return vector



def slide_window(part, bundle_size=10, scale_int=0):

	vector = vectorize(part, scale_int=scale_int)

	sample_size = len(vector) - bundle_size + 1
	ret_vector = np.empty(shape=(sample_size, bundle_size, onehot_size))

	for i in range(sample_size):
		bundle_vector = vector[i:i+bundle_size, :]
		ret_vector[i] = bundle_vector

	return ret_vector



def note_to_vector(note):
	onehot_vector = np.zeros(onehot_size)
	name_number = transform_name_to_number(note.name)
	octave = get_octave(note.octave)
	duration_index = transform_duration_to_number(note.duration.quarterLength)
	if(name_number < 0):  # Case of Cb
		if(octave != 0):
			octave -= 1
			name_number = 12 + name_number
		else:
			print("Invalid Note. Consider it as a Rest")
			onehot_vector[0] = 1  
			onehot_vector[duration_pos_in_vector + duration_index] = 1
	elif(octave > 9):
		print("Octave is too high. Consider it as a Rest")
		onehot_vector[0] = 1  
		onehot_vector[duration_pos_in_vector + duration_index] = 1
	else:
		onehot_vector[octave_pos_in_vector + octave] = 1
		onehot_vector[name_pos_in_vector + name_number] = 1
		onehot_vector[duration_pos_in_vector + duration_index] = 1
	return onehot_vector





def generate_music(model, bundle_size=10):
	first_note_name =  name_dic[np.random.choice(len(name_dic))]
	first_note_duration = np.random.choice([0.25, 0.5, 1.0, 2.0, 4.0])
	first_note_octave = np.random.choice(['4', '5'])
	first_note = note.Note(first_note_name + first_note_octave, quarterLength = first_note_duration)
	predict_one_hots = note_to_vector(first_note).reshape(1, 1, onehot_size)
	predict_notes = [first_note]
	for i in range(1, 400):
		print(i, "/", 400)
		outcome = model.predict(predict_one_hots)
		latest_outcomt = outcome[0, -1]
		predict_note = vector_to_note(latest_outcomt.reshape(1, 1, onehot_size))
		predict_notes.extend(predict_note)
		predict_one_hot = output_to_one_hot(latest_outcomt)
		if(len(predict_one_hots[0]) < 10):
			predict_one_hots = np.append(predict_one_hots[0], predict_one_hot.reshape(1, onehot_size), axis=0)
			len_so_far, no = predict_one_hots.shape
			predict_one_hots = predict_one_hots.reshape(1, len_so_far, onehot_size)
		else:
			predict_one_hots[0, :-1, :] = predict_one_hots[0, 1:, :]
			predict_one_hots[0, -1] = predict_one_hot
	return predict_notes
