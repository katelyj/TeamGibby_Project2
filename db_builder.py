import sqlite3
#connect to the file
file = "data/database.db"

#connect using sqlite
db = sqlite3.connect(file)

#set up cursor
c = db.cursor()

#create user table
#four columns: username, fname, lname, password
q = "CREATE TABLE user (username TEXT, fname TEXT, lname TEXT, password TEXT)"

#execute user table command
c.execute(q)

#create story_directory table
#three columns: storyID, title, creator
q = "CREATE TABLE story_directory (storyID INTEGER, title TEXT, creator TEXT)"

#execute story_directories table command
c.execute(q)

#create story_entries table
#four columns: storyID, entrynum, user, content
q = "CREATE TABLE story_entries (storyID INTEGER, entrynum INT, user TEXT, content TEXT)"

#execute story_entries command
c.execute(q)

#commit db
db.commit()

#close db
db.close()
