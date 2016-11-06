import hashlib
import sqlite3


def hashDis(x):
    h = hashlib.sha256()
    h.update(x)
    return h.hexdigest()


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

def register(username, first, last, password):

    f = "data/database.db"
    db1 = sqlite3.connect(f)
    og = db1.cursor()

    s = "SELECT username FROM user"
    t = og.execute(s)

    #checking if user is already registered
    for record in t:
        if record[0] == username:
            return False

    #user is not already registered
    insert = "INSERT INTO user VALUES ('%s', '%s', '%s', '%s')"%(username, first, last, hashDis(password))
    og.execute(insert)
    db1.commit()
    db1.close()
    return True

def changeP(username, oldP, newP):
    f = "data/database.db"
    db2 = sqlite3.connect(f)
    og = db2.cursor()

    s = "SELECT * FROM user WHERE username == '" + username + "'"
    t = og.execute(s)
    if hashDis(oldP) == t[3]:
        replace = "UPDATE user SET password = " + hashDis(newP) + " WHERE username == '" + username + "'"
        og.execute(replace)
        db2.commit()
        db2.close()
        return True
    else:
        return False
    
