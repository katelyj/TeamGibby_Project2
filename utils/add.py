#!/usr/bin/python 
from flask import Flask, render_template, request, session, redirect, url_for
import hashlib #use sha256
import sqlite3




# Adds an entry to the stories database
def findNextEntryNum(storyID):
	f = "data/database.db"
	db = sqlite3.connect(f)
	og = db.cursor()
	command = "SELECT entryNum FROM story_entries WHERE storyID == " + str(storyID) + ""
	derekShepherd = og.execute(command)
	maxlis = 0
	for manz in derekShepherd:
		if (manz[0] >= maxlis):
			maxlis = manz[0]
    
        db.close()
	return maxlis + 1


def return_Last_Entry_and_title_user(ID):
	f = "data/database.db"
	db = sqlite3.connect(f)
	og = db.cursor()
	command = "SELECT title, creator FROM story_directory WHERE storyID ==" + str(ID)
	meredithGrey = og.execute(command)
	li = []
	for scalpel in meredithGrey:
		li.append(scalpel[0])
		li.append(scalpel[1])

	command2 = "SELECT content, entryNum FROM story_entries WHERE storyID ==" + str(ID) 
	cristinaYang = og.execute(command2)
	li2 = []
	for tenblade in cristinaYang:
		li2.append(tenblade[0])
	li.append(li2[len(li2)-1])
	db.close()
	return li#should be title, creator, last entry




def addEntry(storyId, entryNum, user, entryText):
	f = "data/database.db"
	db = sqlite3.connect(f)
	og = db.cursor()
	command = "INSERT INTO story_entries VALUES(%d, %d, '%s', '%s')"%(storyId, entryNum, user, entryText)	
	print storyId
	print entryNum
	print user
	print entryText
	og.execute(command)
	db.commit()
        db.close()



