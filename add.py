#!/usr/bin/python 
from flask import Flask, render_template, request, session, redirect, url_for
import  #use sha256
import sqlite3
f = "database.db"
db = sqlite3.connect(f)
og = db.cursor()
d = {}



# Adds an entry to the stories database

def addEntry(storyId, entryNum, user, timestamp, entryText):
	command = "INSERT INTO story_entries VALUES(%d , %d, %s, %s, %s)"%(storyId, entryNum, user, timestamp, entryText)
	og.execute(command)
	db.commit()
    db.close()


