from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
from datetime import datetime


print datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def findNextStoryID():
    f = "../data/database.db"
    db = sqlite3.connect(f)
    og = db.cursor()
    command = "SELECT MAX(storyID) FROM story_directory"
    maxStoryID = og.execute(command)
    for item in maxStoryID:
        return item[0]
    
findNextStoryID()