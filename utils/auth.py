import hashlib
import sqlite3

def checkLogin(username, password):

    f = "data/database.db"
    db = sqlite3.connect(f)
    og = db.cursor()

    s = "SELECT username, password FROM user"
    t = og.execute(s)

    for record in t:
        if record[0] == username: #username found
            if record[1] == hash(password): #correct password
                db.close()
                return True
            else: #incorrect password
                db.close()
                return False
            
    #no username was found
    db.close()
    return False

