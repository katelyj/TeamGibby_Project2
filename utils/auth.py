import hashlib
import sqlite3

#hasing passwords
def hashDis(x):
    h = hashlib.sha256()
    h.update(x)
    return h.hexdigest()


#authenticating a user
def checkLogin(username, password):

    f = "data/database.db"
    db = sqlite3.connect(f)
    og = db.cursor()

    s = "SELECT username, password FROM user"
    t = og.execute(s)

    for record in t:
        if record[0] == username: #username found
            if record[1] == hashDis(password): #correct password
                db.close()
                return True
            else: #incorrect password
                db.close()
                return False
            
    #no username was found
    db.close()
    return False


#registering a new user
def register(username, first, last, password):

    f = "data/database.db"
    db = sqlite3.connect(f)
    og = db.cursor()

    s = "SELECT username FROM user"
    t = og.execute(s)

    #checking if user is already registered
    for record in t:
        if record[0] == username:
            return False

    #user is not already registered
    insert = "INSERT INTO user VALUES ('%s', '%s', '%s', '%s')"%(username, first, last, hashDis(password))
    og.execute(insert)
    db.commit()
    db.close()
    return True

#changing a user's password
def changeP(username, oldP, newP):
    f = "data/database.db"
    db = sqlite3.connect(f)
    og = db.cursor()

    s = "SELECT * FROM user WHERE username == '" + username + "'"
    t = og.execute(s)
    for x in t:
        if hashDis(oldP) == x[3]:
            replace = "UPDATE user SET password = '" + hashDis(newP) + "' WHERE username == '" + username + "'"
            og.execute(replace)
            db.commit()
            db.close()
            return True
        else:
            return False
    
