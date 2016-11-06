import sqlite3
file = "data/database.db"
db = sqlite3.connect(file)
c = db.cursor()
q = "CREATE TABLE user (username TEXT, fname TEXT, lname TEXT, password TEXT)"
c.execute(q)

q = "CREATE TABLE story_directory (storyID INTEGER, title TEXT, creator TEXT, timestamp BLOB)"

c.execute(q)

q = "CREATE TABLE story_entries (storyID INTEGER, entrynum INT, user TEXT, timestamp BLOB, content TEXT)"

c.execute(q)

db.commit()
db.close()
