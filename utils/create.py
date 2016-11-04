from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
from datetime import datetime

f = "database.db"
db = sqlite3.connect(f)
q = db.cursor()

print datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Adds an entry to the stories database
def findNextEntryNum(storyID):
	command = "SELECT MAX(storyID) FROM users"
    print command 

def createEntry(storyID, title, user, timestamp):
    command = "INSERT INTO story_directory VALUES(%d, %s, %s, %s)"%(storyID, title, user, timestamp)
	og.execute(command)
	db.commit()
    db.close()
