from collections import OrderedDict
import datetime
import os
import sys
from peewee import *

db = SqliteDatabase('Notes.db')

class Note(Model):
	content = TextField()
	date = DateTimeField(default=datetime.datetime.now)
	
	class Meta:
		database = db

def intialize():
	""" init our database"""
	db.connect()
	db.create_tables([Note],safe=True)

def clear():
	os.system('cls' if os.name == 'nt' else 'clear')
		
def menu_loop():
	"""Show the menu"""
	choice = None
	while choice != 'q':
		clear()
		print('Enter q to quit')
		for key,value in menu.items():
			print('{}) {}'.format(key,value.__doc__))
		
		choice = input('Action: ').lower().strip()
		
		if choice in menu:
			clear()
			menu[choice]()

	
def add_note():
	"""Add a note"""
	print('Enter your note , Press ctrl+d when finish')
	data = sys.stdin.read().strip()
	
	if data:
		if input('Save this Note? [Yn]').lower() != 'n':
			Note.create(content=data)
			print('data is saved')


def view_note(search_note=None):
	"""view a note"""
	notes = Note.select().order_by(Note.date.desc())
	if search_note:
		notes = notes.where(Note.content.contains(search_note)) # like
	for note in notes:
		clear()
		date = note.date.strftime('%A %B %D %I:%M%p')
		print(date)
		print('='*len(date))
		print(note.content)
		print('\n\n'+'='*len(date))
		print('n) to next note')
		print('d) for delete.')
		print('q) return  to the menu')
		
		next_act = input('Action: [Ndq]').lower().strip()
		if next_act == 'q':
			break
		elif next_act == 'd':
			delete_note(note)

def search_note():
	"""search for a note"""
	view_note(input('Search: '))
	
	
def delete_note(note):
	"""delete a note"""
	if input('Are you sure? [Yn] ').lower() == 'y':
		note.delete_instance()
		print('note deleted')

	
menu = OrderedDict([
	('a',add_note),
	('v',view_note),
	('s',search_note)
])

if __name__ == "__main__":
	intialize()
	menu_loop()
