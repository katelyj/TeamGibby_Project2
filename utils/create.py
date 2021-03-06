from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3




#finding the maximum storyID
def findNextStoryID():
    f = "data/database.db"
    db = sqlite3.connect(f)
    og = db.cursor()
    command = "SELECT MAX(storyID) FROM story_directory"
    maxStoryID = og.execute(command)
    for item in maxStoryID:
        return item[0] + 1



#adding a new story to the database
def addNewStory(storyID, title, creator, content):
    f = "data/database.db"
    db = sqlite3.connect(f)
    og = db.cursor()
    command = "INSERT INTO story_directory VALUES(%d, '%s', '%s')"%(storyID, title, creator)
    og.execute(command)
    command = "INSERT INTO story_entries VALUES(%d, %d, '%s', '%s')"%(storyID, 1, creator, content)
    og.execute(command)
    db.commit()
    db.close()

