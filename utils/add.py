#!/usr/bin/python 
from flask import Flask, render_template, request, session, redirect, url_for
import hashlib #use sha256
import sqlite3
f = "database.db"
db = sqlite3.connect(f)
og = db.cursor()
d = {}



# Adds an entry to the stories database
def findNextEntryNum(storyID):
	command = "SELECT entryNum FROM story_entries WHERE storyID == " + str(storyID) + ""
	derekShepherd = og.execute(command)
	maxlis = 0
	for manz in derekShepherd:
		if (manz[0] >= maxlis):
			maxlis = manz[0]
	return maxLis + 1



def addEntry(storyId, entryNum, user, entryText):
	
	command = "INSERT INTO story_entries VALUES(%d , %d, %s, %s)"%(storyId, entryNum, user, entryText)
	og.execute(command)
	db.commit()
        db.close()


