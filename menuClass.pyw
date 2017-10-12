from tkinter import *
from tkinter.filedialog import askopenfilename    # get standart dialog to request a file
from tkinter.filedialog import asksaveasfilename    # get standart dialog to request a file
from tkinter.simpledialog import askstring
#from docx import Document
from tkinter.messagebox import *
import os
    

class CreateMenuOperations(object):
	def __init__(self):
		self.setFilenameAndExtension()
		self.setWidgetPopupVar()
		
	def setFilenameAndExtension(self):
		self.filename = 'Untitled'
		self.file_extension = '.txt'
		
	def setWidgetPopupVar(self):
		self.widgetPopup = 'None'
		#self.findBtn = None
		
	"""
	this replaces labmda callback on tkinter GUI, its readable and maintainable
	"""
	def command(self,callback, *args, **kwargs):
		def do_call():
			return callback(*args, **kwargs)
		return do_call

	#----------------------------------------------OpenFile--------------------------------------------
	def OpenFile(self,obj,scrolledTextObj):
		text= scrolledTextObj.getTextobj()
		if text.edit_modified():
			self.onNewWidget(obj,scrolledTextObj)
			
			if self.widgetPopup == 'Save':
				self.SaveFile(obj,scrolledTextObj)
				self.Open(obj,scrolledTextObj)
			elif self.widgetPopup == 'NoSave':
				self.Open(obj,scrolledTextObj)
			else:
				pass
		else:
			self.Open(obj,scrolledTextObj)

	def Open(self,obj,scrolledTextObj):
		self.addText = scrolledTextObj
		opts = {}
		try:
			opts['filetypes'] = [('Text Documents','.txt'),('Microsoft 10 Word Documents','.docx')]
			self.filename,self.file_extension = self.addText.settext('',askopenfilename(**opts) )
			if self.filename != 'Untitled':
				obj.setTitle(self.filename+self.file_extension)
		except TclError:
			showerror('error','error opening file')
		
	#------------------------------------onNew-------------------------------------------
	def onNew(self,obj,scrolledTextObj):
		text= scrolledTextObj.getTextobj()
		if text.edit_modified():
			self.onNewWidget(obj, scrolledTextObj)
			if self.widgetPopup =='NoSave':
				self.onNewNoSave(obj,scrolledTextObj)
			elif self.widgetPopup =='Save':
				self.onNewSave(obj,scrolledTextObj)
			else:
				pass
				
		else:
			self.onNewFinished(obj,scrolledTextObj)
	#--------------------------------------------------------------------------------------------
			

	"""
	------------------------------------------onNew fxn-----------------------------------------------------------------------
	                     Below takes care of creating a new file.
	"""
	def onNewWidget(self, obj, scrolledTextObj):
		self.widgetPopup = 'None'
		
		popup=Toplevel()
		popup.resizable(0,0)
		popup.geometry("%dx%d+%d+%d" %(300,100,420,323)) #centralize this window.
		popup.attributes("-toolwindow",1)		#Remove the top minmize/mazimize button
		popup.attributes("-topmost",True)      #always keep this wondow on the top

		popup.title(obj.returnEditorTitle())
		label = Label(popup, text="Text has changed: do you want to save changes?")
		label.config(fg = 'blue')
		label.config(height = 4)
		label.pack(expand = YES, fill = BOTH)
	
		Button(popup, text='Cancel', command = popup.destroy).pack(side = RIGHT)
		Button(popup, text='Don\'t save', command = self.command(self.onWidgetNoSave, obj, scrolledTextObj,popup)).pack(side = RIGHT)
		Button(popup, text='Save' , command = self.command(self.onWidgetSave,obj,scrolledTextObj, popup)).pack(side = RIGHT)
				
		popup.focus_set()
		popup.grab_set()
		popup.wait_window()

	def onWidgetNoSave(self,obj,scrolledTextObj,popup):
		popup.destroy()
		self.widgetPopup = 'NoSave'
	def onWidgetSave(self,obj,scrolledTextObj,popup):
		popup.destroy()
		self.widgetPopup = 'Save'
	def returnNewWidgetValue(self):
		return self.widgetPopup

	"""
	--------------------------------------------------onNew fxn end-----------------------------------------------------
	"""
	
	#take care of 'don't save' function on creating new file	
	def onNewNoSave(self, obj,scrolledTextObj):
		self.onNewFinished(obj,scrolledTextObj)
	#take care of 'save' function on creating a new file
	def onNewSave(self,obj,scrolledTextObj):
		self.SaveFile(obj,scrolledTextObj)
		self.onNewFinished(obj,scrolledTextObj)
		
	#take care of creating new files.
	def onNewFinished(self,obj, scrolledTextObj):
		text = scrolledTextObj.getTextobj()
		text.delete('1.0',END)
		text.edit_reset()
		text.edit_modified(0)
		self.setFilenameAndExtension()
		obj.setTitle(self.filename)
	
	
	
	def SaveFile(self,obj, scrolledTextObj):

		if  self.filename != 'Untitled':
			try:
				filename = self.filename + self.file_extension
				file = open(filename, 'w')
				text= scrolledTextObj.getTextobj()
				text.tag_add(SEL, '1.0', END)
				alltext=text.get(SEL_FIRST, SEL_LAST)
				text.tag_remove(SEL, '1.0', END)
				file.write(alltext)	
				text.edit_modified(0)
			except FileNotFoundError:
				showerror('error',"Could\'n not open file")
		else:
			self.SaveAsFile(obj,scrolledTextObj)
			return
		
			
		
	def SaveAsFile(self,obj, scrolledTextObj):
		title = 'Save File As'
		ftypes = [('Text Documents', '.txt'), ('All files', '*')]
		idir = os.curdir			
		fout = asksaveasfilename(filetypes=ftypes ,initialdir = idir, title=title ,defaultextension = '.txt' ,initialfile= self.filename)
		if fout:
			try:
				with open(fout, 'w') as output:
					text= scrolledTextObj.getTextobj()
					text.tag_add(SEL, '1.0', END)
					alltext=text.get(SEL_FIRST, SEL_LAST)
					text.tag_remove(SEL, '1.0', END)
					output.write(alltext)
					obj.setTitle(fout)
					text.edit_modified(0)
					
							
			except FileNotFoundError:
				showerror('error',"Cancelled save or error in filename")
		else:
			pass
	
	def CutText(self,obj, scrolledTextObj):
		cutText = None
		try:
			text= scrolledTextObj.getTextobj()
			cutText = text.get(SEL_FIRST,SEL_LAST)
			text.delete(SEL_FIRST,SEL_LAST)
			text.tag_remove(SEL, '1.0', END)
			return cutText
		except TclError:
			showinfo(obj.returnEditorTitle(), 'Nothing to cut')
			return cutText
		
	def onCopy(self,obj, scrolledTextObj):
		copyText = None
		try:
			text= scrolledTextObj.getTextobj()
			copyText = text.get(SEL_FIRST,SEL_LAST)
			return copyText
		except TclError:
			showinfo(obj.returnEditorTitle(), 'Nothing to copy')
			return copyText
			
	"""
	below we create a dialog box for find/replace functionalities.
	we create a normal toplevel window, then by using '.attributes("-toolwindow",1)' we remove the minmize/mazimage button hence 
	recembling a normal dialog box, but here we have more control over the window.
	-----------------------------
	other options are (.overrideredirect(1), .resizable(0,0) )
	"""
	def onFind(self,scrolledTextObj,obj):
		self.popup=Toplevel()
		
		self.setWindowPositionAndSize(obj)
		
		self.popup.resizable(0,0) #stop resizable 
		self.popup.attributes("-toolwindow",1)		#Remove the top minmize/mazimize button
		self.popup.attributes("-topmost",True)      #always keep this wondow on the top
		self.popup.title('Find/Replace')
		Label(self.popup, text="Find").grid(row=0)
		Label(self.popup, text="Replace With").grid(row=1)
		
		self.entry_f = Entry(self.popup)
		self.entry_r = Entry(self.popup)
		self.entry_f.focus()
		
		self.var_f = StringVar()
		self.var_r = StringVar()
		self.entry_r.config(textvariable = self.var_r)
		self.entry_f.config(textvariable = self.var_f)
		self.entry_f.grid(row=0, column = 1)
		self.entry_r.grid(row=1, column = 1)
		self.findBtn = Button(self.popup, text='Find' , command =self.command(self.onFindHelper,scrolledTextObj), state = DISABLED)
		self.findBtn.grid(row=3, column = 0)
		self.replaceBtn = Button(self.popup, text='Replace', command = self.command(self.onReplaceHelper,scrolledTextObj), state = DISABLED)
		self.replaceBtn.grid(row=3, column = 1)
		Button(self.popup, text='Cancel', command = self.popup.destroy).grid(row=3, column = 2)
		#self.popup.focus_set()
		#popup.grab_set()
		#popup.wait_window()
		
		self.popup.bind('<Key-Return>',lambda event: self.onFindHelper(scrolledTextObj))
		self.entry_f.bind('<Key>',self.checkEntryValue_f)
		self.entry_r.bind('<Key>',self.checkEntryValue_r)
		
	
	def setWindowPositionAndSize(self,obj):
		x,y = obj.returnWindowPosition()
		x,y = abs(x+150),abs(y+100)
		if y >477:
			y = 400
		self.popup.geometry("%dx%d+%d+%d" %(250,70,x,y))
		
		
	def checkEntryValue_f(self, event=''):
		self.popup.after(1000,self.checkEntryValueHelper_f)	
	def checkEntryValue_r(self, event=''):
		self.popup.after(1000,self.checkEntryValueHelper_r)	
						
	def onUndo(self,obj,scrolledTextObj): 
		text = scrolledTextObj.getTextobj()
		try: 
			text.edit_undo() # exception if stacks empty
		except TclError: # menu tear-offs for quick undo
			showinfo(obj.returnEditorTitle(), 'Nothing to undo')
	def onRedo(self,obj,scrolledTextObj): # 2.0: redo an undone
		text = scrolledTextObj.getTextobj()
		try:
			text.edit_redo()
		except TclError:
			showinfo(obj.returnEditorTitle(), 'Nothing to redo')
			
	def onSelectAll(self,scrolledTextObj):
		text = scrolledTextObj.getTextobj()
		text.tag_add(SEL, '1.0', END+'-1c') # select entire text


	def onDelete(self,obj, scrolledTextObj):
		text = scrolledTextObj.getTextobj()
		try:
			text.delete(SEL_FIRST, SEL_LAST)
		except TclError:
			showinfo(obj.returnEditorTitle(), 'Please select something to delete')
		"""
		if not text.tag_ranges(SEL):
			showinfo(obj.returnEditorTitle(), 'Please select something to delete')
		else:
			text.delete(SEL_FIRST, SEL_LAST)
		"""
	def onDeleteAll(self,obj,scrolledTextObj):
		if askyesno(obj.returnEditorTitle(),'Are you sure you want to delete all?'):
			text = scrolledTextObj.getTextobj()
			text.delete('1.0', END+'-1c') # delete entire text
		else:
			pass
		
	"""
	---------------------------------Helper functions------------------------------------------
	"""	
	def checkEntryValueHelper_r(self,event=''):
		getEntryText_r = self.entry_r.get()
		getEntryText_f = self.entry_f.get()
		if getEntryText_r !='' and getEntryText_f != '':
			self.replaceBtn.config(state = NORMAL)
		else:
			self.replaceBtn.config(state = DISABLED)	
	def checkEntryValueHelper_f(self,event=''):
		getEntryText_f = self.entry_f.get()
		getEntryText_r = self.entry_f.get()
		if getEntryText_f =='':
			self.findBtn.config(state = DISABLED)
			self.replaceBtn.config(state = DISABLED)
		else:
			self.findBtn.config(state = NORMAL)
			self.checkEntryValueHelper_r()

	def onFindHelper(self, scrolledTextObj, event = ''):
		text = scrolledTextObj.getTextobj()
		target=self.var_f.get()
		if target:
			where = text.search(target, INSERT, END)
			if where:
				pastit = where + ('+%dc' % len(target)) #since search return 'row.col' of first occurance of text at start, we add the text length highlit the full text
				text.tag_remove(SEL, '1.0', END)
				text.tag_add(SEL,where,pastit)      #tag it to SEL which automatically highlit it
				text.tag_config(SEL, background='purple')
				text.tag_config(SEL, foreground='white')
				text.see(SEL_FIRST)  
				text.mark_set(INSERT, pastit)
				text.focus()

				
			else:
				showwarning('warning','End of file reach, couldn\'t find word')
				
	def onReplaceHelper(self, scrolledTextObj):
		text = scrolledTextObj.getTextobj()
		target_f=self.var_f.get()
		target_r=self.var_r.get()
		pos = '1.0'
		replaceCount = 0
		if target_f:
			while True:
				where = text.search(target_f, pos, END)
				if where:
					pastit = where + ('+%dc' % len(target_f))
					text.tag_remove(SEL, '1.0', END)
					text.tag_add(SEL,where,pastit)
					text.mark_set(INSERT, pastit)
					delText = text.get(SEL_FIRST,SEL_LAST)
					text.delete(SEL_FIRST,SEL_LAST)
					text.tag_remove(SEL, '1.0', END)
					text.insert(INSERT, target_r)
					pos = INSERT
					replaceCount +=1
				else:
					labelText=str(replaceCount)+" word replaced"
					Label(self.popup, text=labelText , fg='green').grid(row=4, column = 0)
					break
	

		