# This Python file uses the following encoding: utf-8
from tkinter import *
import sys

class MakeAccentation(object):

	accentList = {'i':u'í','o':'ó','a':'á','e':'é', 'u':'ú'}
	def __init__(self,parent= None):
		pass

	def createAccentation(self, textObj): 
		self.textObj = textObj
		
		self.master.bind_all("<Control-Key-'><i>",self.insert_accented_i)
		self.bind_all("<Control-Key-'><o>",self.insert_accented_o)
		self.bind_all("<Control-Key-'><u>",self.insert_accented_u)
		self.bind_all("<Control-Key-'><a>",self.insert_accented_a)
		self.bind_all("<Control-Key-'><e>",self.insert_accented_e)

		
	def insert_accented_i(self, event = ''):
		char = 'i'
		self.set_accent(char)
		
	def insert_accented_o(self, event = ''):
		char = 'o'
		self.set_accent(char)
	def insert_accented_u(self, event = ''):
		char = 'u'
		self.set_accent(char)
	def insert_accented_a(self, event = ''):
		char = 'a'
		self.set_accent(char)
	def insert_accented_e(self, event = ''):
		char = 'e'
		self.set_accent(char)
		
	def set_accent(self,char):
		getAccent = self.accentList[char]
		self.textObj.getTextobj().insert(INSERT, getAccent)
