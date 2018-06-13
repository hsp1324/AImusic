import pysynth
import random as rd
from pydub import AudioSegment
import music21 as m21

all_note1 = ['c','c#','d','d#','e','f','f#','g','g#','a','a#','b']
all_note2 = ['c','db','d','eb','e','f','gb','g','ab','a','bb','b']
c_diatonc_scale = ['c','d','e','f','g','a','b']

def enharmonic(note):
	if(note in all_note1):
		index = all_note1.index(note)
		return all_note2[index]
	elif(note in all_note2):
		index = all_note2.index(note)
		return all_note1[index]
	else:
		raise Exception("There is no such", note, "exists")



# To adjust root.  scale_notes start from one octave down from root. 
# so root is scale_notes[octave_adjust(12)].
octave_adjust = 7

def make_scale(root, scale, octave=4):

	scale_notes = []
	# print('len:', len(keys), keys)
	if('major' is scale):
		new_scale = m21.scale.MajorScale(root)
		scale_notes = [str(p) for p in new_scale.getPitches(root + str(octave-1), root + str(octave+2))]

	elif('minor' is scale):
		new_scale = m21.scale.MinorScale(root)
		scale_notes = [str(p) for p in new_scale.getPitches(root + str(octave-1), root + str(octave+2))]

	return scale_notes





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


############## Canon process base ##################
def create_base0(process, name='new'):
	# base0 = [['c3*',4], ['g3*',4], ['c4*',4], ['r',4],
	# 		 ['g2*',4], ['d3*',4], ['g3*',4], ['r',4],
	# 		 ['a2*',4], ['e3*',4], ['a3*',4], ['r',4],
	# 		 ['e2*',4], ['b2*',4], ['e3*',4], ['r',4],
	# 		 ['f2*',4], ['c3*',4], ['f3*',4], ['r',4],
	# 		 ['c2*',4], ['g2*',4], ['c3*',4], ['r',4],
	# 		 ['f2*',4], ['c3*',4], ['f3*',4], ['r',4],
	# 		 ['g2*',4], ['d3*',4], ['g3*',4], ['r',4]]

	base_1 = []
	first_chord = True
	for chord in process:
		if first_chord:
			first_chord = False
			scale = make_scale(chord[0], chord[1], 3)
		else:
			scale = make_scale(chord[0], chord[1], 2)
		do = scale[0+octave_adjust]
		mi = scale[2+octave_adjust]
		so = scale[4+octave_adjust]
		do_octave = scale[7+octave_adjust]
		base_1.append((do+'*',4))
		base_1.append((so+'*',4))
		base_1.append((do_octave+'*',4))
		base_1.append(('r',4))

	final_name = "base/base_" + name + ".wav"
	pysynth.make_wav(base_1, boost = 1.5, fn = final_name)
	return final_name





def create_base1(process, name='new'):
	base_1 = []
	base_2 = []
	for chord in process:
		scale = make_scale(chord[0],chord[1], 3)
		do = scale[0+octave_adjust]
		mi = scale[2+octave_adjust]
		so = scale[4+octave_adjust]
		base_1.append((do+'*',8))
		base_1.append(('r',8))
		base_1.append((so+'*',8))
		base_1.append(('r',8))
		base_2.append(('r',8))
		base_2.append(('r',8))
		base_2.append((mi+'*',8))
		base_2.append(('r',8))
	##### Tried to make last chord different as a ending chord #####
	# last_chord = process[-1]
	# last_scale = make_scale(last_chord[0],last_chord[1])
	# do = last_scale[0]
	# mi = last_scale[2]
	# so = last_scale[4]
	# base_1.append((so,8))
	# base_1.append(('r',8))
	# base_1.append((mi,8))
	# base_1.append(('r',8))
	# base_1.append((do,4))
	# base_2.append((mi,8))
	# base_2.append(('r',8))
	# base_2.append((do,8))
	# base_2.append(('r',8))

	pysynth.make_wav(base_1, boost = 1.5, fn = "base/base_" + name + "_1.wav")
	pysynth.make_wav(base_2, boost = 1.5, fn = "base/base_" + name + "_2.wav")

	sound1 = AudioSegment.from_file("base/base_" + name + "_1.wav")
	sound2 = AudioSegment.from_file("base/base_" + name + "_2.wav")
	combined = sound1.overlay(sound2)
	final_name = "base/base_" + name + ".wav"
	combined.export(final_name, format='wav')
	return final_name



