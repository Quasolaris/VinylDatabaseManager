#!/usr/bin/env python

import discogs_client
import pandas as pd
import re
import time

USER_TOKEN = "YOUR_ACCESS_TOKEN_HERE" # insert your token here
USER_DATABASE = "../database/template_file.csv" # change path to your vinylDB file
DISCOGS_DB = "../database/workingDB.csv" # DO NOT CHANGE

"""
This script updates the database (saved as workingDB.csv) via the Discogs API.
See README for instructions
"""
def getDatabase():
	raw_database = pd.read_csv(USER_DATABASE)

	data = [raw_database['Artist'], raw_database['Album']]
	header = ["Artist", "Album"]

	API_formated_database = pd.concat(data, axis=1, keys=header)

	print("Found entries: ", len(API_formated_database))


	discogs_API = discogs_client.Client('ExampleApplication/0.1', user_token=USER_TOKEN)
	
	results = []
	queryCount = 0
	for index in range(0, len(API_formated_database)):
		
		# waiting 5 sec after 50 fetches
		if queryCount % 50 == 0:
			print("====== 5 Sec. Pause for API cooldown =====")
			time.sleep(5)

		entry = discogs_API.search(str(API_formated_database["Album"][index]), artist=str(API_formated_database["Artist"][index]) , type='release')
		if entry:
			results.append(getAlbumInfo(entry))
			print(index , " fetching: ", entry[0].title)	
		queryCount += 1


	dataFrame = pd.DataFrame(results, columns=["title", "artist", "genre", "tracklist"])
	return dataFrame


def updateDB():
	API_db = getDatabase()

	print("Writing DB to file")

	API_db.to_csv(DISCOGS_DB, index=False)
	print(API_db.head())


def getAlbumInfo(entry):
	album = entry[0]
	albumInfo = []
	albumInfo.append(getAlbumName(str(album.title)))
	if album.artists:
		albumInfo.append(getArtistName(str(album.artists[0])))
	else:
		albumInfo.append("No Artist")

	if album.genres:
		albumInfo.append( album.genres[0])
	else:
		albumInfo.append("No Genre")


	# keys for index and duration side are:
	# $index[INDEX], $side[SIDE] and $dur[DURATION]
	tracks = ""
	index = 1
	for track in album.tracklist:
		tracks += "$index[" + str(index) + "] " + str(track.title)
		index += 1

		if track.position:
			tracks += " $side[" + track.position + "]"

		if track.duration:
			tracks += " $dur[" + track.duration + "]"
		tracks += "\n" 

	albumInfo.append(tracks)
	return albumInfo


def getArtistName(artistString):
	artist = re.search("'(.*)'>$", artistString)
	if artist:
		return artist.group(1)
	else:
		return "No Album"

def getAlbumName(albumString):
	album = re.search("^.* - (.*)$", albumString)
	if album:
		return album.group(1)
	else:
		return "No Album"

updateDB()