from music21 import *
import numpy as np
from fractions import Fraction
from collections import Counter

#c0 - b8
#vector size = 1(not rest) + 12 * 9(number of notes) + 1(duration) + 1(measure at) + 1(measure left)

""" 
Duration
1/12, 0.0625, 0.125, 0.1875, 0.375, 0.625, 0.875,
1/6,  0.25, 1/3, 0.5, 2/3,  0.75, 5/6,  1, 7/6, 1.25, 4/3,  1.5, 5/3,  1.75, 11/6, 2,
13/6, 2.25, 7/3, 2.5, 8/3, 2.75, 17/6, 3, 19/6, 3.25, 10/3, 3.5, 11/3, 3.75, 23/6, 4, 6
"""


# vector_size = 1 + 12*9 + 1 + 1 + 1
# measure_at_pos = 1 + 12*9
vector_size = 12*9
measure_at_pos = 12*9
measure_left_pos = measure_at_pos + 1
duration_pos = measure_left_pos + 1

def vectorizePart(part):
	measures = part.getElementsByClass('Measure')
	vector = np.zeros(len(measures))  # I am not sure Rest does count here
	
	for measure_index in range(len(measures)):
		iter_measure = measures[measure_index]
		measure_vector = vectorizeMeasure(iter_measure, measure_index, len(measures))
		vector[measure_index] = measure_vector

	return vector



def vectorizeMeasure(measure, measure_num, total_num_measure, total_index=0, partVector=np.empty(1)):  # partVector and total_index are for the test for now
	allNotes = measure.recurse().notes
	# vector = np.empty([vector_size, len(allNotes)])  # np.empty or np.zeros

	if len(allNotes) == 0:
		return partVector

	accum_duration = 0
	for vector_index in range(len(allNotes)):
		vector = np.empty(vector_size)  # np.empty or np.zeros
		iter_item = allNotes[vector_index]
		iter_note = None
		if type(iter_item) is note.Note:
			iter_note = iter_item
		elif type(iter_note) is chord.Chord:
			iter_note = iter_item[-1]   # get the hightst picth in the chord for now. We will get all notes in chord in the future
		elif type(iter_note) is note.Rest:
			vector[0] = 1  # Might vector[vector_index][0] = 1
			continue
		else:
			print("Type is neighther note nor chord")

		iter_name = iter_note.name
		iter_octave = iter_note.octave
		iter_duration = iter_note.duration.quarterLength
		note_num_pos = name_to_number(iter_name)

		if(iter_octave == 0 and note_pos < 0):
			print("Invalid Note")
			continue

		if(iter_octave > 9):
			print("Octave is too high")

		iter_note_index_in_vector = iter_octave * 12 + note_num_pos + 1  # add 1 for 'not rest'

		vector[total_index][iter_note_index_in_vector] = 1
		vector[total_index][measure_at_pos] = measure_num
		vector[total_index][measure_left_pos] = total_num_measure
		vector[total_index][duration_pos] = iter_duration  # Might want to introduce accum_duration


		partVector[total_index+vector_index] = vector


	return partVector, vector




def vectorize(part):
	measures = part.getElementsByClass('Measure')
	total_num_measure = len(measures)
	allNotes = part.recurse().notes
	vector = np.zeros([1, len(allNotes), vector_size])  # np.empty or np.zeros

	accum_duration = 0
	vector_index = 0
	measure_index = 0
	for measure in measures:
		allNotes = measure.recurse().notes
		if len(allNotes) == 0:
			measure_index += 1
			accum_duration+= 4
			continue

		for iter_item in allNotes:
			# vector[0][vector_index][0] = 1  # Show that it is not rest
			iter_note = None
			if type(iter_item) is note.Note:
				iter_note = iter_item
			elif type(iter_item) is chord.Chord:
				iter_note = iter_item[-1]   # get the hightst picth in the chord for now. We will get all notes in chord in the future
			elif type(iter_item) is note.Rest:
				# vector[vector_index] = 1  # Might vector[vector_index][0] = 1
				continue
			else:
				print("Type is neighther note nor chord")

			iter_name = iter_note.name
			iter_octave = iter_note.octave
			iter_duration = iter_note.duration.quarterLength
			note_num_pos = name_to_number(iter_name)

			if(iter_octave == 0 and note_pos < 0):
				print("Invalid Note")
				continue

			if(iter_octave > 9):
				print("Octave is too high")

			# iter_note_index_in_vector = iter_octave * 12 + note_num_pos + 1  # add 1 for 'not rest'
			iter_note_index_in_vector = iter_octave * 12 + note_num_pos
			vector[0][vector_index][iter_note_index_in_vector] = 1
			# vector[0][vector_index][measure_at_pos] = measure_index
			# vector[0][vector_index][measure_left_pos] = total_num_measure - measure_index - 1
			# vector[0][vector_index][duration_pos] = iter_duration  # Might want to introduce accum_duration

			vector_index += 1

		measure_index += 1

	return vector



def name_to_number(name):
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
		print("name_to_number is not in A to G")

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

# c = {x:allDuration.count(x) for x in allDuration}

# summer = converter.parse("Summer_Joe_Hisaishi.mxl")
# part1 = summer.getElementsByClass('Part')[0]
# measures1 = part1.getElementsByClass('Measure')
# allNotes1 = measures1.recurse().notes
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
0.0625, 1/10, 1/12, 0.125, 1/6, 0.25, 1/3, 0.5, 0.75, 1.0, 1.5, 1.75, 2.0, 3.0, 4.0, 6.0
"""