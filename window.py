from tkinter import *
import createMusic as cm

class Window(Frame):

	def __init__(self, master = None):
		Frame.__init__(self, master)

		self.master = master
		self.rootNote = None
		self.chord = None
		self.process = []
		self.rootNoteDropDown = None
		self.chordDropDown = None
		self.str_process = ""
		self.label_process = None
		self.manual_process = []
		self.recommend_process = []
		self.init__window()
	def init__window(self):
		rowIndex = 0

		self.master.title("GUI")
		self.pack(fill=BOTH, expand=1)

		# quitButton = Button(self, text="Quit", command=self.client_exit)
		# quitButton.place(x=0, y=0)
		self.makeMenu()

		self.label_process = Label(self, bg="cyan", text="Create your own music")
		self.label_process.grid(row=rowIndex, columnspan=200, sticky=W)
		rowIndex+=1



		label_key = Label(self, text="Key")
		label_key.grid(row=rowIndex, column=0, sticky=W)
		self.rootNoteDropDown = StringVar()
		rootNotes = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
		self.rootNoteDropDown.set(rootNotes[0])
		self.rootNoteDropDownObject = OptionMenu(self, self.rootNoteDropDown, *rootNotes, command=self.setRoot)
		self.rootNoteDropDownObject.grid(row=rowIndex, column=1, sticky=W)

		label_key = Label(self, text="Recommend")
		label_key.grid(row=rowIndex, column=2, sticky=W)
		recommendDropDown = StringVar()
		recommendDropDown.set(None)
		recommendDropDownObject = OptionMenu(self, recommendDropDown, *cm.recommend_list, command=self.select_recommend)
		recommendDropDownObject.grid(row=rowIndex, column=3, sticky=W)


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


		label_1 = Label(self, text="Save As")
		entry_1 = Entry(self)
		label_1.grid(row=rowIndex)
		entry_1.grid(row=rowIndex, column=1)
		rowIndex+=1



		quitButton = Button(self, text="Quit", command=exit)
		quitButton.grid(row=rowIndex)
		rowIndex+=1
		# label_1 = Label(self, text="Name")
		# entry_1 = Entry(self)
		# label_1.grid(row=0)
		# entry_1.grid(row=0, column=1)

		c = Checkbutton(self, text="test")
		c.grid(row=rowIndex)
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

	def setChord(self, chord):
		self.chord = chord


	def client_exit(self):
		exit()
		return None


	def addChord(self):
		#If recommend chord is displaying, do not modify manual chord
		if(self.process != self.manual_process): 
			self.process = self.manual_process
		else:
			rootNote = self.rootNoteDropDown.get()
			chord = self.chordDropDown.get()
			self.manual_process.append((rootNote, chord))
			self.process = self.manual_process
		self.str_process = self.make_str_process(self.process)
		self.label_process.configure(text=self.str_process)
		print("process: ", self.process)
		

	def deleteChord(self):
		#If recommend chord is displaying, do not modify manual chord
		if(self.process != self.manual_process): 
			self.process = self.manual_process
			self.str_process = self.make_str_process(self.process)
			self.label_process.configure(text=self.str_process)
		else:
			if(len(self.manual_process) > 1):
				self.manual_process.pop()
				self.str_process = self.make_str_process(self.manual_process)
				self.label_process.configure(text=self.str_process)
			elif(len(self.manual_process) == 1):
				self.manual_process = []
				self.str_process = ""
				self.label_process.configure(text="Create your own music")
			else:
				self.label_process.configure(text="Create your own music")
			self.process = self.manual_process


	def select_recommend(self, selection):
		index = cm.recommend_list.index(selection)
		self.recommend_process = cm.processes[index]
		self.process = self.recommend_process
		str_process = self.make_str_process(self.process)
		self.label_process.configure(text=str_process)



	def printName(self):
		print("Sun")


	def make_str_process(self, process):
		str_process = ""
		for chord in process:
			str_process = str_process + chord[0] + " " + chord[1] + ", "
		return str_process


root = Tk()
root.geometry("400x300")

app = Window(root)
root.mainloop()
