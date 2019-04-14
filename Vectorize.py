import music21
import numpy as np
from fractions import Fraction
from collections import Counter
import copy
from keras.preprocessing import sequence
from keras.models import load_model
import os.path

#c0 - b8
#onehot_size: 1(rest) + 10(number of note pressed) + ( 9(number of octave) * 12(number of names) ) + 16(number of possible durations) Not using{+ 1(measure at) + 1(measure left)}


# score.flat     # naive flat
# score.chordify()   # more delicate 






""" 
Duration
1/12, 0.0625, 0.125, 0.1875, 0.375, 0.625, 0.875,
1/6,  0.25, 1/3, 0.5, 2/3,  0.75, 5/6,  1, 7/6, 1.25, 4/3,  1.5, 5/3,  1.75, 11/6, 2,
13/6, 2.25, 7/3, 2.5, 8/3, 2.75, 17/6, 3, 19/6, 3.25, 10/3, 3.5, 11/3, 3.75, 23/6, 4, 6
"""


possible_duration = [0.0625, Fraction(1,10), Fraction(1,12), 0.125, Fraction(1,6), Fraction(1,5), 0.25, 
										Fraction(1,3), 0.375,	0.5, Fraction(2,3), Fraction(1,6), 0.75, 0.875, 1.0, 1.5, 1.75, 2.0, 3.0, 3.5, 4.0, 6.0]

name_dic = {0:'C', 1:'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F', 6: 'F#', 7: 'G',
				8: 'G#', 9: 'A', 10: 'A#', 11: 'B'}

sharps_to_diatonic_dic = {-1: -5, -2: 2, -3: -3, -4: 4, -5: -1, -6: -6,
													0: 0, 1: 5, 2: -2, 3: 3, 4: -4, 5: 1}



# measure_at_index = 1 + 12*9
MAX_NUM_NOTES = 25   # Max number of notes per Measure
sequence_length = 0
possible_number_of_note_pressed = 10
number_of_octave = 9
number_of_names = 12
number_of_possible_duration = len(possible_duration)
onehot_size = 1 + possible_number_of_note_pressed + (number_of_octave * number_of_names) + number_of_possible_duration
note_pos_in_vector = 1 + possible_number_of_note_pressed
duration_pos_in_vector = note_pos_in_vector + (number_of_octave * number_of_names)
max_notes = 800

duration_dic = {}
for i in range(len(possible_duration)):
	duration_dic[i] = possible_duration[i]




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
		print("There is no such duration '" + str(duration) + "' in possible_duration list so I will return 0.5(half)")
		return possible_duration.index(0.5)



# Count all notes including notes, rests, chords
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
			if type(item) is music21.note.Note:
				note_cnt += 1
				duration_cnt += item.duration.quarterLength
			elif type(item) is music21.note.Rest:
				rest_cnt += 1
				duration_cnt += item.duration.quarterLength
			elif type(item) is music21.chord.Chord:
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


# input vector shape suppose to be (1, num_of_notes, one_hot_size)
def vector_to_note(vector):	
	stream_notes = []
	vector = vector.reshape(len(vector[0,:]), len(vector[0,0,:]))
	length = vector.shape[0]
	for i in range(length):
		iter_vector = vector[i, :]
		number_of_note_pressed = get_number_of_key_pressed(iter_vector)
		name_vector = iter_vector[note_pos_in_vector : note_pos_in_vector + (number_of_octave * number_of_names)]
		duration_vector = iter_vector[duration_pos_in_vector : duration_pos_in_vector + len(possible_duration)]
		is_rest_name = np.append(np.array(iter_vector[0]), iter_vector[note_pos_in_vector : note_pos_in_vector + (number_of_octave * number_of_names)])
		if(number_of_note_pressed == 0):
			max_val = max(duration_vector)
			if(max_val == 0):
				choosen_duration = 0.5
			else:
				choosen_duration = possible_duration[duration_vector.argmax()]
			next_note = music21.note.Rest(quarterLength = choosen_duration)
		else:
			choosen_notes = choose_note(name_vector, number_of_note_pressed)
			choosen_duration = choose_duration(duration_vector)
			if number_of_note_pressed == 1:
				next_note = music21.note.Note(choosen_notes[0], quarterLength = choosen_duration)
			else:
				next_note = music21.chord.Chord(choosen_notes, quarterLength = choosen_duration)
		print("next_note:", next_note)
		stream_notes.append(next_note)
	return stream_notes



def get_number_of_key_pressed(iter_vector):
	number_of_note_pressed_vector = iter_vector[0 : 1 + possible_number_of_note_pressed]
	number_of_note_pressed = number_of_note_pressed_vector.argmax()
	return number_of_note_pressed




def choose_note(name_vector, number_of_note_pressed):
	sum_value = name_vector.sum()
	name_prob = name_vector / sum_value  # Normalize
	choosen_values = np.random.choice(name_vector, number_of_note_pressed, replace=False, p=name_prob)
	choosen_notes = []
	for choosen_value in choosen_values:
		choosen_index = np.where(name_vector == choosen_value)[0][0]
		name_vector[choosen_index] = 0.0   # Make it 0.0 that is choosen for deleting same probabilty
		choosen_octave = int(choosen_index / number_of_names)
		choosen_name_index = choosen_index % number_of_names
		choosen_name = name_dic[choosen_name_index]
		choosen_note = choosen_name + str(choosen_octave)
		choosen_notes.append(choosen_note)
	return choosen_notes


def choose_duration(duration_vector):
	# Probability duration
	sum_value = duration_vector.sum()
	duration_vector = duration_vector / sum_value
	choosen_duration_value = np.random.choice(duration_vector, p = duration_vector)
	choosen_duration_index = np.where(duration_vector == choosen_duration_value)[0][0]
	choosen_duration = possible_duration[choosen_duration_index]
	# choosen_duration = possible_duration[duration_vector.argmax()]   # For choosing the hightest prob duration, not selecting base on prob 
	return choosen_duration





def output_to_one_hot(vector):
	# vecctor shape should be (38, )
	one_hot = np.zeros(onehot_size)
	number_of_key_pressed_vector = vector[:11]
	note_vector = vector[11 : duration_pos_in_vector]
	duration_vector = vector[duration_pos_in_vector : duration_pos_in_vector + len(possible_duration)]

	duration_index = duration_vector.argmax()
	one_hot[duration_pos_in_vector + duration_index] = 1


	sum_value = name_vector.sum()
	name_prob = name_vector / sum_value  # Normalize
	choosen_values = np.random.choice(name_vector, number_of_note_pressed, replace=False, p=name_prob)
	choosen_notes = []
	for choosen_value in choosen_values:
		choosen_index = np.where(name_vector == choosen_value)[0][0]
		name_vector[choosen_index] = 0.0   # Make it 0.0 that is choosen for deleting same probabilty
		choosen_octave = int(choosen_index / number_of_names)
		choosen_name_index = choosen_index % number_of_names
		choosen_name = name_dic[choosen_name_index]
		choosen_note = choosen_name + str(choosen_octave)
		choosen_notes.append(choosen_note)


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



def pad_sequences(vector, maxlen=600):
	# vector should shape in (sequence length, one_hot_vector length)
	seq_len, bundle_len, onehot_len = vector.shape
	pad_vector = np.zeros([maxlen, bundle_len, onehot_len])
	if seq_len > maxlen:
		pad_vector[: maxlen] = vector[: maxlen]
	else:
		pad_vector[: seq_len] = vector[: seq_len]
	return pad_vector



def mxl_to_vector(mxl_file, measure_size=2, bundle_size=20, slide_size=2, maxlen=max_notes, clef="treble"):
	first_love = music21.converter.parse(mxl_file)
	part_chordify = first_love.chordify()   # Merge treble and bass
	key_ = get_key(part_chordify)
	part = remove_tie_part(part_chordify)
	# if clef == "treble":
	# 	part = first_love.getElementsByClass('Part')[0]
	# elif clef == "bass":
	# 	part = first_love.getElementsByClass('Part')[1]
	# else:
	# 	print("Clef is either treble or bass. Default is treble")
	# 	part = first_love.getElementsByClass('Part')[0]
	# vector = all_vectorize(part, measure_size, key_.sharps)   # Slide window by measure
	vector, output = slide_window(part, bundle_size=bundle_size, slide_size=slide_size, scale_int=key_.sharps)  # Slide window by notes
	sample_size = int(np.ceil((max_notes - bundle_size + 1) / slide_size))
	vector = vector[:sample_size]
	output = output[:sample_size]
	# output = make_output(vector)
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
	s = music21.stream.Stream()
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


def test_transform_to_diatonic():
	river = music21.converter.parse('score/River_Flows_In_You.mxl')
	river_chordify = river.chordify()   # Merge treble and bass
	key_ = get_key(river_chordify)
	untied_river = remove_tie_part(river_chordify)
	vectorized_diatonic_part = all_vectorize(untied_river, scale_int=key_.sharps)
	reshaped = vectorized_diatonic_part.reshape(1, vectorized_diatonic_part.shape[0], vectorized_diatonic_part.shape[1])
	diatonic_stream = vector_to_stream(reshaped)
	return diatonic_stream





def all_vectorize(part, scale_int=0):
	measures = part.getElementsByClass('Measure')
	total_num_measures = len(measures)
	num_all_notes = count_notes(part)
	print("num_all_notes:", num_all_notes)
	vector = np.zeros([max_notes, onehot_size]) 
	total_accum_duration = 0
	nth_index = 0
	measure_index = 0
	steps_to_move = sharps_to_diatonic_dic[scale_int]
	for measure in measures:
		measure_index += 1
		measure_accum_duration = 0
		for iter_item in measure:
			if type(iter_item) not in [music21.note.Note, music21.note.Rest, music21.chord.Chord]:
				continue
			elif nth_index >= max_notes-1:
				return vector[:nth_index]
			iter_vector = vector[nth_index]  # Make pointer to vector to be returned
			# vector[0][nth_index][0] = 1  # Show that it is not rest
			iter_note = None
			if type(iter_item) is music21.note.Note:
				iter_note = iter_item.transpose(steps_to_move)   # change note to diatonic mode(C major)
				vector[nth_index] = note_to_vector(iter_note)
			elif type(iter_item) is music21.chord.Chord:
				iter_notes = iter_item.transpose(steps_to_move)   # chord
				# iter_note = iter_item[-1].transpose(steps_to_move)  # get the hightst picth in the chord for now. We will get all notes in chord in the future
				vector[nth_index] = note_to_vector(iter_notes)
			elif type(iter_item) is music21.note.Rest:
				iter_vector[0] = 1
				iter_duration = iter_item.duration.quarterLength
				duration_index = transform_duration_to_number(iter_duration)
				iter_vector[duration_pos_in_vector + duration_index] = 1
			else:
				continue
			nth_index += 1
	vector = vector[: nth_index]
	return vector




# Convert note or chord to one_hot vector
def note_to_vector(iter_note):
	onehot_vector = np.zeros(onehot_size)
	duration_index = transform_duration_to_number(iter_note.duration.quarterLength)
	onehot_vector[duration_pos_in_vector + duration_index] = 1
	if type(iter_note) is music21.note.Note:
		is_chord = False
	elif type(iter_note) is music21.chord.Chord:
		is_chord = True
	else:
		is_chord = False
		print("WARNING!!! iter_note is", type(iter_note))
		onehot_vector[0] = 1
		return onehot_vector
	if is_chord:
		number_of_key_pressed = len(iter_note)
	else:
		iter_note = [iter_note]
		number_of_key_pressed = 1
	onehot_vector[number_of_key_pressed] = 1
	for each_note in iter_note:
		name_number = transform_name_to_number(each_note.name)
		octave = get_octave(each_note.octave)
		each_note_index = name_number + number_of_names * octave
		if(name_number < 0):  # Case of Cb
			if(octave != 0):
				octave -= 1
				name_number = 12 + name_number  # Convert Cb to B
			else:
				print("Invalid Note. Consider it as a Rest")
				onehot_vector[0] = 1  
		elif(octave > 9):
			print("Octave is too high. Consider it as a Rest")
			onehot_vector[0] = 1  
		else:
			onehot_vector[note_pos_in_vector + each_note_index] = 1
	return onehot_vector




def slide_window(part, bundle_size=10, slide_size=2, scale_int=0):
	vector = all_vectorize(part, scale_int=scale_int)
	print("vector.shape: ", vector.shape)
	print("len(vector): ", len(vector))
	sample_size = int(np.ceil((len(vector) - bundle_size + 1) / slide_size))
	input_ = np.empty(shape=[0, bundle_size, onehot_size])
	output_ = np.empty(shape=[0, bundle_size, onehot_size])
	input_vector = np.empty(shape=(sample_size, bundle_size, onehot_size))
	output_vector = np.empty(shape=(sample_size, bundle_size, onehot_size))
	index = 0
	for i in range(0, sample_size - slide_size, slide_size):
		input_ = np.append(input_, copy.deepcopy(vector[i : i + bundle_size, : ]).reshape([1, bundle_size, onehot_size]), axis=0)
		output_ = np.append(output_, copy.deepcopy(vector[i + 1 : i + bundle_size + 1, : ]).reshape([1, bundle_size, onehot_size]), axis=0)
		input_vector[index] = copy.deepcopy(vector[i : i + bundle_size, : ])
		output_vector[index] = copy.deepcopy(vector[i + 1 : i + bundle_size + 1, : ])
		index += 1
	return input_, output_








def generate_music(model, bundle_size=10, total_length=400):
	first_note_name =  name_dic[np.random.choice(len(name_dic))]
	first_note_duration = np.random.choice([0.25, 0.5, 1.0, 2.0, 4.0])
	first_note_octave = np.random.choice(['4', '5'])
	first_note = music21.note.Note(first_note_name + first_note_octave, quarterLength = first_note_duration)
	predict_one_hots = note_to_vector(first_note).reshape(1, 1, onehot_size)
	predict_notes = [first_note]
	for i in range(1, 400):
		print(i, "/", 400)
		outcome = model.predict(predict_one_hots)
		latest_outcome = outcome[0, -1]
		predict_note = vector_to_note(latest_outcome.reshape(1, 1, onehot_size))
		predict_notes.extend(predict_note)
		predict_one_hot = note_to_vector(predict_note[0])
		# predict_one_hot = output_to_one_hot(latest_outcome)
		# slide window  keep accumulate predict_one_hot until the bundle size. Then keep the bundle size
		if(len(predict_one_hots[0]) < bundle_size):
			predict_one_hots = np.append(predict_one_hots[0], predict_one_hot.reshape(1, onehot_size), axis=0)
			len_so_far, no = predict_one_hots.shape
			predict_one_hots = predict_one_hots.reshape(1, len_so_far, onehot_size)
		else:
			predict_one_hots[0, :-1, :] = predict_one_hots[0, 1:, :]
			predict_one_hots[0, -1] = predict_one_hot
	return predict_notes




def select_chord(measure):
	all_notes = list(measure.notes)
	


def save_train(trained_model):
	for i in range(1000):
		file_name = 'saved_model/model' + str(i) + '.h5'
		if not os.path.isfile(file_name):
			trained_model.save(file_name)
			return
	print('Too many file exist. It is saved in', file_name)
	trained_model.save(file_name)



def load_train(model_name):
	return load_model(model_name)



def set_slur(s):
	prev = s[0]
	prev_offset = prev.offset
	for cur in s[1:]:
		cur_offset = cur.offset
		if type(prev) is music21.note.Note:
			prev_note = prev
		elif type(prev) is music21.chord.Chord:
			prev_note = prev.sortDiatonicAscending()[0]
		else:
			prev = cur
			continue
		if type(cur) is music21.note.Note:
			cur_note = cur
		elif type(prev) is music21.chord.Chord:
			cur_note = cur.sortDiatonicAscending()[0]
		else:
			continue
		if prev_note == cur_note:
			sl = spanner.Slur([prev, cur])
			s.insert(prev_offset, sl)
		prev = cur
		prev_offset = cur_offset
	return s



def combine_consecutive_note(s):
	new_notes = []
	prev = s[0]
	prev_offset = prev.offset
	accum_quarter_length = prev.quarterLength
	for cur in s[1:]:
		cur_offset = cur.offset
		if type(prev) is music21.note.Note:
			prev_note = prev
		elif type(prev) is music21.chord.Chord:
			prev_note = prev.sortDiatonicAscending()[0]
		elif type(prev) is music21.note.Rest:
			prev = cur
			continue
		else:
			prev = cur
			continue
		if type(cur) is music21.note.Note:
			cur_note = cur
		elif type(cur) is music21.chord.Chord:
			cur_note = cur.sortDiatonicAscending()[0]
		elif type(cur) is music21.note.Rest:
			new_notes.append(music21.note.Note(prev_note), quarterLength=accum_quarter_length)
			new_notes.append(cur)
			prev = cur
			continue    # It might need to be prev = cur
		if prev_note == cur_note:
			accum_quarter_length += cur.quarterLength
		else:
			new_notes.append(music21.note.Note(prev_note), quarterLength=accum_quarter_length)
			prev = cur
			accum_quarter_length = cur.quarterLength
			prev_offset = cur_offset
	new_stream = music21.stream.Stream(new_notes)
	return new_stream




def remove_tie_part(part):
	measures = part.getElementsByClass('Measure')
	for measure_ in measures:
		chords = measure_.getElementsByClass('Chord')
		for chord_ in chords:
			remove_tie_chord(chord_)
	return part



# remove tied note that was chordify()
''' I think I need to consider the case where the tie is not created by chordify().
	Such as a note supposed to be full length and it is full length by two 2 quarter length
'''
def remove_tie_chord(chord_):
	note_index_to_be_remove = []
	for i in range(len(chord_)):
		note_ = chord_[i]
		if note_.tie in [music21.tie.Tie('stop'), music21.tie.Tie('continue')]:
			note_index_to_be_remove.append(i)
		elif note_.tie == music21.tie.Tie('start'):
			note_.tie = None
	while len(note_index_to_be_remove) != 0:
		index = note_index_to_be_remove.pop()
		chord_.remove(chord_[index])




def divide_treb_bass(s):
	treble = []
	bass = []
	for i in s:
		if type(i) is music21.note.Note:
			treble.append(i)
			bass.append(music21.note.Rest(quarterLength = i.quarterLength))
		elif type(i) is music21.chord.Chord:
			bass_note = i.sortDiatonicAscending()[0]
			bass_note.offset = i.offset
			bass.append(bass_note)
			i.remove(i.sortDiatonicAscending()[0])
			treble.append(i)
		else:
			continue
	treb_st = music21.stream.Stream(treble)
	bass_st = music21.stream.Stream(bass)
	main_st = music21.stream.Stream()
	main_st.insert(treb_st)
	main_st.insert(bass_st)
	return main_st
