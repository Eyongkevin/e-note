from tkinter import *
import fontList
from tkinter.colorchooser import askcolor         # opens windows default color dialog
class GuiFontFrame:
	fontFamily = 'Arial'
	fontStyle = ''
	fontSize = 10
	fontColor = 'black'
	underline = False
	ApplyToValue = ' '
	def __init__(self, parent = None):
		pass
	def createFontGui(self):
		self.makeSettings()
		popup=Toplevel()		
		self.setWindowPositionAndSize(popup)
		popup.resizable(0,0)
		popup.attributes("-toolwindow",1)		#Remove the top minmize/mazimize button
		#popup.attributes("-topmost",True)      #always keep this wondow on the top all windows.
		popup.lift(self)                         #always keep this window on top it parent widnow( the contrary is '.lower(self))
		popup.title(self.title)
		self.makeFontWinget(popup)
		self.makeFontStyleWinget(popup)
		self.makeFontSizeWinget(popup)
		self.makeFontColor(popup)
		self.makeRadioButton(popup)
		self.makeReviewSample(popup)
		self.makeOkCancelButton(popup)
		
		popup.focus_set()
		popup.grab_set()
		popup.wait_window()
		
		
	def makeSettings(self):
		self.title = 'Font'
		self.windowX,self.windowY = 550,300
		self.fontFamilyList = fontList.returnFontList()
		self.fontStyleList = ['Regular','Italic','Bold','Bold Italic']
		self.fontSizeList = [8,9,10,11,12,14,16,18,20,22,24,26,28,36,48,72]
		self.RadioButtonList = ['All','Selected Only']
		self.ReturnFromGuiFontClass  = False
		
	def setWindowPositionAndSize(self, popup):
			x,y = self.returnWindowPosition()
			x,y = abs(x+30),abs(y+50)
			if y >477:
				y = 400
			popup.geometry("%dx%d+%d+%d" %(self.windowX,self.windowY,x,y))
			

	def makeFontWinget(self,obj):
		frame = Frame(obj, bd = 10)
		frame.grid(row = 1, column = 0)
		label = Label(frame, text="Font Family")
		label.config(fg = 'blue')
		label.config(height = 1)
		label.grid(row = 1, column = 0, sticky = W)
		
		self.listboxFont = Listbox(frame, height = 7)
		self.listboxFont.grid(row = 2, column = 0)
		for item in self.fontFamilyList: 
			self.listboxFont.insert(END, item)
			
		self.listboxFont.select_set(0)
		
		self.listboxFont.bind("<<ListboxSelect>>", self.getChoiceFontFamily)	
		sbar = Scrollbar(frame, orient = VERTICAL)
		sbar.config(command = self.listboxFont.yview) 			#synch scrollbar with canvas - on scrollbar scroll, scroll canvas
		self.listboxFont.config(yscrollcommand = sbar.set)		#synch canvas with scrollbar- on canvas scroll,scroll scrollbar
		sbar.grid(row = 2, column = 1,sticky = NS)
		
	def makeFontStyleWinget(self,obj):
		frame = Frame(obj, bd = 10)
		frame.grid(row = 1, column = 2)
		label = Label(frame, text="Font Style")
		label.config(fg = 'blue')
		label.config(height = 1)
		label.grid(row = 1, column = 1, sticky =W)
		
		self.listboxFontStyle = Listbox(frame, height = 7)
		self.listboxFontStyle.grid(row = 2, column = 1)
		for item in self.fontStyleList:
			self.listboxFontStyle.insert(END, item)
			
		self.listboxFontStyle.bind("<<ListboxSelect>>", self.getChoiceFontStyle)
		sbar = Scrollbar(frame, orient = VERTICAL)
		sbar.config(command = self.listboxFontStyle.yview) 			#synch scrollbar with canvas - on scrollbar scroll, scroll canvas
		self.listboxFontStyle.config(yscrollcommand = sbar.set)		#synch canvas with scrollbar- on canvas scroll,scroll scrollbar
		sbar.grid(row = 2, column = 2,sticky = NS)
		
	def makeFontSizeWinget(self,obj):
		frame = Frame(obj, bd = 10)
		frame.grid(row = 1, column = 3)
		label = Label(frame, text="Font Size")
		label.config(fg = 'blue')
		label.config(height = 1)
		label.grid(row = 1, column = 1, sticky =W)
		
		self.listboxFontSize = Listbox(frame, width = 6, height = 7)
		self.listboxFontSize.grid(row = 2, column = 1)
		for item in self.fontSizeList:
			self.listboxFontSize.insert(END, item)
			
		self.listboxFontSize.bind("<<ListboxSelect>>", self.getChoiceFontSize)
		sbar = Scrollbar(frame, orient = VERTICAL)
		sbar.config(command = self.listboxFontSize.yview) 			#synch scrollbar with canvas - on scrollbar scroll, scroll canvas
		self.listboxFontSize.config(yscrollcommand = sbar.set)		#synch canvas with scrollbar- on canvas scroll,scroll scrollbar
		sbar.grid(row = 2, column = 2,sticky = NS)
		
	def makeFontColor(self, obj):
		frame = Frame(obj, bd = 10)
		frame.grid(row = 1, column = 4)
		label = Label(frame, text="Font Color")
		label.config(fg = 'blue')
		label.config(height = 1)
		label.grid(row = 1, column = 0, sticky =W)
		
		Button(frame, text='Choose Color',bd = 3, width = 10, command = self.onSetColor).grid(row = 2, column = 0, sticky =W)
		

	def makeRadioButton(self, obj):
		frame = Frame(obj, bd = 10)
		group = LabelFrame(frame, text = 'Apply To', padx = 1, pady =1)
		group.config(fg = 'blue', cursor = 'circle', borderwidth = 1)
		group.grid()
		frame.grid(row = 2, column = 0)
		self.var = StringVar()
		for index, key in enumerate(self.RadioButtonList):
			Radiobutton(group, text = key,
							   command = self.onPressRadio,
							   variable = self.var,
							   value = key).grid(row = index+2,column = 0, sticky = W)
				
		self.var.set(key)
		self.ApplyToValue = key
		
	def makeReviewSample(self, obj):
		frame = Frame(obj, bd = 10, width = 100, height = 100)
		group = LabelFrame(frame, text = 'Review', padx = 1, pady =1)
		group.config(fg = 'blue', borderwidth = 1)
		group.grid()
		frame.grid(row = 2, column = 3)
		frame.grid_propagate(0)
		self.reviewLabel = Label(group, text ='AaBbYyZz' )
		self.fixReviewSample()
		self.reviewLabel.config(height = 3)
		self.reviewLabel.grid(row= 1, column = 1, sticky = 'nsew')
		
	def makeOkCancelButton(self,obj):
		frame = Frame(obj)
		frame.grid(row = 8, column = 2,  sticky = 'nsew')
		Button(frame, text='Ok',bd = 3, width = 10, command =lambda : self.onOk(obj)).grid(row = 1, column = 0, sticky =W)
		Button(frame, text='Cancel', bd = 3, width = 10, command = lambda : self.onCancel(obj)).grid(row = 1, column = 1, sticky =W)

	
	def fixReviewSample(self):	
			FontBuilder = (self.fontFamily,self.fontSize,self.fontStyle)
			self.reviewLabel.config(fg = self.fontColor, padx = 10, font = FontBuilder)

	"""
	------------------Calllback functnons-------------------------
	"""
	def onSetColor(self):
		color = askcolor()
		if color != (None,None):
			(other,self.fontColor) = color
			self.fixReviewSample()
	def onPressRadio(self):
		self.ApplyToValue = self.var.get()
		
	def onOk(self,obj):
		self.ReturnFromGuiFontClass = True
		obj.destroy()
	def onCancel(self, obj):
		self.ReturnFromGuiFontClass  = False
		obj.destroy()
		
	def getChoiceFontFamily(self, event = ' '):
		INDEX =self.listboxFont.curselection()
		self.fontFamily = self.fontFamilyList[INDEX[0]]
		self.fixReviewSample()

		
	def getChoiceFontStyle(self, event =''):
		INDEX =self.listboxFontStyle.curselection()
		if INDEX[0] == 0:
			self.fontStyle = ''
		else:
			self.fontStyle = self.fontStyleList[INDEX[0]].lower()
		self.fixReviewSample()
		
	def getChoiceFontSize(self, event = ' '):
		INDEX =self.listboxFontSize.curselection()
		self.fontSize = self.fontSizeList[INDEX[0]]
		self.fixReviewSample()

		
		
		
		
		
		