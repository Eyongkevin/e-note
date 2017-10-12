from tkinter import *

class HyperlinkManager:
	def __init__(self, text):
		self.text = text
		
		self.text.tag_config('hyper',foreground = 'blue', underline = 1)
		
		self.text.tag_bind('hyper','<Enter>', self._enter)
		self.text.tag_bind('hyper','<Leave>', self._leave)
		self.text.tag_bind('hyper','<Button-1>', self._click)
		
		self.reset()
		
	def reset(self):
		self.links = {}
		
	def add(self, action):
		tag = 'hyper-%d'% len(self.links)
		self.links[tag] = action
		return 'hyper', tag
		
	def _enter(self, event):
		self.text.config(cursor = 'hand2')
		print('hand')
		
	def _leave(self, event):
		self.text.config(cursor = '')
		
	def _click(self, event):
		for tag in self.text.tag_names(CURRENT):
			if tag[:6] == 'hyper-':
				self.links[tag]()
				print(tag)
				return
				
if __name__ == '__main__':
	root =Tk()
	root.title('Hyperlink-1')
	
	text = Text(root)
	text.pack()
	
	hyperlink = HyperlinkManager(text)
	
	def click1():
		print('click-1')
		
	text.insert(INSERT, 'this is a')
	text.insert(INSERT, 'link', hyperlink.add(click1))
	text.insert(INSERT, '\n\n')
	
	def click2():
		print('click 2')
		
	text.insert(INSERT, 'this is a')
	text.insert(INSERT, 'link', hyperlink.add(click2))
	text.insert(INSERT, '\n\n')
	
	mainloop()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	