from music21 import *
import numpy as np
from fractions import Fraction
from collections import Counter

#c0 - b8
#vector size = 1(rest) + 9(number of octave) + 12(number of names) + 16(number of possible durations) + 1(measure at) + 1(measure left)

""" 
Duration
1/12, 0.0625, 0.125, 0.1875, 0.375, 0.625, 0.875,
1/6,  0.25, 1/3, 0.5, 2/3,  0.75, 5/6,  1, 7/6, 1.25, 4/3,  1.5, 5/3,  1.75, 11/6, 2,
13/6, 2.25, 7/3, 2.5, 8/3, 2.75, 17/6, 3, 19/6, 3.25, 10/3, 3.5, 11/3, 3.75, 23/6, 4, 6
"""


# vector_size = 1 + 9 + 12 + 1 + 1 + 1
# measure_at_index = 1 + 12*9
number_of_octave = 9
number_of_names = 12
number_of_possible_duration = 16
vector_size = 1 + number_of_octave + number_of_names + number_of_possible_duration + 1 + 1
octave_pos_in_vector = 1
name_pos_in_vector = octave_pos_in_vector + number_of_octave
duration_pos_in_vector = name_pos_in_vector + number_of_names
measure_at_pos_in_vector = duration_pos_in_vector + number_of_possible_duration
measure_left_pos_in_vector = measure_at_pos_in_vector + 1





def vectorize(part):
	measures = part.getElementsByClass('Measure')
	total_num_measures = len(measures)
	num_all_notes = count_notes(part1)
	vector = np.zeros([num_all_notes, vector_size])  # np.empty or np.zeros
	total_accum_duration = 0
	nth_index = -1
	measure_index = 0
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
				iter_note = iter_item
			elif type(iter_item) is chord.Chord:
				iter_note = iter_item[-1]   # get the hightst picth in the chord for now. We will get all notes in chord in the future
			elif type(iter_item) is note.Rest:
				iter_vector[0] = 1  # Might vector[nth_index][0] = 1
				iter_duration = iter_item.duration.quarterLength
				duration_index = transform_duration_to_number(iter_duration)
				iter_vector[duration_pos_in_vector + duration_index] = 1
				iter_vector[measure_at_pos_in_vector] = measure_index
				iter_vector[measure_left_pos_in_vector] = total_num_measures - measure_index - 1
				measure_accum_duration += iter_duration
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
					iter_vector[measure_at_pos_in_vector] = measure_index
					iter_vector[measure_left_pos_in_vector] = total_num_measures - measure_index - 1
					measure_accum_duration += iter_duration
					continue

			if(iter_octave > 9):
				print("Octave is too high. Consider it as a Rest")
				iter_vector[0] = 1  
				iter_vector[duration_pos_in_vector + duration_index] = 1
				iter_vector[measure_at_pos_in_vector] = measure_index
				iter_vector[measure_left_pos_in_vector] = total_num_measures - measure_index - 1
				measure_accum_duration += iter_duration
				continue

			iter_vector[octave_pos_in_vector+iter_octave] = 1
			iter_vector[name_pos_in_vector+iter_name_number] = 1
			iter_vector[duration_pos_in_vector+duration_index] = 1
			iter_vector[measure_at_pos_in_vector] = measure_index
			iter_vector[measure_left_pos_in_vector] = total_num_measures - measure_index - 1


			measure_accum_duration += iter_duration

		total_accum_duration += measure_accum_duration
	return vector




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
	possible_duration = [0.0625, Fraction(1,10), Fraction(1,12), 0.125, Fraction(1,6), 0.25, Fraction(1,3),
						0.5, 0.75, 1.0, 1.5, 1.75, 2.0, 3.0, 4.0, 6.0]
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

summer = converter.parse("Summer_Joe_Hisaishi.mxl")
part1 = summer.getElementsByClass('Part')[0]
measures1 = part1.getElementsByClass('Measure')
num_all_notes1 = measures1.recurse().notes
vector1 = vectorize(part1)

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
0.0625, 1/10, 1/12, 0.125, 1/6, 0.25, 1/3, 0.5, 0.75, 1.0, 1.5, 1.75, 2.0, 3.0, 4.0, 6.0
"""


