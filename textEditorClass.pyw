from tkinter import *
#import docx 
import os
class ScrolledText:
	"""
	creates a scrollbar and a text object,then link them to synch at each scroll
	"""
	def makewidgets(self):
		self.sbar = Scrollbar(None)							#vertical scrollbar obj
		self.ybar = Scrollbar(None, orient='horizontal') 	#horizontal scrollbar obj
		self.text = Text(None, relief=SUNKEN, undo = True )				#text obj
		self.sbar.config(command=self.text.yview)			#sych vertical scrollbar and text obj
		self.ybar.config(command=self.text.xview)			
		self.text.config(yscrollcommand = self.sbar.set)
		self.text.config(xscrollcommand = self.ybar.set)
		self.sbar.pack(side = RIGHT,  fill=Y)
		self.ybar.pack(side = BOTTOM, fill=X)
		self.text.pack(side = LEFT, expand= YES, fill= BOTH)

	def settext(self, text='Build by Eyong kevin...', file=None):
	
		if file:
			#text = open(file, 'rb').read()  # get the content of the file
			#text = Document(file)
			filename, file_extension = os.path.splitext(file)
			if file_extension == '.docx':
				pass
				'''
				doc = docx.Document(file)
				fullText = []
				for para in doc.paragraphs:
					fullText.append(para.text)
				text= '\n\n'.join(fullText)
				'''
			else:
				text = open(file, 'r').read()
				
		else:
			
			filename = 'Untitled'
			file_extension = '.txt'
			return filename,file_extension
					
		self.text.delete('1.0', END)       # empty the scrolledtext object entries
		self.text.insert('1.0', text)      # populate the scrolledtext with file content
		self.text.mark_set(INSERT, '1.0')  # set the cursur to the start of the text.
		self.text.focus()  		#set focus to the content
		self.text.edit_modified(False)
		return filename,file_extension 
	"""
	return ScrolledText obj for reused
	"""
	def getTextobj(self):
		return self.text
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
		
	