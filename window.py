from tkinter import *

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
		self.init__window()

	def init__window(self):
		rowIndex = 0

		self.master.title("GUI")
		self.pack(fill=BOTH, expand=1)

		# quitButton = Button(self, text="Quit", command=self.client_exit)
		# quitButton.place(x=0, y=0)
		self.makeMenu()

		self.label_process = Label(self, bg="cyan", text="Make your own music")
		self.label_process.grid(row=rowIndex, columnspan=6, sticky=W)
		rowIndex+=1
		label_1 = Label(self, text="Name")
		entry_1 = Entry(self)
		label_1.grid(row=rowIndex)
		entry_1.grid(row=rowIndex, column=1)
		rowIndex+=1

		label_2 = Label(self, text="me")
		entry_2 = Entry(self)
		label_2.grid(row=rowIndex)
		entry_2.grid(row=rowIndex, column=1)
		rowIndex+=1




		makeProcess = Text(self, width=50, height=1)
		# makeProcess.width(100)
		makeProcess.insert(END, "Select Chrod")
		# makeProcess.grid(row = 7)

		label_key = Label(self, text="Key")
		label_key.grid(row=rowIndex, column=0, sticky=W)

		self.rootNoteDropDown = StringVar()
		rootNotes = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
		self.rootNoteDropDown.set(rootNotes[0])
		self.rootNoteDropDownObject = OptionMenu(self, self.rootNoteDropDown, *rootNotes, command=self.setRoot)
		self.rootNoteDropDownObject.grid(row=rowIndex, column=1, sticky=W)
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
		addChordButton.grid(row=rowIndex)
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
		rootNote = self.rootNoteDropDown.get()
		chord = self.chordDropDown.get()
		self.process.append((rootNote, chord))
		self.str_process = self.str_process + rootNote + " " + chord + " "
		self.label_process.configure(text=self.str_process)
		print("process: ", self.process)
		


	def printName(self):
		print("Sun")



root = Tk()
root.geometry("400x300")

app = Window(root)
root.mainloop()
