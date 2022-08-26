#!/usr/bin/env python

import pandas as pd
import re
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import tkinter.font as font
import tkinter as tk
from collections import OrderedDict
 
DISCOGS_DB = "../database/workingDB.csv" # DO NOT CHANGE

class VinylDB:
	def __init__(self, name):
		self.database = pd.read_csv(DISCOGS_DB).values.tolist()
		self.name = name

DATABASE = VinylDB("DB")


def printAlbumInfo(entry):
	print("Title: ", entry[0])
	print("Artist: ", entry[1])
	print("Genre: ", entry[2])
	print("Tracklist: ")
	print(entry[3])

def getArtistInfoUser(evt):
	activeArtist = ArtistsListPanel.get(ANCHOR).strip()

	# searches entries with sam ealbum string, takes first find
	albums = [index for (index, a_tuple) in enumerate(DATABASE.database) if a_tuple[1]==activeArtist]

	# sort out duplicates
	sortedAlbumList = []
	for index in albums:
		sortedAlbumList.append(DATABASE.database[index][0])
	
	sortedAlbumList = sorted(list(OrderedDict.fromkeys(sortedAlbumList)))

	AlbumListPanel.delete(0, END)
	for albumEntry in sortedAlbumList:
		AlbumListPanel.insert(END, albumEntry)

def getAlbumInfoUser(evt):
	activeAlbum = AlbumListPanel.get(ANCHOR).strip()

	# searches entries with sam ealbum string, takes first find
	album = [index for (index, a_tuple) in enumerate(DATABASE.database) if a_tuple[0]==activeAlbum]
	if len(album) >= 1:
		album = DATABASE.database[album[0]]
	else:
		album = DATABASE.database[album]

	labelString = "Album: " + activeAlbum + "\nArtist: " + album[1] + "\nGenre: " + album[2]
	albumInfo_label.config(text=labelString)

	# regex matches in shown order:
	# INDEX ALBUMTITLE DURATION
	tracklistString = album[3]
	pattern = re.compile(r"\$index\[([0-9]*)\] (.*) \$side\[(.+)\] \$dur\[(.*)\]")
	tracklist = []
	for match in pattern.finditer(tracklistString):
		tracklist.append([match.group(1), match.group(2), match.group(3), match.group(4)])
	
	Tracklist.delete(*Tracklist.get_children())
	for i in range(len(tracklist)):
            Tracklist.insert(parent='', index=i, iid=i, text='', values=tracklist[i])


def updateDBPanel():
	sortedArtisList = []
	for entry in DATABASE.database:
		sortedArtisList.append(entry[1])

	sortedArtisList = sorted(list(OrderedDict.fromkeys(sortedArtisList)))
	ArtistsListPanel.delete(0, END)
	for entry in sortedArtisList:
		ArtistsListPanel.insert(END, entry)



"""
updateDB()
new_database = pd.read_csv(DISCOGS_DB)
print("------------")
list_ = new_database.values.tolist()
for entry in list_:
	printAlbumInfo(entry)

"""
print("Creating GUI")
# GUI
# create root window
root = Tk()

# root window title and dimension
root.title("Vinyl Collection Database")
# Set geometry (widthxheight)
root.geometry('1280x720')
root.configure(background="white")
# uncomment for Fullscreen
#root.attributes('-fullscreen',True)

window_label = Label(root, text="Vinyl Collection Database")
window_label.configure(font=('Helvetica',15), fg="black")
window_label.grid(column=1, columnspan=4, pady=10)

#Create database panel
ArtistsListPanel = Listbox(root, width=30, height=30, bg="white")
ArtistsListPanel.insert(END, "Artists")
ArtistsListPanel.configure(font=('Helvetica',15), 
							border="2px", 
							fg="black")
ArtistsListPanel.grid(column=1, row=2, padx=5, rowspan=3)
ArtistsListPanel.bind("<<ListboxSelect>>", getArtistInfoUser)
updateDBPanel()

#Create database panel
AlbumListPanel = Listbox(root, width=40, height=30, bg="white")
AlbumListPanel.insert(END, "Choose an Album")
AlbumListPanel.configure(font=('Helvetica',15), 
							border="2px", 
							fg="black")
AlbumListPanel.grid(column=2, row=2, padx=5, rowspan=3)
AlbumListPanel.bind("<<ListboxSelect>>", getAlbumInfoUser)


albumInfo_label = Label(root, text="Choose an Album")
albumInfo_label.configure(font=('Helvetica',15))
albumInfo_label.grid(column=3, row=2, pady=10)


Tracklist = ttk.Treeview(root, height=20)
Tracklist.grid(column=3, columnspan=2, row=3, rowspan=3)
Tracklist['columns']=('Index', 'Track', 'Position', 'Duration')
Tracklist.column('#0', width=0, stretch=NO)
Tracklist.column('Index', anchor=CENTER, width=50)
Tracklist.column('Track', anchor=CENTER, width=200)
Tracklist.column('Position', anchor=CENTER, width=80)
Tracklist.column('Duration', anchor=CENTER, width=80)
Tracklist.heading('#0', text='', anchor=CENTER)
Tracklist.heading('Index', text='Index', anchor=CENTER)
Tracklist.heading('Track', text='Track', anchor=CENTER)
Tracklist.heading('Position', text='Position', anchor=CENTER)
Tracklist.heading('Duration', text='Duration', anchor=CENTER)


buttonFont = font.Font(family='Helvetica', size=20, weight='bold')

# Execute Tkinter
root.mainloop()