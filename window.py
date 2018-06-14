from tkinter import *
import createMusic as cm
from music21 import *



# make more space 



class Window(Frame):

	def __init__(self, master = None):
		Frame.__init__(self, master)

		self.master = master
		self.rootNote = None
		self.half = None
		self.chord = None
		self.process = []
		self.stream = None
		self.rootNoteDropDown = None
		self.sharpflatDropDown = None
		self.chordDropDown = None
		self.str_process = ""
		self.label_process = None
		self.manual_process = []
		self.recommend_process = []
		self.num_of_loop = 1
		self.label_loop = None
		self.label_status = None
		self.init__window()


	def init__window(self):
		rowIndex = 0

		self.master.title("GUI")
		self.pack(fill=BOTH, expand=1)

		# quitButton = Button(self, text="Quit", command=self.client_exit)
		# quitButton.place(x=0, y=0)
		self.makeMenu()

		label_title = Label(self, text="Hello AI Music Generator", font=("Helvetica", 20))
		label_title.grid(row=rowIndex, columnspan=5)
		rowIndex+=1






		label_key = Label(self, text="Key")
		label_key.grid(row=rowIndex, column=0, sticky=W)
		self.rootNoteDropDown = StringVar()
		rootNotes = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
		self.rootNoteDropDown.set(rootNotes[0])
		self.rootNoteDropDownObject = OptionMenu(self, self.rootNoteDropDown, *rootNotes, command=self.setRoot)
		self.rootNoteDropDownObject.grid(row=rowIndex, column=1, sticky=W)
		self.sharpflatDropDown = StringVar()
		sharpflat = ["None", "#", "b", "##", "bb"]
		self.sharpflatDropDown.set(sharpflat[0])
		self.sharpflatDropDownObject = OptionMenu(self, self.sharpflatDropDown, *sharpflat, command=self.setHalf)
		self.sharpflatDropDownObject.grid(row=rowIndex, column=2, sticky=W)




		label_key = Label(self, text="Recommend")
		label_key.grid(row=rowIndex, column=3, sticky=W)
		recommendDropDown = StringVar()
		recommendDropDown.set(None)
		recommendDropDownObject = OptionMenu(self, recommendDropDown, *cm.recommend_list, command=self.select_recommend)
		recommendDropDownObject.grid(row=rowIndex, column=4, sticky=W)
		rowIndex+=1


		label_chord = Label(self, text="Chord")
		label_chord.grid(row=rowIndex, column=0, sticky=W)
		self.chordDropDown = StringVar()
		chords = ['major', 'minor', 'aug', 'dim']
		self.chordDropDown.set(chords[0])
		self.chordDropDownObject = OptionMenu(self, self.chordDropDown, *chords, command=self.setChord)
		self.chordDropDownObject.grid(row=rowIndex, column=1, sticky=W)
		rowIndex+=1


		print("root: ", self.rootNote)
		print("chord: ", self.chord)


		addChordButton = Button(self, text="Add", command=self.addChord)
		addChordButton.grid(row=rowIndex, column=0)

		deleteChordButton = Button(self, text="Delete", command=self.deleteChord)
		deleteChordButton.grid(row=rowIndex, column=1)		
		rowIndex+=1

		self.label_loop = Label(self, text="Loop: " + str(self.num_of_loop))
		self.label_loop.grid(row=rowIndex, column=0, sticky=W)

		plusButton = Button(self, text="+", command=self.incrementLoop)
		plusButton.grid(row=rowIndex, column=1)
		minusButton = Button(self, text="-", command=self.decrementLoop)
		minusButton.grid(row=rowIndex, column=2)
	
		rowIndex+=1
		# label_1 = Label(self, text="Save As")
		# entry_1 = Entry(self)
		# label_1.grid(row=rowIndex)
		# entry_1.grid(row=rowIndex, column=1)
		# rowIndex+=1



		# label_1 = Label(self, text="Name")
		# entry_1 = Entry(self)
		# label_1.grid(row=0)
		# entry_1.grid(row=0, column=1)

		c = Checkbutton(self, text="test")
		c.grid(row=rowIndex)
		rowIndex+=1


		self.label_process = Label(self, text="Create your own music", anchor=W, justify=LEFT, width=28, borderwidth=10, highlightthickness=2, highlightbackground="black")
		self.label_process.grid(row=rowIndex, rowspan=5, columnspan=300, sticky=W)


		sb1 = Scrollbar(self)
		sb1.grid(row=2, column=2, columnspan=2)

		generateButton = Button(self, text="Generate", command=self.generateMusic)
		generateButton.grid(row=rowIndex, column=4)
		rowIndex+=5



		self.label_status = Label(self, bg="cyan", text="Waiting for input.....", anchor=CENTER, justify=CENTER, height=1, width=30)
		self.label_status.grid(row=rowIndex, columnspan=300, sticky=W)

		quitButton = Button(self, text="Quit", command=exit)
		quitButton.grid(row=rowIndex, column=4)
		rowIndex+=1



		generateButton = Button(self, text="Play", command=self.playMusic)
		generateButton.grid(row=rowIndex, column=0)

		generateButton = Button(self, text="Show Score", command=self.showScore)
		generateButton.grid(row=rowIndex, column=1)

		generateButton = Button(self, text="Save Midi", command=self.saveMusic)
		generateButton.grid(row=rowIndex, column=2)

		generateButton = Button(self, text="Save Score", command=self.saveScore)
		generateButton.grid(row=rowIndex, column=3)
		rowIndex+=1



	def makeMenu(self):
		menu = Menu(self.master)
		self.master.config(menu=menu)

		file = Menu(menu)

		file.add_command(label='Save', command=self.client_exit)
		file.add_command(label='Exit', command=self.client_exit)

		menu.add_cascade(label='File', menu=file)

		edit = Menu(menu)
		edit.add_command(label='Undo')
		menu.add_cascade(label='Edit', menu=edit)



	def setRoot(self, rootNote):
		self.rootNote = rootNote

	def setHalf(self, half):
		self.half = half


	def setChord(self, chord):
		self.chord = chord


	def client_exit(self):
		exit()
		return None


	def addChord(self):
		#If recommend chord is displaying, do not modify manual chord
		rootNote = self.rootNoteDropDown.get()
		chord = self.chordDropDown.get()
		half = self.sharpflatDropDown.get()
		if(half != "None"):
			rootNote = rootNote + half
		self.process.append((rootNote, chord))
		self.str_process = self.make_str_process()
		self.label_process.configure(text=self.str_process)
		

	def deleteChord(self):
		if(len(self.process) > 1):
			self.process.pop()
			self.str_process = self.make_str_process()
			self.label_process.configure(text=self.str_process)
		elif(len(self.process) == 1):
			self.process = []
			self.str_process = ""
			self.label_process.configure(text="Create your own music")
		else:
			self.label_process.configure(text="Create your own music")


	def select_recommend(self, selection):
		index = cm.recommend_list.index(selection)
		self.recommend_process = cm.processes[index]
		self.process = self.recommend_process[:]
		str_process = self.make_str_process()
		self.label_process.configure(text=str_process)


	def incrementLoop(self):
		self.num_of_loop += 1
		self.label_loop.configure(text="Loop: " + str(self.num_of_loop))


	def decrementLoop(self):
		self.num_of_loop -= 1
		if(self.num_of_loop < 1):
			self.num_of_loop = 1
		self.label_loop.configure(text="Loop: " + str(self.num_of_loop))

	def printName(self):
		print("Sun")


	def make_str_process(self):
		str_process = ""
		index = 0
		for chord in self.process:
			if(index != 0 and index%4 == 0):
				str_process = str_process + '\n'
			str_process = str_process + chord[0] + " " + chord[1] + ", "
			index += 1
		return str_process



	def generateMusic(self):
		self.label_status.configure(text="Generating..........", bg="yellow")
		self.label_status.update()
		try:
			process = self.process # * self.num_of_loop
			self.stream = cm.generate_from_shell(process, loop=self.num_of_loop)
			self.label_status.configure(text="Generating Done !!!", bg="lawn green")
		except:
			self.label_status.configure(text="Something Wrong !!!", bg="red")



	def playMusic(self):
		try:
			self.label_status.configure(text="Playing.....", bg="lawn green")
			self.stream.show('midi')
		except:
			self.label_status.configure(text="Something Wrong !!!", bg="red")



	def saveMusic(self):
		try:
			self.stream.write('midi', 'AIsong.mid')
			self.label_status.configure(text="Music is successfully saved", bg="lawn green")
		except:
			self.label_status.configure(text="Something Wrong !!!", bg="red")



	def saveScore(self):
		try:
			self.stream.write('xml', 'AIsong.xml')
			self.label_status.configure(text="The score is successfully saved", bg="lawn green")
		except:
			self.label_status.configure(text="Something Wrong !!!", bg="red")



	def showScore(self):
		try:
			self.label_status.configure(text="Showing.....", bg="lawn green")
			self.stream.show()
		except:
			self.label_status.configure(text="Something Wrong !!!", bg="red")






root = Tk()
root.geometry("500x400")

app = Window(root)
root.mainloop()
