# This Python file uses the following encoding: utf-8
from tkinter import *
from tkinter.filedialog import asksaveasfilename
from textEditorClass import ScrolledText
from menuClass import CreateMenuOperations
from GuiFont import GuiFontFrame
from textAccent import MakeAccentation
from tkinter.filedialog import askopenfilename    
from tkinter.simpledialog import askstring
import sys

class SimpleEditor(Frame, GuiFontFrame, MakeAccentation, CreateMenuOperations):
	setTagToTextCount = 0
	setWindowLocation = "%dx%d+%d+%d" %(661,405,290,173)
	
	def __init__(self, parent = None, file = None):
		Frame.__init__(self, parent)
		self.setDeleteWindowOption()
		self.setLocation()                   #position the window to the center of the screen.(most be call after the window has been created.)
		self.st = ScrolledText()             #create scrolledText obj
		self.menu= CreateMenuOperations()    #create menu obj
		self.createWidgets()                 #create menu
		self.setEditorTitle()
		self.master.title(self.editorTitle+' - Untitled')
		self.master.iconbitmap('icon.ico')   #not red Tk
		self.st.makewidgets()                #create text space
		self.st.settext()                    #set default text on text space
		self.createAccentation(self.st)      #create action for inserting accents,(eg í,ó,á,é,ú')
		
		self.rightClickEvent_Helper()        #set right click event for drop down menu popup on text area.
		
		
		self.bind_all('<Button-3>', self.onRightClickEvent)
		
		#self.after(5000, self.setLocation)
	


		
	def setDeleteWindowOption(self):
		self.master.protocol('WM_DELETE_WINDOW', self.checkOnWindowDelete_Helper) 
		
	def setLocation(self):
		self.master.geometry(self.setWindowLocation)
		
	def setEditorTitle(self):
		self.editorTitle = 'e~note'
		
	def setTitle(self,title):
		self.master.title(self.editorTitle+' - '+ title) 
		
	def quitWindow(self):
		sys.exit()
		
		"""
		this will create the top menu with it sub-menus
		"""
	def createWidgets(self):
		self.makeMenuBar()
			
	def makeMenuBar(self):
		self.menubar = Menu(self.master)
		self.master.config(menu=self.menubar)
		self.fileMenu()
		self.editMenu()
		self.searchMenu()
		self.formatMenu()
		self.InsertMenu()
		self.encodingMenu()
		self.HelpMenu()
	"""
	create menu 'file' and it sub-menus
	"""
	def fileMenu(self):
		pulldown = Menu(self.menubar, tearoff=False)
		pulldown.add_command(label='New..' , command=self.onNew , accelerator="Ctrl+N")
		pulldown.add_command(label='Open..' , command=self.onOpen , accelerator="Ctrl+O")
		pulldown.add_command(label='Save..' , command = self.onSave, accelerator="Ctrl+S")
		pulldown.add_command(label='Save as..', command=self.onSaveAs , accelerator="Ctrl+Alt+S")
		self.menubar.add_cascade(label='File', underline=0, menu=pulldown)
		
		#bind keyboard shortcuts
		self.bind_all("<Control-s>",self.onSave)
		self.bind_all("<Control-n>",self.onNew)
		self.bind_all("<Control-o>",self.onOpen)
		self.bind_all("<Control-Alt-s>",self.onSaveAs)
	"""
	create menu 'edit' and it sub-menus
	"""
	def editMenu(self):
		self.pulldown = Menu(self.menubar, tearoff=False, postcommand = self.enableOrDisableIterms)
		self.pulldown.add_command(label='Undo', command = self.onUndo, accelerator="Ctrl+U")
		self.pulldown.add_command(label='Redo', command = self.onRedo, accelerator="Ctrl+R" )
		self.pulldown.add_separator()
		self.pulldown.add_command(label='Copy', command =self.onCopy , accelerator="Ctrl+C")
		self.pulldown.add_command(label='Cut', command =self.CutText , accelerator="Ctrl+X")
		self.pulldown.add_command(label='Paste', command = self.onPaste, accelerator="Ctrl+V / Ctrl+P")
		self.pulldown.add_command(label='Select All',command = self.onSelectAll, accelerator="Ctrl+A")
		self.pulldown.add_separator()
		self.pulldown.add_command(label='Delete', command = self.onDelete, accelerator = 'Ctrl+D')
		self.pulldown.add_command(label='Delete All', command = self.onDeleteAll)
		self.menubar.add_cascade(label='Edit', underline=0, menu=self.pulldown)
		
		"""
		bind keyboard shortcuts
		------------
		by default,some keyboard shortcuts are already set by the OS, so setting them again here causes some minor bug
		eg 'control-d' in most OS is use to delete selected text. if i set it here again, this action might be called twice(the action defined by
		me, and that already defined by the OS. i need a way to stop the default action.)
		"""
		#self.bind_all("<Control-x>",self.CutText)
		self.bind_all("<Control-c>",self.onCopy)
		self.bind_all("<Control-p>",self.onPaste)
		self.bind_all("<Control-u>",self.onUndo)
		self.bind_all("<Control-r>",self.onRedo)
		self.bind_all("<Control-a>",self.onSelectAll)
		#self.bind_all("<Control-d>",self.onDelete)
		
	def searchMenu(self):
		pulldown = Menu(self.menubar, tearoff=False)
		pulldown.add_command(label='Find/Replace..' , command= self.onFind , accelerator="Ctrl+F")
		pulldown.add_separator()
		pulldown.add_command(label='Go to..', accelerator="Ctrl+G" , state = DISABLED)
		self.menubar.add_cascade(label='Search', underline=0, menu=pulldown)
		
		#bind keyboard shortcuts
		self.bind_all("<Control-f>",self.onFind)
		#self.bind_all("<Control-x>",self.CutText)
		
	def formatMenu(self):
		pulldown = Menu(self.menubar, tearoff=False)
		pulldown.add_command(label='Font..', command = self.onFont)
		self.menubar.add_cascade(label='Format', underline=0, menu=pulldown)
		
	def InsertMenu(self):
		pulldown = Menu(self.menubar, tearoff=False)
		pulldown.add_command(label='Shapes', state = DISABLED)
		pulldown.add_command(label='Special Chars', state = DISABLED)
		self.menubar.add_cascade(label='Insert', underline=0, menu=pulldown)	
		
	def encodingMenu(self):
		pulldown = Menu(self.menubar, tearoff=False)
		pulldown.add_command(label='Encode in ANSII', state = DISABLED)
		pulldown.add_command(label='Encode in UTF-8 ', state = DISABLED)
		pulldown.add_separator()
		pulldown.add_command(label='Input..', state = DISABLED)
		self.menubar.add_cascade(label='Encoding', underline=0, menu=pulldown)

	def HelpMenu(self):
		pulldown = Menu(self.menubar, tearoff=False)
		pulldown.add_command(label='Shortcuts', state = DISABLED)
		pulldown.add_command(label='About e~note ', state = DISABLED)
		self.menubar.add_cascade(label='?', underline=0, menu=pulldown)
	
	"""
	-----------------------------------------------------------------------------------
	|								Caller Function									   |
	| This are helper function which calls it respective method from 'menuClass' file  |
	------------------------------------------------------------------------------------
	"""
	def CutText(self, event=''):
		text=self.menu.CutText(self,self.st)
		self.CopyCutClipboard_Helper(text)
		
	def onPaste(self, event=''):
		try:
			text=self.selection_get(selection = 'CLIPBOARD')
			self.st.getTextobj().insert(INSERT, text)	
		except TcLError:
			pass
			
	def onFind(self, event=''):
		self.menu.onFind(self.st,self)
		
	def onSaveAs(self, event=''):
		self.menu.SaveAsFile(self,self.st)
		
	def onSave(self, event=''):
		self.menu.SaveFile(self,self.st)
		
	def onOpen(self, event=''):
		self.menu.OpenFile(self,self.st)
		
	def onNew(self, event=''):
		self.menu.onNew(self,self.st)
		
	def onUndo(self, event=''):
		self.menu.onUndo(self,self.st)
		
	def onRedo(self, event=''):
		self.menu.onRedo(self,self.st)
		
	def onSelectAll(self, event = ''):
		self.menu.onSelectAll(self.st)
		
	def onDelete(self, event = ''):
		self.menu.onDelete(self,self.st)
		
	def onDeleteAll(self, event =''):
		self.menu.onDeleteAll(self,self.st)

	def onCopy(self, event=''):
		text=self.menu.onCopy(self,self.st)
		self.CopyCutClipboard_Helper(text)
		
	def onFont(self,event =''):
		self.createFontGui()
		self.checkFontGuiOutCome()
		
	def onRightClickEvent(self,event):
		self.aMenu.post(event.x_root, event.y_root)
		
	def checkFontGuiOutCome(self):
		if self.ApplyToValue == 'All' :
			self.setTextFontOnAll()
		elif self.ApplyToValue == 'Selected Only':
			self.setTextFontOnSelected()
		else:
			pass

			
	def setTextFontOnAll(self):
		setFont = [self.fontFamily, self.fontSize, self.fontStyle]
		textObj = self.st.getTextobj()
		textObj.config(font = setFont, fg = self.fontColor )
		
	def setTextFontOnSelected(self):
		textObj = self.st.getTextobj()
		tagCount = self.setTagToText_Helper(textObj)
		try:
			setFont = [self.fontFamily, self.fontSize, self.fontStyle]
			textObj.tag_configure(tagCount, font = setFont,foreground = self.fontColor)
		except TclError:
			pass
	
	"""
	-----------------------------------------------------------------------------------
	|								Menu Postcommand functions on menubar								   |
	| these are helper function that responds to postcommand option on the menubar |
	------------------------------------------------------------------------------------
	"""
	def enableOrDisableIterms(self):
		self.checkMenuOnCopyOnCut_Helper()
		self.checkMenuOnPaste_Helper()
		self.checkMenuOnDeleteAll_Helper()
		
		
	def checkMenuOnCopyOnCut_Helper(self):
		try:
			text= self.st.getTextobj()
			copyText = text.get(SEL_FIRST,SEL_LAST)
		except TclError:
			self.pulldown.entryconfig(3, state = DISABLED)
			self.pulldown.entryconfig(4, state = DISABLED)
			self.pulldown.entryconfig(8, state = DISABLED)
		else:
			self.pulldown.entryconfig(3, state = NORMAL)
			self.pulldown.entryconfig(4, state = NORMAL)
			self.pulldown.entryconfig(8, state = NORMAL)
			
	def checkMenuOnPaste_Helper(self):
		try:
			text=self.selection_get(selection = 'CLIPBOARD')
		except TclError:
			self.pulldown.entryconfig(5, state = DISABLED)
		else:
			self.pulldown.entryconfig(5, state = NORMAL)
		
	def checkMenuOnDeleteAll_Helper(self):
		text= self.st.getTextobj()
		get = text.get('1.0', END+'-1c')
		if get == '':
			self.pulldown.entryconfig(9, state = DISABLED)
		else:
			self.pulldown.entryconfig(9, state = NORMAL)
	
	"""
	-----------------------------------------------------------------------------------
	|								Menu Postcommand functions on text area								   |
	| these are helper function that responds to postcommand option on the menu text area |
	------------------------------------------------------------------------------------
	"""		
					
	def enableOrDisableItermsOnTextArea(self):
		self.checkMenuOnCopyOnCutOnTextArea_Helper()
		self.checkMenuOnPasteOnTextArea_Helper()
		self.checkMenuOnDeleteAllOnTextArea_Helper()
		
		
	def checkMenuOnCopyOnCutOnTextArea_Helper(self):
		try:
			text= self.st.getTextobj()
			copyText = text.get(SEL_FIRST,SEL_LAST)
		except TclError:
			self.aMenu.entryconfig(3, state = DISABLED)
			self.aMenu.entryconfig(4, state = DISABLED)
			self.aMenu.entryconfig(8, state = DISABLED)
		else:
			self.aMenu.entryconfig(3, state = NORMAL)
			self.aMenu.entryconfig(4, state = NORMAL)
			self.aMenu.entryconfig(8, state = NORMAL)
			
	def checkMenuOnPasteOnTextArea_Helper(self):
		try:
			text=self.selection_get(selection = 'CLIPBOARD')
		except TcLError:
			self.aMenu.entryconfig(5, state = DISABLED)
		else:
			self.aMenu.entryconfig(5, state = NORMAL)
			
	def checkMenuOnDeleteAllOnTextArea_Helper(self):
		text= self.st.getTextobj()
		get = text.get('1.0', END+'-1c')
		if get == '':
			self.aMenu.entryconfig(9, state = DISABLED)
		else:
			self.aMenu.entryconfig(9, state = NORMAL)
	
	"""
	--------------------------------------------------------------------------
	|                                 Helper function                        |
	--------------------------------------------------------------------------
	"""
	def CopyCutClipboard_Helper(self,text):
		if text:
			self.clipboard_clear()
			self.clipboard_append(text)
		else:
			pass
		
	def setTagToText_Helper(self,textObj):
		self.setTagToTextCount += 1
		try:
			tagCount = 'setFont'+ str(self.setTagToTextCount)
			textObj.tag_add(tagCount,SEL_FIRST,SEL_LAST)
			return tagCount
		except TclError:
			return
			
	def clearTagText_Helper(self,textObj):
		#textObj.tag_remove('setFont', '1.0', END)
		pass
	"""
		@param void
			respond to the main window exit build-in fxn and check if text was modified.
			if yes, it popup a comfirmation window asking 'save,don't save and cancel'.
			if 'save', it save the changes and exit the window.
			if 'don't save', it simply exit the window.
			if 'cancel', it does nothing.
		@return void.
	"""
	def checkOnWindowDelete_Helper(self):
		textObj = self.st.getTextobj()
		if textObj.edit_modified():
			self.menu.onNewWidget(self,self.st)
			if self.menu.returnNewWidgetValue() == 'Save':
				self.onSave()
				self.quitWindow()
			elif self.menu.returnNewWidgetValue() == 'NoSave':
				self.quitWindow()
			else:
				pass
		else:
			self.quitWindow()
			
	def rightClickEvent_Helper(self):
		self.aMenu = Menu(self.master,tearoff = 0,postcommand = self.enableOrDisableItermsOnTextArea)
		self.aMenu.add_command(label = 'Undo',command = self.onUndo)
		self.aMenu.add_command(label = 'Redo',command = self.onRedo)
		self.aMenu.add_separator()
		self.aMenu.add_command(label = 'Copy', command = self.onCopy)	
		self.aMenu.add_command(label = 'Cut',command =self.CutText)					
		self.aMenu.add_command(label = 'Paste',command = self.onPaste)
		self.aMenu.add_command(label = 'Select All',command = self.onSelectAll)
		self.aMenu.add_separator()
		self.aMenu.add_command(label = 'Delete',command = self.onDelete)
		self.aMenu.add_command(label = 'Delete All',command = self.onDeleteAll)
		self.aMenu.add_separator()		
		self.aMenu.add_command(label = 'Other',command = lambda:None)		
	
	"""
	-------------------------------------------------------------------------
	|							Return functions							|
	-------------------------------------------------------------------------
	"""
	
	"""
		@param void
			return the text editor title
		@return self.editorTitle [type: str]
	"""
	def returnEditorTitle(self):
		return self.editorTitle
	
	"""
		@param void
			return the x and y coordinate of the master window.
		@returns self.master.winfo_x, self.master.winfo_y [type: float]
	"""
	def returnWindowPosition(self):
		return (self.master.winfo_x(),self.master.winfo_y())

if __name__ == '__main__':
	if len(sys.argv) > 1:
		SimpleEditor(file=sys.argv[1]).mainloop() # filename on command line
	else:
		SimpleEditor().mainloop() # or not: start empty