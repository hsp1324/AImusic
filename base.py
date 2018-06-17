import scales as sc
from music21 import stream, note

octave_adjust = sc.octave_adjust

class Base:

	def __init__(self, process, loop=1, base_type=None):
		self.base = []
		self.loop = loop
		# self.create_base(base_type)
		self.first_chord = process[0]
		self.keys = sc.make_scale(self.first_chord[0], self.first_chord[1])

		self.base = self.create_base0(process, loop)


	def make_base(self, base):

		base_melody = stream.Stream()

		for itr_note in base:
			name = itr_note[0]
			duration = itr_note[1]
			if name == 'r':
				temp_note = note.Rest(type='quarter')
			else:
				temp_note = note.Note(name, quarterLength=duration)
			base_melody.append(temp_note)
		return base_melody


	############## Canon process base ##################
	def create_base0(self, process, loop, name='new'):
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
		for loop_index in range(loop):
			for chord in process:
				if first_chord:
					first_chord = False
					scale = sc.make_scale(chord[0], chord[1], 3)
				else:
					scale = sc.make_scale(chord[0], chord[1], 2)
				do = scale[0+octave_adjust]
				mi = scale[2+octave_adjust]
				so = scale[4+octave_adjust]
				do_octave = scale[7+octave_adjust]
				base_1.append((do,1))
				base_1.append((so,1))
				base_1.append((do_octave,1))
				base_1.append(('r',1))

		base_melody = self.make_base(base_1)

		return base_melody





	def create_base1(self, process, name='new'):
		base_1 = []
		base_2 = []
		for chord in process:
			scale = sc.make_scale(chord[0],chord[1], 3)
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
		return None





	def create_base2(self, process, name='new'):
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

		return None







