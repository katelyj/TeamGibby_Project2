import sqlite3
import hashlib


db = sqlite3.connect("database.db")
c = db.cursor()


#changing password
def changePass(username, originalPass, newPass):
    
    s = "SELECT username, password FROM user"
    t = c.execute(s)

    for record in t:
        if record[0] == u: #correct user
            if record[1] == hash(originalPass): #correct original password
                record[1] = hash(newPass) #change to new password
                db.commit()
                db.close()
                return "Success!"
            else: #incorrect original password
                return "Incorrect password!"

    return "Error: user not found" #shouldn't happen... but just in case


#hashing passwords
def hash(x):
    h = hashlib.sha256()
    h.update(x)
    return h.hexdigest()
