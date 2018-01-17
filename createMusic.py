import pysynth
from mixfiles import mix_files
import random as rd
import scales as sc
import os.path

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


def createMelody():
	note = []
	beat = []
	for i in range(1,8*4+1):
		if(i%16 == 0):
			note.append('r')
			beat.append(4)
		elif(i%8 == 0):
			note.append(rd.choice(cMajor+['r']))
			beat.append(4)
		else:
			note.append(rd.choice(cMajor))
			beat.append(4)
	return list(zip(note,beat))



process = [('c', 'major'), ('g','major'), ('a','minor'),('e','minor'),('f','major'),('c','major'),('f','major'),('g','major')]


def createMelody2(process, whole_beat):
	notes = []
	beats = []
	relative_notes_index = []
	section_beat = []
	# process = [cMajor, gMajor, aMinor, eMinor, fMajor, cMajor, fMajor, gMajor]

	prev_section_note = []
	prev_chord = None
	prev_key = None

	for i in range(len(process)):

		# Make beat
		if(i == 0 or i == 1):
			section_beat = create_random_beat(whole_beat)
		else:
			section_beat = create_relative_beat(i, beats)
		beats.append(section_beat)
		chord = process[i]

		print("chord", chord)
		print("section_beat",section_beat)
		# Make Note accordingly
		section_note = create_notes(process, chord, section_beat, relative_notes_index, i)
		relative_section_note_index = create_relative_notes_index(chord, section_note)
		print("section_note", section_note)
		notes.append(section_note)
		relative_notes_index.append(relative_section_note_index)


	notes = make_last_note_do(notes)

	print("notes", notes)
	print("beats", beats)

	melody = zip_note_beat(notes, beats)
	return melody





def create_random_beat(whole_beat):
	# beats = []
	accumulated_beat = 0
	section_beat = []
	while(accumulated_beat < whole_beat):
		if(accumulated_beat >= 7/8):
			next_beat = 8
		else:
			next_beat = rd.choice([4,8])
		section_beat.append(next_beat)
		accumulated_beat += 1.0 / next_beat

	return section_beat



def create_relative_beat(i, beats):
	beat_type = beats[i%2]
	return beat_type



def create_notes(process, chord, section_beat, relative_notes_index, chord_index):
	# Make Note accordingly
	scale = sc.make_scale(chord[0],chord[1])
	root_index = c_major_scale.index(chord[0])
	keys = c_major_scale[root_index-5:root_index+5]
	accum_beat = 0
	section_note = []
	prev_key = None
	prev_note = None
	for iter_beat_index in range(len(section_beat)):
		do = scale[0]
		mi = scale[2]
		so = scale[4]
		soD = keys[keys.index(do)-3]
		miD = keys[keys.index(do)-5]
		next_note = None
		if(chord_index == 0 or chord_index == 1):  # make first measure random8
			probability = [1]*len(keys)
			if(accum_beat == 0):
				next_note = rd.choice([do,mi,so])
			else:
				prev_note_index = keys.index(prev_note)
				
				if(prev_note_index == 0):
					probability[prev_note_index+1] += 10
				elif(prev_note_index == len(keys)-1):
					probability[prev_note_index-1] += 10
				else:
					probability[prev_note_index+1] += 10
					probability[prev_note_index-1] += 10
				probability[prev_note_index] += 10
				do_index = keys.index(do)
				mi_index = keys.index(mi)
				so_index = keys.index(so)
				miD_index = keys.index(miD)
				soD_index = keys.index(soD)
				probability[do_index] += 10
				probability[mi_index] += 10
				probability[so_index] += 10
				probability[soD_index] += 10
				probability[miD_index] += 10

				if(accum_beat in [0, 0.25,0.5,0.75]): # Add extrat weight every 1/4 tik
					probability[do_index] += 10
					probability[mi_index] += 10
					probability[so_index] += 10
					probability[soD_index] += 10
					probability[miD_index] += 10

				next_note = rd.choices(keys, weights=probability, k=1)[0]
				
		else:  # make the rest of the measures imitating the first measure
			probability = [1]*len(keys)
			comparitive_note_index = relative_notes_index[chord_index%2][iter_beat_index]
			probability[comparitive_note_index] += 100

			##### got it from first measure######
			if prev_note != None:
				prev_note_index = keys.index(prev_note)
				
				if(prev_note_index == 0):
					probability[prev_note_index+1] += 10
				elif(prev_note_index == len(keys)-1):
					probability[prev_note_index-1] += 10
				else:
					probability[prev_note_index+1] += 10
					probability[prev_note_index-1] += 10
				probability[prev_note_index] += 10
				do_index = keys.index(do)
				mi_index = keys.index(mi)
				so_index = keys.index(so)
				miD_index = keys.index(miD)
				soD_index = keys.index(soD)
				probability[do_index] += 10
				probability[mi_index] += 10
				probability[so_index] += 10
				probability[soD_index] += 10
				probability[miD_index] += 10
			##### got it from first measure######


			next_note = rd.choices(keys, weights=probability, k=1)[0]

		prev_note = next_note
		accum_beat += section_beat[iter_beat_index]
		section_note.append(next_note)

	return section_note



def create_relative_notes_index(chord, section_note):
	root_index = c_major_scale.index(chord[0])
	keys = c_major_scale[root_index-5:root_index+5]
	relative_section_note_index = []
	for note in section_note:
		relative_next_note_index = keys.index(note)
		relative_section_note_index.append(relative_next_note_index)
	return relative_section_note_index



def zip_note_beat(notes, beats):
	melody = []
	for i in zip(notes,beats):
		print(i)
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


process = process2

new_melody = createMelody2(process, 1/2)
new_base = sc.create_base1(process, "Love_is_an_open_door")
# pysynth.make_wav(base1_1, boost = 1.5, fn = "base/base1_1.wav")
# pysynth.make_wav(base1_2, boost = 1.5, fn = "base/base1_2.wav")

# creating file name
index = 0
mixed_filename = 'rangeOut'
for i in range(1,100):
	if(not os.path.isfile('testSong/process2_' + str(i) + '.wav')):
		index = i
		mixed_filename = 'testSong/process2_' + str(i) + '.wav'
		break



pysynth.make_wav(new_melody, fn = "melody/melody2_" + str(index) + ".wav")
mix_files(new_base, "melody/melody2_" + str(index) + ".wav", mixed_filename)


# mixing base1, base2 and melody
# mix_files("base/base1_1.wav", "melody/melody1_" + str(index) + ".wav", mixed_filename)
# mix_files(mixed_filename, "base/base1_2.wav", "full.wav")




