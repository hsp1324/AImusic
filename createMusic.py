import pysynth
from mixfiles import mix_files
import random as rd
import scales as sc


c_major_scale = ['c3','d3','e3','f3','g3','a3','b3','c','d','e','f','g','a','b','c5','d5','e5','f5','g5','a5','b5',]
d_major_scale = ['d','e','f#','g','']

simple_beat = [2,4]


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





def createMelody2():
	notes = []
	beats = []
	relative_notes_index = []
	section_beat = []
	# process = [cMajor, gMajor, aMinor, eMinor, fMajor, cMajor, fMajor, gMajor]
	process = [('c', 'major'), ('g','major'), ('a','minor'),('e','minor'),('f','major'),('c','major'),('f','major'),('g','major')]


	prev_section_note = []
	prev_chord = None
	prev_key = None

	for chord in process:
		print("chord", chord)
		total_beat = 0
		scale = sc.make_scale(chord[0],chord[1])

		section_note = []
		relative_section_note_index = []

		relative_next_note_index = None
		root_index = c_major_scale.index(chord[0])
		keys = c_major_scale[root_index-5:root_index+5]

		# Make beat
		if(section_beat == []):
			section_beat = create_random_beat()
			print("section_beat",section_beat)


		# Make Note accordingly
		accum_beat = 0
		for iter_beat_index in range(len(section_beat)):
			do = scale[0]
			mi = scale[2]
			so = scale[4]
			soD = keys[keys.index(do)-3]
			miD = keys[keys.index(do)-5]
			next_note = None
			if(process.index(chord) == 0):  # make first measure random
				if(accum_beat in [0, 0.25,0.5,0.75]):  
					next_note = rd.choice([do,mi,so])
				else:
					prev_key_index = keys.index(prev_key)
					probability = [1]*len(keys)
					if(prev_key_index == 0):
						probability[prev_key_index+1] += 2
					elif(prev_key_index == len(keys)-1):
						probability[prev_key_index-1] += 2

					probability[prev_key_index] += 1
					do_index = keys.index(do)
					mi_index = keys.index(mi)
					so_index = keys.index(so)
					miD_index = keys.index(miD)
					soD_index = keys.index(soD)
					probability[do_index] += 1
					probability[mi_index] += 1
					probability[so_index] += 1
					probability[soD_index] += 1
					probability[miD_index] += 1
					next_note = rd.choices(keys, weights=probability, k=1)[0]
					

					# next_note = rd.choice(keys[:-1])
					# next_note = rd.choices([next_note, 'r'], weights=[0.9, 0.1], k=1)[0]

			else:  # make the rest of the measures imitating the first measure
				probability = [1]*len(keys)
				for iter_section_note_index in relative_notes_index:
					comparitive_note_index = iter_section_note_index[iter_beat_index]
					probability[comparitive_note_index] += 1000000
				next_note = rd.choices(keys, weights=probability, k=1)[0]

			relative_next_note_index = keys.index(next_note)
			accum_beat += section_beat[iter_beat_index]
			prev_key = next_note
			section_note.append(next_note)
			relative_section_note_index.append(relative_next_note_index)

		prev_section_note = section_note
		prev_chord = chord

		notes.append(section_note)
		beats.append(section_beat)
		relative_notes_index.append(relative_section_note_index)


	#always end with do
	dos = ['c3', 'c', 'c5']
	do_dist = [abs(c_major_scale.index(notes[-1][-2]) - c_major_scale.index('c3')),
			   abs(c_major_scale.index(notes[-1][-2]) - c_major_scale.index('c')),
			   abs(c_major_scale.index(notes[-1][-2]) - c_major_scale.index('c5'))]
	do_max_index = do_dist.index(min(do_dist))
	notes[-1][-1] = dos[do_max_index]


	melody = zip_note_beat(notes, beats)
	return melody





def create_random_beat():
	beats = []
	total_beat = 0
	section_beat = []
	while(total_beat < 0.99):
		next_beat = rd.choice([4,8])
		section_beat.append(next_beat)
		total_beat += 1.0 / next_beat
	return section_beat



def create_repeated_beat():
	return None



def create_notes():
	return None



def zip_note_beat(notes, beats):
	melody = []
	for i in zip(notes,beats):
		print(i)
		melody.extend(tuple(zip(i[0],i[1])))
	return melody




new_melody = createMelody2()

pysynth.make_wav(base, boost = 1.5, fn = "base/base15.wav")

pysynth.make_wav(new_melody, fn = "melody/new_melody6.wav")

mix_files("base/base15.wav", "melody/new_melody6.wav", "testSong/random6.wav")




