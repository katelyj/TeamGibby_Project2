from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import hashlib


ramirez = Flask(__name__)
ramirez.secret_key = "fjrjgh??0vjirun??f449929hnf"

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
def checkLogin(username, password):

    s = "SELECT username, password FROM user"
    t = c.execute(s)

    for record in t:
        if record[0] == username: #username found
            if record[1] == hash(password): #correct password
                return True
            else: #incorrect password
                return False
            
    #no username was found
    return False


@ramirez.route("/")
def root():
    for user in session:
        return redirect(url_for("main"))
    return redirect(url_for("auth"))


@ramirez.route("/auth/")
def auth():
    print request.headers
    return render_template("login.html")


@ramirez.route("/main/")
def main():
    return render_template("main.html", user = session["user"])


@ramirez.route("/logout/", methods = ["POST"])
def logout():
    if request.form["enter"] == "logout":
        session.pop("user")
    return redirect(url_for("auth"))


@ramirez.route("/check/", methods = ["GET", "POST"])
def check():
    
    response = request.form
    username = response["user"]
    password = response["password"]
    session["user"] = username
        
    if checkLogin(username, password): #successfully logged in
        return redirect(url_for("main"))
        
    else: #unsuccessful login
        return render_template("login.html", result = "Incorrect username or password.")


@ramirez.route("/create/", methods = ["GET", "POST"])
def create():

    response = request.form
    username = response["user"]
    first = response["first"]
    last = response["last"]
    password = response["password"]
    session["user"] = username

    return render_template("login.html", result = register(username, first, last, password))

        
if __name__ == "__main__":
    ramirez.debug = True
    ramirez.run()
