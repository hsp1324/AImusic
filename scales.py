
import random as rd
import music21 as m21


# To adjust root.  scale_notes start from one octave down from root. 
# so root is scale_notes[octave_adjust(12)].
octave_adjust = 7

def make_scale(root, scale, octave=4):

	scale_notes = []
	if('major' == scale):
		new_scale = m21.scale.MajorScale(root)
		scale_notes = [str(p) for p in new_scale.getPitches(root + str(octave-1), root + str(octave+2))]

	elif('minor' == scale):
		new_scale = m21.scale.MinorScale(root)
		scale_notes = [str(p) for p in new_scale.getPitches(root + str(octave-1), root + str(octave+2))]
	print("scale_notes: ", scale_notes)
	return scale_notes

