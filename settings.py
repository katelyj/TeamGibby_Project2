#SETTINGS

#change password?
#customize user page?

import sqlite3

db = sqlite3.connect("database.db")
c = db.cursor()

#changing password
def changePass(username, originalPass, newPass):
    
    s = "SELECT username, password FROM user"
    t = c.execute(s)

    for record in t:
        if record[0] == u: #correct user
            if record[1] == originalPass: #correct original password
                record[1] = newPass #change to new password
                db.commit()
                db.close()
                return "Success!"
            else:
                return "Incorrect password!"

    return "Error: user not found" #shouldn't happen... but just in case


    
