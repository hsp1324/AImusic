import pysynth
import random as rd
import scales as sc
import os.path
import beat as bt
from pydub import AudioSegment
import sys, getopt

# 끝날때 마무리, 높음은 나오면 좋을 것 같아
#relative_next_note_index: how far the note away from do on the major

# For more info, read octave_adjust in scales.py
octave_adjust = sc.octave_adjust

# Dinimished code cannot be handled yet
def createMelody(process, measure_beat_size, loop=1):
	notes = []
	beats = bt.Beat(process, loop, measure_beat_size=1)
	relative_notes_index = []
	first_chord = process[0]
	
	keys = sc.make_scale(first_chord[0],first_chord[1])
	print('main keys: ', keys)
	beats = beats.beats
	print("------Generating Melody------")
	for loop_index in range(loop):
		for chord_index in range(len(process)):
			chord = process[chord_index]
			print("chord:", chord)
			print("measure_beat:", beats[chord_index])
			# Make melody according to beats
			
			scale = sc.make_scale(chord[0],chord[1])   # I need to fix it!!!
			measure_notes = generate_notes(process, chord_index, beats[chord_index], relative_notes_index, keys, notes)
			print("measure_notes:", measure_notes)
			# relative_measure_notes_index = make_relative_notes_index(scale, measure_notes)
			notes.append(measure_notes)
			# relative_notes_index.append(relative_measure_notes_index)

			print("-------------" + str(chord_index+1 + len(process)*loop_index) + "/" + str(len(process) + len(process)*loop) + ("-------------"))

	print('len(notes) / len(beats): ', len(notes), ' / ', len(beats))
	melody = zip_note_beat(notes, beats)
	return melody




# Currently  I am making first two measure melody independent and make the rest of measures melody to be similar as the first two melody.
def generate_notes(process, chord_index, measure_beat, relative_notes_index, keys, notes):
	# Make Note accordingly
	chord = process[chord_index]
	scale = sc.make_scale(chord[0],chord[1])
	accum_beat = 0
	measure_notes = []
	relative_measure_notes_index = []
	prev_key = None
	prev_note = None
	for iter_beat_index in range(len(measure_beat)):
		do = scale[0+octave_adjust]
		mi = scale[2+octave_adjust]
		so = scale[4+octave_adjust]
		next_note = None
		probability = [0]*len(keys)

		if(chord_index == 0 or chord_index == 1):  # make first measure random8
			if(accum_beat == 0): # start with one of the tride note
				next_note = rd.choice([do,mi,so])
			else:
				apply_up_down_tendancy(probability, measure_notes, keys)
				apply_tride_notes_probability(probability, scale, keys, accum_beat)

				# Tring to repeat the melody within current  measure.... working on it
				# if(accum_beat is 0.5):
				# 	first_note = measure_notes[0]
				# 	first_note_index = keys.index(first_note)
				# 	probability[first_note_index] += 5

				next_note = rd.choices(keys, weights=probability, k=1)[0]
				

		else:  # make the rest of the measures imitating the first measure
			try:
				comparitive_note_index = relative_notes_index[chord_index%2][iter_beat_index]
				keys_index = keys.index(do) + comparitive_note_index
				comparitive_note = keys[keys_index]
				if(comparitive_note in scale):
					probability[keys_index] += 20
				else:
					probability[keys_index] += 10
			except:
				pass


			##### got it from first measure######
			if prev_note != None:
				prev_note_index = keys.index(prev_note)
				apply_up_down_tendancy(probability, measure_notes, keys)
				apply_tride_notes_probability(probability, scale, keys, accum_beat)
			##### got it from first measure######

			# print(chord[0],' probability:', probability)
			# print(chord[0],' scale:', scale)
			next_note = rd.choices(keys, weights=probability, k=1)[0]

		prev_note = next_note
		accum_beat += 1.0 / measure_beat[iter_beat_index]
		relative_next_note_index = keys.index(next_note) - keys.index(do)
		relative_measure_notes_index.append(relative_next_note_index)
		measure_notes.append(next_note)
	relative_notes_index.append(relative_measure_notes_index)
	return measure_notes




def generate_measure_beat(measure_beat_size):
	beat_choice = [4,8]
	accumulated_beat = 0
	measure_beat = []
	probability = [1]*2
	while(accumulated_beat < measure_beat_size):
		if(accumulated_beat >= measure_beat_size - 1/8):
			next_beat = 8
		else:
			### Tried to repeat the beats ###
			# if(accumulated_beat == 0.5):
			# 	first_beat = measure_beat[0]
			# 	first_beat_index = beat_choice.index(first_beat)
			# 	probability[first_beat_index] += 1
			next_beat = rd.choices(beat_choice, weights=probability, k=1)[0]
		measure_beat.append(next_beat)
		accumulated_beat += 1.0 / next_beat

	return measure_beat



def generate_relative_beat(index, beats):
	# 반전  check
	# 나누기
	# 세잎단음표
	# 앞붙점 뒷붙점
	original_beat = beats[index-2]
	return_beat = original_beat

	##### make a single beat triplet ######
	# select_beat_index = rd.randint(0,len(original_beat)-1)
	# return_beat = make_triplet(select_beat_index, original_beat)
	##### make a single beat triplet ######


	##### reversing Beat #####
	can_reverse = False
	reverse_start_index = 0
	accum_beat = 0
	for index in range(len(return_beat)):
		accum_beat += 1/return_beat[index]
		if(accum_beat == 1/2):
			can_reverse = True
			reverse_start_index = index
			break
	if(can_reverse == True):
		return_beat = reversing_half_beat(reverse_start_index, return_beat)
	##### reversing Beat #####


	return return_beat



def reversing_half_beat(center_index, original_beat):
	return_beat = []
	reverse_start_index = center_index
	while(reverse_start_index >= 0):
		return_beat.append(original_beat[reverse_start_index])
		reverse_start_index -= 1

	end_index = len(original_beat)-1
	while(end_index > center_index):
		return_beat.append(original_beat[end_index])
		end_index -= 1

	return return_beat


def make_triplet(index, beat):
	index_beat = beat[index]
	new_beat = []
	if index == len(beat)-1:
		new_beat = beat[:index] + [index_beat*3]*3
	else:
		new_beat = beat[:index] + [index_beat*3]*3 + beat[index+1:]
	return new_beat


def generate_beats(process, measure_beat_size):
	beats = []
	for i in range(len(process)):
		if(i == 0 or i == 1):
			measure_beat = generate_measure_beat(measure_beat_size)
		else:
			measure_beat = generate_relative_beat(i, beats)
		beats.append(measure_beat)
	return beats



def apply_up_down_tendancy(probability, measure_notes, keys):
	prev_note = measure_notes[-1]
	prev_note_index = keys.index(prev_note)

	probability[prev_note_index] += 5
	# increase left, right notes' probability of prev_note
	if(prev_note_index == 0):
		probability[prev_note_index+1] += 5
	elif(prev_note_index == len(keys)-1):
		probability[prev_note_index-1] += 5
	else:
		probability[prev_note_index+1] += 5
		probability[prev_note_index-1] += 5

	# increase left, right notes' probability of prev_note if past two steps were increment or decrement
	if len(measure_notes) >=2:
		prev_prev_note = measure_notes[-2]
		prev_prev_note_index = keys.index(prev_prev_note)
		if(prev_note_index - prev_prev_note_index == 1 and prev_note_index != len(keys)-1):
			probability[prev_note_index+1] += 5
		elif(prev_prev_note_index - prev_note_index == 1 and prev_note_index != 0):
			probability[prev_note_index-1] += 5
	return None




def apply_tride_notes_probability(probability, scale, keys, accum_beat):
	do = scale[0+octave_adjust]
	mi = scale[2+octave_adjust]
	so = scale[4+octave_adjust]
	soD = keys[keys.index(do)-3+octave_adjust]
	miD = keys[keys.index(do)-5+octave_adjust]
	doD = keys[keys.index(do)-7+octave_adjust]
	for note in [doD, miD, soD, do, mi, so]:
		if(note in keys):
			note_index = keys.index(note)
			probability[note_index] += 5
		if(accum_beat in [0, 0.25,0.5,0.75]): # Add extrat weight every 1/4 tik
			probability[note_index] += 20
	return None



def zip_note_beat(notes, beats):
	melody = []
	for i in zip(notes,beats):
		melody.extend(tuple(zip(i[0],i[1])))
	return melody



def make_last_note_do(notes):
	dos = ['c3', 'c', 'c5']
	do_dist = [abs(c_major_scale.index(notes[-1][-2]) - c_major_scale.index('c3')),
			   abs(c_major_scale.index(notes[-1][-2]) - c_major_scale.index('c')),
			   abs(c_major_scale.index(notes[-1][-2]) - c_major_scale.index('c5'))]
	do_max_index = do_dist.index(min(do_dist))
	notes[-1][-1] = dos[do_max_index]
	return notes







c_major_scale = ['c3','d3','e3','f3','g3','a3','b3','c','d','e','f','g','a','b','c5','d5','e5','f5','g5','a5','b5',]
d_major_scale = ['d','e','f#','g','']



test = [['c*',4],['e*',4],['g*',2],['c5*',2],['r',1]]

base = [['c3*',4] , ['g3*',4] , ['c4*',4], ['r',4],
		['g2*',4], ['d3*',4] , ['g3*',4] , ['r',4],
		['a2*',4], ['e3*',4] , ['a3*',4] , ['r',4],
		['e2*',4], ['b2*',4], ['e3*',4] , ['r',4],
		['f2*',4], ['c3*',4] , ['f3*',4] , ['r',4],
		['c2*',4], ['g2*',4], ['c3*',4] , ['r',4],
		['f2*',4], ['c3*',4] , ['f3*',4] , ['r',4],
		['g2*',4], ['d3*',4] , ['g3*',4] , ['r',4]]

smpl_melody = [['c',4],['d',4],['e',4],['f',4],['g',4],['f',4],['e',4],['d',4],
			   ['c',4],['d',4],['e',4],['f',4],['g',4],['f',4],['e',4],['d',4],
			   ['c',4],['d',4],['e',4],['f',4],['g',4],['f',4],['e',4],['d',4],
			   ['c',4],['d',4],['e',4],['f',4],['g',4],['f',4],['e',4],['d',4]]

base0 = [['c3*',4], ['g3*',4], ['c4*',4], ['r',4],
		 ['g2*',4], ['d3*',4], ['g3*',4], ['r',4],
		 ['a2*',4], ['e3*',4], ['a3*',4], ['r',4],
		 ['e2*',4], ['b2*',4], ['e3*',4], ['r',4],
		 ['f2*',4], ['c3*',4], ['f3*',4], ['r',4],
		 ['c2*',4], ['g2*',4], ['c3*',4], ['r',4],
		 ['f2*',4], ['c3*',4], ['f3*',4], ['r',4],
		 ['g2*',4], ['d3*',4], ['g3*',4], ['r',4]]

base1_1 = [['c3*',2], ['g3*',4], ['g3*',4],
		   ['g2*',2], ['g3*',4], ['g3*',4],
		   ['f2*',2], ['f3*',4], ['f3*',4],
		   ['g2*',2], ['g3*',4], ['g3*',4]]

base1_2 = [['r',2], ['e3*',4], ['e3*',4],
		   ['r',2], ['e3*',4], ['e3*',4],
		   ['r',2], ['c3*',4], ['c3*',4],
		   ['r',2], ['d3*',4], ['d3*',4]]

process0 = [('c', 'major'), ('g','major'), ('a','minor'),('e','minor'),('f','major'),('c','major'),('f','major'),('g','major')]


# Love is an open door chord
process1 = [('c', 'major'), ('e','minor'), ('f','major'),('g','major'),
			('c', 'major'), ('e','minor'), ('f','major'),('g','major'),
			('c', 'major'), ('e','minor'), ('f','major'),('g','major'),
			('c', 'major'), ('e','minor'), ('a','minor'),('g','major'),
			('a', 'minor'), ('a','minor'), ('c','major'),('c','major'),
			('d', 'minor'), ('d','minor'), ('f','major'),('f','major'),
			('c', 'major'), ('e','minor'), ('d','minor'),('f','major'),
			('c', 'major'), ('e','minor'), ('d','minor'),('f','major'),
			('c', 'major'), ('e','minor'), ('d','minor'),('f','major'),
			('c', 'major'), ('e','minor'), ('f','major'),('g','major')]


process2 = [('f', 'major'), ('e','major'), ('a','minor'),('g','minor'),
			('f', 'major'), ('e','major'), ('a','minor'),('g','minor'),
			('f', 'major'), ('e','major'), ('a','minor'),('g','minor'),
			('f', 'major'), ('e','major'), ('a','minor'),('g','minor')]

process3 = [('c', 'major'), ('g','major'), ('a','minor'),('c','major'),
			('f', 'major'), ('g','major'), ('c','major'),('g','major'),
			('c', 'major'), ('g','major'), ('a','minor'),('f','major'),
			('d', 'minor'), ('g','major'), ('c','major'),('c','major')]


process4 = [('d', 'major'), ('a','major'), ('b','minor'),('f#','minor'),
			('g', 'major'), ('e','major'), ('a','major'),('a','major'),
			('d', 'major'), ('a','major'), ('b','minor'),('f#','minor'),
			('g', 'major'), ('a','major'), ('d','major'),('d','major')]

recommend_list = ['Canon', 'Love is an open door']
processes = [process0, process1, process2, process3, process4]



def main(argv):

	inputfile = ''
	outputfile = ''
	process_name = ''
	try:
		opts, args = getopt.getopt(argv,"hp:t:l:",["ifile=","ofile=","lfile="])
	except getopt.GetoptError:
		print('Error test.py -p <base> -t <beat> -l <loop>')
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print('test.py -p <process> -t <tempo>')
			print("Cannon - process0 - 1")
			print("Love is an open door - process1 - 1/2")
			print("R&B - process2 - 1")
			print("joy1 - process3 - 1")
			print("joy2 - process4 - 1")
		
			sys.exit()
		elif opt in ("-p", "--ifile"):
			process = eval(arg)
			process_name = arg
		elif opt in ("-t", "--ofile"):
			tempo = eval(arg)
		elif opt in ("-l", "--lfile"):
			loop = eval(arg)



	new_melody = createMelody(process, tempo, loop=loop)
	if process_name == 'process0':
		new_base = sc.create_base0(process*loop, "Canon")
	elif process_name == 'process2':
		new_base = sc.create_base1(process*loop, "Love_is_an_open_door")
	elif process_name == 'process3':
		new_base = sc.create_base0(process*loop, "R&B")
	elif process_name == 'process4':
		new_base = sc.create_base0(process*loop, "Canon")
	elif process_name == 'process5':
		new_base = sc.create_base0(process*loop, "Canon")


	# creating file name
	index = 0
	mixed_filename = 'rangeOut'
	for i in range(1,100):
		if(not os.path.isfile('testSong/' + process_name + '_' + str(i) + '.wav')):
			index = i
			mixed_filename = 'testSong/' + process_name + '_' + str(i) + '.wav'
			break

	melody_name = "melody/melody" + process_name[-1] +  "_" + str(index) + ".wav"
	pysynth.make_wav(new_melody, fn = melody_name)


	sound1 = AudioSegment.from_file(melody_name)
	sound2 = AudioSegment.from_file(new_base)

	combined = sound1.overlay(sound2)

	combined.export(mixed_filename, format='wav')



if __name__== "__main__":
  main(sys.argv[1:])




def generate_from_shell(process, tempo=1, loop=1):
	process_name = "shell_test"

	new_melody = createMelody(process, tempo, loop)
	new_base = sc.create_base0(process, "Canon")


	# creating file name
	index = 0
	mixed_filename = 'rangeOut'
	for i in range(1,100):
		if(not os.path.isfile('testSong/' + process_name + '_' + str(i) + '.wav')):
			index = i
			mixed_filename = 'testSong/' + process_name + '_' + str(i) + '.wav'
			break

	melody_name = "melody/melody" + process_name[-1] +  "_" + str(index) + ".wav"
	pysynth.make_wav(new_melody, fn = melody_name)


	sound1 = AudioSegment.from_file(melody_name)
	sound2 = AudioSegment.from_file(new_base)

	combined = sound1.overlay(sound2)

	combined.export(mixed_filename, format='wav')


 