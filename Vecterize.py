from music21 import *
import numpy as np

#c0 - b8
#vector size 12 * 9(number of notes) + 1(not rest) + 1(duration) + 1(measure at) + 1(measure left) + 1(duration so far)


vector_size = 1 + 12*9 + 1 + 1 + 1
measure_at_pos = 1 + 12*9
measure_left_pos = measure_at_pos + 1
duration_pos = measure_left_pos + 1

def vectorizePart(part):
	measures = part.getElementsByClass('Measure')
	vector = np.zeros(len(measures))  # I am not sure Rest does count here
	
	for measure_index in range(len(measures)):
		iter_measure = measures[measure_index]
		measure_vector = vectorizeMeasure(iter_measure)
		vector[measure_index] = measure_vector

	return vector



def vectorizeMeasure(measure, measure_num, total_num_measure):
	allNotes = measure.recurse().notes
	vector = np.zeros([vector_size, len(allNotes)])  # I am not sure Rest does count here

	accum_duration = 0
	for vector_index in range(len(allNotes)):
		iter_item = allNotes[vector_index]
		iter_note = None
		if type(iter_item) is note.Note:
			iter_note = iter_item
		elif type(iter_note) is chord.Chord:
			iter_note = iter_item[-1]   # get the hightst picth in the chord for now. We will get all notes in chord in the future
		elif type(iter_note) is note.Rest:
			vector[0] = 1
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

		vector[iter_note_index_in_vector] = 1
		vector[measure_at_pos] = measure_num
		vector[measure_left_pos] = total_num_measure
		vector[duration_pos] = accum_duration  # I am not sure this will increase.  Might cause bad overfitting

		accum_duration += iter_duration


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

