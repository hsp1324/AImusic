import pysynth
from mixfiles import mix_files
import random as rd

all_note1 = ['c','c#','d','d#','e','f','f#','g','g#','a','a#','b']
all_note2 = ['c','db','d','eb','e','f','gb','b','ab','a','bb','b']
c_diatonc_scale = ['c','d','e','f','g','a','b']


def whole_up(note):
	changed_note = None
	if(note == 'cb'):
		changed_note = 'db'
	elif(note == 'c'):
		changed_note = 'd'
	elif(note == 'c#'):
		changed_note = 'd#'
	elif(note == 'db'):
		changed_note = 'eb'
	elif(note == 'd'):
		changed_note = 'e'
	elif(note == 'd#'):
		changed_note = 'e#'
	elif(note == 'eb'):
		changed_note = 'f'
	elif(note == 'e'):
		changed_note = 'f#'
	elif(note == 'e#'):
		changed_note = 'g'
	elif(note == 'f'):
		changed_note = 'g'
	elif(note == 'fb'):
		changed_note = 'gb'
	elif(note == 'f#'):
		changed_note = 'g#'
	elif(note == 'gb'):
		changed_note = 'ab'
	elif(note == 'g'):
		changed_note = 'a'
	elif(note == 'g#'):
		changed_note = 'a#'
	elif(note == 'ab'):
		changed_note = 'bb'
	elif(note == 'a'):
		changed_note = 'b'
	elif(note == 'a#'):
		changed_note = 'b#'
	elif(note == 'bb'):
		changed_note = 'c'
	elif(note == 'b'):
		changed_note = 'c#'
	elif(note == 'b#'):
		changed_note = 'd'
	else:
		raise Exception('Not a scale')
	return changed_note


def half_up(note):
	changed_note = None
	if(note == 'cb'):
		changed_note = 'c'
	elif(note == 'c'):
		changed_note = 'c#'
	elif(note == 'c#'):
		changed_note = 'd'
	elif(note == 'db'):
		changed_note = 'd'
	elif(note == 'd'):
		changed_note = 'd#'
	elif(note == 'd#'):
		changed_note = 'e'
	elif(note == 'eb'):
		changed_note = 'e'
	elif(note == 'e'):
		changed_note = 'f'
	elif(note == 'e#'):
		changed_note = 'f#'
	elif(note == 'fb'):
		changed_note = 'f'
	elif(note == 'f'):
		changed_note = 'f#'
	elif(note == 'f#'):
		changed_note = 'g'
	elif(note == 'gb'):
		changed_note = 'g'
	elif(note == 'g'):
		changed_note = 'g#'
	elif(note == 'g#'):
		changed_note = 'a'
	elif(note == 'ab'):
		changed_note = 'a'
	elif(note == 'a'):
		changed_note = 'a#'
	elif(note == 'a#'):
		changed_note = 'b'
	elif(note == 'bb'):
		changed_note = 'b'
	elif(note == 'b'):
		changed_note = 'c'
	elif(note == 'b#'):
		changed_note = 'c#'
	else:
		raise Exception('Not a scale')
	return changed_note
	


def whole_down(note):
	changed_note = None
	if(note == 'cb'):
		changed_note = 'a'
	elif(note == 'c'):
		changed_note = 'bb'
	elif(note == 'c#'):
		changed_note = 'b'
	elif(note == 'db'):
		changed_note = 'b'
	elif(note == 'd'):
		changed_note = 'c'
	elif(note == 'd#'):
		changed_note = 'c#'
	elif(note == 'eb'):
		changed_note = 'db'
	elif(note == 'e'):
		changed_note = 'd'
	elif(note == 'e#'):
		changed_note = 'd#'
	elif(note == 'fb'):
		changed_note = 'd'
	elif(note == 'f'):
		changed_note = 'eb'
	elif(note == 'f#'):
		changed_note = 'e'
	elif(note == 'gb'):
		changed_note = 'fb'
	elif(note == 'g'):
		changed_note = 'f'
	elif(note == 'g#'):
		changed_note = 'f#'
	elif(note == 'ab'):
		changed_note = 'gb'
	elif(note == 'a'):
		changed_note = 'g'
	elif(note == 'a#'):
		changed_note = 'g#'
	elif(note == 'bb'):
		changed_note = 'ab'
	elif(note == 'b'):
		changed_note = 'a'
	elif(note == 'b#'):
		changed_note = 'a#'
	else:
		raise Exception('Not a scale')
	return changed_note



def half_down(note):
	changed_note = None
	if(note == 'cb'):
		changed_note = 'bb'
	elif(note == 'c'):
		changed_note = 'b'
	elif(note == 'c#'):
		changed_note = 'c'
	elif(note == 'db'):
		changed_note = 'c'
	elif(note == 'd'):
		changed_note = 'db'
	elif(note == 'd#'):
		changed_note = 'd'
	elif(note == 'eb'):
		changed_note = 'd'
	elif(note == 'e'):
		changed_note = 'eb'
	elif(note == 'e#'):
		changed_note = 'e'
	elif(note == 'fb'):
		changed_note = 'eb'
	elif(note == 'f'):
		changed_note = 'e'
	elif(note == 'f#'):
		changed_note = 'f'
	elif(note == 'gb'):
		changed_note = 'f'
	elif(note == 'g'):
		changed_note = 'gb'
	elif(note == 'g#'):
		changed_note = 'g'
	elif(note == 'ab'):
		changed_note = 'g'
	elif(note == 'a'):
		changed_note = 'ab'
	elif(note == 'a#'):
		changed_note = 'a'
	elif(note == 'bb'):
		changed_note = 'a'
	elif(note == 'b'):
		changed_note = 'bb'
	elif(note == 'b#'):
		changed_note = 'b'
	else:
		raise Exception('Not a scale')
	return changed_note



def make_scale(root, scale):
	keys = []
	if(root in all_note1):
		root_index = all_note1.index(root)
		keys = all_note1[root_index:] + [i+'5' for i in all_note1[:root_index]]
	elif(root in all_note2):
		root_index = all_note2.index(root)
		keys = all_note1[root_index:] + [i+'5' for i in all_note2[:root_index]]
	else:
		raise Exception('Not a key')

	scale_notes = []
	if(scale == 'major'):
		scale_notes = [keys[0],keys[2],keys[4],keys[5],keys[7],keys[9],keys[11]]
	elif(scale == 'minor'):
		scale_notes = [keys[0],keys[2],keys[3],keys[5],keys[7],keys[8],keys[10]]
	elif(scale == 'altered'):
		scale_notes = [keys[0],keys[1],keys[3],keys[4],keys[6],keys[8],keys[10]]
	elif(scale == 'diminished'):
		scale_notes = [keys[0],keys[2],keys[3],keys[5],keys[6],keys[8],keys[9],keys[11]]
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


def create_base1(process, name='new'):
	first_chord = process[0]
	root = first_chord[0]
	chord = first_chord[1]
	scale = make_scale(root, chord)
	base_1 = []
	base_2 = []
	for chord in process:
		scale = make_scale(chord[0],chord[1])
		do = scale[0]
		mi = scale[2]
		so = scale[4]
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
	mix_files("base/base_" + name + "_1.wav", "base/base_" + name + "_2.wav", "base/base_" + name + ".wav")
	return "base/base_" + name + ".wav"











# major = s.make_scale('a', 'major')
# beat = [4]*7
# melody = list(zip(major,beat))
# pysynth.make_wav(melody, fn = "test_aMajor.wav")


# major = s.make_scale('a#', 'major')
# beat = [4]*7
# melody = list(zip(major,beat))
# pysynth.make_wav(melody, fn = "test_a#Major.wav")


# major = s.make_scale('b', 'major')
# beat = [4]*7
# melody = list(zip(major,beat))
# pysynth.make_wav(melody, fn = "test_bMajor.wav")


# major = s.make_scale('c', 'major')
# beat = [4]*7
# melody = list(zip(major,beat))
# pysynth.make_wav(melody, fn = "test_cMajor.wav")


# major = s.make_scale('c#', 'major')
# beat = [4]*7
# melody = list(zip(major,beat))
# pysynth.make_wav(melody, fn = "test_c#Major.wav")


# major = s.make_scale('d', 'major')
# beat = [4]*7
# melody = list(zip(major,beat))
# pysynth.make_wav(melody, fn = "test_dMajor.wav")


# major = s.make_scale('d#', 'major')
# beat = [4]*7
# melody = list(zip(major,beat))
# pysynth.make_wav(melody, fn = "test_d#Major.wav")


# major = s.make_scale('e', 'major')
# beat = [4]*7
# melody = list(zip(major,beat))
# pysynth.make_wav(melody, fn = "test_eMajor.wav")


# major = s.make_scale('f', 'major')
# beat = [4]*7
# melody = list(zip(major,beat))
# pysynth.make_wav(melody, fn = "test_fMajor.wav")


# major = s.make_scale('f#', 'major')
# beat = [4]*7
# melody = list(zip(major,beat))
# pysynth.make_wav(melody, fn = "test_f#Major.wav") 


# major = s.make_scale('g', 'major')
# beat = [4]*7
# melody = list(zip(major,beat))
# pysynth.make_wav(melody, fn = "test_gMajor.wav")


# major = s.make_scale('g#', 'major')
# beat = [4]*7
# melody = list(zip(major,beat))
# pysynth.make_wav(melody, fn = "test_g#Major.wav")
