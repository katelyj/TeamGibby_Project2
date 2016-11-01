from flask import Flask
import sqlite3
import hashlib


ramirez = Flask(__name__)

db = sqlite3.connect("database.db")
c = db.cursor()


#hashing passwords
def hash(x):
    h = hashlib.sha3()
    h.update(x)
    return h.hexdigest()


#new user registering
def register(username, first, last, password):

    s = "SELECT username, password FROM user"
    t = c.execute(s)

    #checking if user is already registered
    for record in t:
        if record[0] == username:
            return "Whoops, this user is already registered!"

    #user is not already registered
    insert = "INSERT INTO user VALUES (%s, %s, %s, %s)"%(username, first, last, hash(password))
    c.execute(insert)

    db.commit()
    db.close()

        


#logging in
def login(username, password):
    return ""
