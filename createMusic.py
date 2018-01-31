import pysynth
from mixfiles import mix_files
import random as rd
import scales as sc
import os.path
from pydub import AudioSegment
import sys, getopt


cMajor = ['c','e','g']
cMinor = ['c','eb','g']
dMajor = ['d','f#','a']
dMinor = ['d','f','a']
eMajor = ['e','g#','b']
eMinor = ['e','g','b']
fMajor = ['f','a','c']
fMinor = ['f','ab','c']
gMajor = ['g','b','d']
gMinor = ['g','bb','d']
aMajor = ['a','c#','e']
aMinor = ['a','c','e']
bMajor = ['b','d#','f#']
bMinor = ['b','db','f#']

new_melody = [[rd.choice(cMajor),4], [rd.choice(cMajor),4], [rd.choice(cMajor),4], [rd.choice(cMajor),4], 
			  [rd.choice(gMajor),4], [rd.choice(gMajor),4], [rd.choice(gMajor),4], [rd.choice([rd.choice(gMajor) ,'r']),4], 
			  [rd.choice(aMinor),4], [rd.choice(aMinor),4], [rd.choice(aMinor),4], [rd.choice(aMinor),4], 
			  [rd.choice(eMinor),4], [rd.choice(eMinor),4], [rd.choice(eMinor),4], ['r',4], 
			  [rd.choice(fMajor),4], [rd.choice(fMajor),4], [rd.choice(fMajor),4], [rd.choice(fMajor),4], 
			  [rd.choice(cMajor),4], [rd.choice(cMajor),4], [rd.choice(cMajor),4], [rd.choice([rd.choice(cMajor) ,'r']),4], 
			  [rd.choice(fMajor),4], [rd.choice(fMajor),4], [rd.choice(fMajor),4], [rd.choice(fMajor),4], 
			  [rd.choice(gMajor),4], [rd.choice(gMajor),4], [rd.choice(gMajor),4], ['r',4]]


new_melody2 =[[rd.choice(cMajor),4], [rd.choice(cMajor),4], [rd.choice(cMajor),4], [rd.choice(cMajor),4], 
			  [rd.choice(gMajor),4], [rd.choice(gMajor),4], [rd.choice(gMajor),4], [rd.choice([rd.choice(gMajor) ,'r']),4], 
			  [rd.choice(aMinor),4], [rd.choice(aMinor),4], [rd.choice(aMinor),4], [rd.choice(aMinor),4], 
			  [rd.choice(eMinor),4], [rd.choice(eMinor),4], [rd.choice(eMinor),4], ['r',4], 
			  [rd.choice(fMajor),4], [rd.choice(fMajor),4], [rd.choice(fMajor),4], [rd.choice(fMajor),4], 
			  [rd.choice(cMajor),4], [rd.choice(cMajor),4], [rd.choice(cMajor),4], [rd.choice([rd.choice(cMajor) ,'r']),4], 
			  [rd.choice(fMajor),4], [rd.choice(fMajor),4], [rd.choice(fMajor),4], [rd.choice(fMajor),4], 
			  [rd.choice(gMajor),4], [rd.choice(gMajor),4], [rd.choice(gMajor),4], ['r',4]]



process = [('c', 'major'), ('g','major'), ('a','minor'),('e','minor'),('f','major'),('c','major'),('f','major'),('g','major')]

# For more info, read octave_adjust in scales.py
octave_adjust = sc.octave_adjust

# Dinimished code cannot be handled yet
def createMelody(process, whole_beat):
	notes = []
	beats = []
	relative_notes_index = []
	first_chord = process[0]
	
	keys = sc.make_scale(first_chord[0],first_chord[1])
	beats = make_beats(process, whole_beat)
	print("------Generating Melody------")
	for chord_index in range(len(process)):
		chord = process[chord_index]
		print("chord:", chord)
		print("measure_beat:", beats[chord_index])
		# Make melody according to beats
		
		scale = sc.make_scale(chord[0],chord[1])   # I need to fix it!!!
		measure_notes = make_notes(process, chord_index, beats[chord_index], relative_notes_index, keys, notes)
		print("measure_notes:", measure_notes)
		# relative_measure_notes_index = make_relative_notes_index(scale, measure_notes)
		notes.append(measure_notes)
		# relative_notes_index.append(relative_measure_notes_index)

		print("-------------" + str(chord_index+1) + "/" + str(len(process)) + ("-------------"))

	melody = zip_note_beat(notes, beats)
	return melody




# Currently  I am making first two measure melody independent and make the rest of measures melody to be similar as the first two melody.
def make_notes(process, chord_index, measure_beat, relative_notes_index, keys, notes):
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
			comparitive_note_index = relative_notes_index[chord_index%2][iter_beat_index]
			comparitive_note = scale[comparitive_note_index]
			if(comparitive_note in keys):
				keys_index = keys.index(comparitive_note)
				probability[keys_index] += 100

			##### got it from first measure######
			if prev_note != None:
				prev_note_index = keys.index(prev_note)
				apply_up_down_tendancy(probability, measure_notes, keys)
				apply_tride_notes_probability(probability, scale, keys, accum_beat)
			##### got it from first measure######


			next_note = rd.choices(keys, weights=probability, k=1)[0]

		prev_note = next_note
		accum_beat += 1.0 / measure_beat[iter_beat_index]
		relative_next_note_index = keys.index(next_note) - keys.index(do)
		relative_measure_notes_index.append(relative_next_note_index)
		measure_notes.append(next_note)
	relative_notes_index.append(relative_measure_notes_index)
	return measure_notes



# def make_relative_notes_index(scale, measure_notes):
# 	relative_measure_notes_index = []
# 	for note in measure_notes:
# 		if note not in scale:
# 			note = sc.enharmonic(note)
# 		if note not in scale:
# 			print('note: ', note)
# 			print('scale: ', scale)
# 			raise Exception('WHATWHATWHATWHATWHATWHATWHATWHAT')
# 		relative_next_note_index = scale.index(note)
# 		relative_measure_notes_index.append(relative_next_note_index)
# 	return relative_measure_notes_index








def generate_measure_beat(whole_beat):
	beat_choice = [4,8]
	accumulated_beat = 0
	measure_beat = []
	probability = [1]*2
	while(accumulated_beat < whole_beat):
		if(accumulated_beat >= whole_beat - 1/8):
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



def generate_relative_beat(i, beats):
	beat_type = beats[i%2]
	return beat_type



def make_beats(process, whole_beat):
	beats = []
	for i in range(len(process)):
		if(i == 0 or i == 1):
			measure_beat = generate_measure_beat(whole_beat)
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

process1 = [('c', 'major'), ('c','major'), ('f','major'),('g','major')]

# Love is an open door chord
process2 = [('c', 'major'), ('e','minor'), ('f','major'),('g','major'),
			('c', 'major'), ('e','minor'), ('f','major'),('g','major'),
			('c', 'major'), ('e','minor'), ('f','major'),('g','major'),
			('c', 'major'), ('e','minor'), ('a','minor'),('g','major'),
			('a', 'minor'), ('a','minor'), ('c','major'),('c','major'),
			('d', 'minor'), ('d','minor'), ('f','major'),('f','major'),
			('c', 'major'), ('e','minor'), ('d','minor'),('f','major'),
			('c', 'major'), ('e','minor'), ('d','minor'),('f','major'),
			('c', 'major'), ('e','minor'), ('d','minor'),('f','major'),
			('c', 'major'), ('e','minor'), ('f','major'),('g','major')]

process3 = [('f', 'major'), ('e','major'), ('a','minor'),('g','minor'),
			('f', 'major'), ('e','major'), ('a','minor'),('g','minor'),
			('f', 'major'), ('e','major'), ('a','minor'),('g','minor'),
			('f', 'major'), ('e','major'), ('a','minor'),('g','minor')]




def main(argv):

	inputfile = ''
	outputfile = ''
	process_name = ''
	try:
		opts, args = getopt.getopt(argv,"hp:t:",["ifile=","ofile="])
	except getopt.GetoptError:
		print('Error test.py -p <base> -t <beat>')
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print('test.py -p <process> -t <tempo>')
			print("Cannon - process0 - 1")
			print("Love is an open door - process2 - 1/2")
			print("R&B - process3 - 1")
		
			sys.exit()
		elif opt in ("-p", "--ifile"):
			process = eval(arg)
			process_name = arg
		elif opt in ("-t", "--ofile"):
			tempo = eval(arg)



	new_melody = createMelody(process, tempo)
	if process_name == 'process0':
		new_base = sc.create_base0(process, "Canon")
	elif process_name == 'process2':
		new_base = sc.create_base1(process, "Love_is_an_open_door")
	elif process_name == 'process3':
		new_base = sc.create_base0(process, "R&B")

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
 