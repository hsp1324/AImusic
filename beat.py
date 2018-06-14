import random as rd
import music21 as m21

class Beat:
	def __init__(self, process, loop, measure_length=4):

		self.beats = []
		self.process = process
		self.loop = loop
		self.measure_length = measure_length


		for i in range(self.loop):
			repeat_range = rd.choice([0,2,4])
			self.repeat_beat(i, repeat_range=repeat_range)



	def repeat_beat(self, loop_index, repeat_range=0):

		# print("repeat_range: ", repeat_range)
		for measure_index in range(len(self.process)):
			# print('measure_index: ', measure_index)
			if(measure_index in range(repeat_range+1)):
				measure_beat = self.random_beat()
			else:
				measure_beat = self.generate_relative_beat(loop_index, measure_index, repeat_range)
			self.beats.append(measure_beat)
		return None


	# def generate_beats(self, process):
	# 	for i in range(len(process)):
	# 		if(i == 0 or i == 1):
	# 			measure_beat = self.random_beat(self.measure_length)
	# 		else:
	# 			measure_beat = self.generate_relative_beat(i, beats)
	# 		beats.append(measure_beat)
	# 	return None


	# Return a random measure beat
	def random_beat(self):
		beat_choice = [1.0, 0.5]
		accumulated_beat = 0
		measure_beat = []
		probability = [1]*2
		while(accumulated_beat < self.measure_length):
			if(accumulated_beat >= self.measure_length - 0.5):
				next_beat = 0.5
			else:
				### Tried to repeat the beats ###
				# if(accumulated_beat == 0.5):
				# 	first_beat = measure_beat[0]
				# 	first_beat_index = beat_choice.index(first_beat)
				# 	probability[first_beat_index] += 1
				next_beat = rd.choices(beat_choice, weights=probability, k=1)[0]
			measure_beat.append(next_beat)
			accumulated_beat += next_beat

		return measure_beat




	def generate_relative_beat(self, loop_index, measure_index, repeat_range):
		# 반전  check
		# 나누기
		# 세잎단음표
		# 앞붙점 뒷붙점

		print('measure_index: ', measure_index)
		print('len(beats): ', len(self.beats))
		if repeat_range == 0:
			original_beat = self.beats[loop_index*len(self.process)]
		else:
			original_beat = self.beats[loop_index*len(self.process) + measure_index%repeat_range]
		return_beat = original_beat


		# if(rd.choice([True, False])):
		# 	print('reverse')
		# 	return_beat = self.reversing_half_beat(return_beat)

		# if(rd.choice([True, False])):
		# 	print('mearge')
		# 	return_beat = self.merge_beat(return_beat)

		# if(rd.choice([True, False])):
		# 	print('break')
		# 	return_beat = self.break_beat(return_beat, degree=2)

		return return_beat



	def reversing_half_beat(self, original_beat):
		can_reverse = False
		reverse_start_index = 0
		accum_beat = 0
		for index in range(len(original_beat)):
			accum_beat += original_beat[index]
			if(accum_beat == self.measure_length/2):
				can_reverse = True
				reverse_start_index = index
				center_index = reverse_start_index
				break
		if(can_reverse == True):
			return_beat = []
			while(reverse_start_index >= 0):
				return_beat.append(original_beat[reverse_start_index])
				reverse_start_index -= 1

			end_index = len(original_beat)-1
			while(end_index > center_index):
				return_beat.append(original_beat[end_index])
				end_index -= 1
			return return_beat
		else:
			return original_beat


	def break_beat(self, beat, degree=2):
		select_beat_index = rd.randint(0,len(beat)-1)
		select_beat = beat[select_beat_index]
		new_beat = beat[:select_beat_index] + [select_beat/degree]*degree + beat[select_beat_index+1:]
		return new_beat



	def merge_beat(self, beat):
		merging_index = rd.choice(range(len(beat)-1))
		return_beat = beat[:merging_index] + \
					  [beat[merging_index] + beat[merging_index+1]] + \
					  beat[merging_index+2:]
		return return_beat





