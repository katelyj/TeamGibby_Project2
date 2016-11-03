#!/usr/bin/python
from flask import Flask, render_template, request, session, redirect, url_for
from utils import add, create
import sqlite3
import hashlib


f = "database.db"
db = sqlite3.connect(f)
og = db.cursor()
d = {}


ramirez = Flask(__name__)
ramirez.secret_key = "fjrjgh??0vjirun??f449929hnf"


def storiesIcanView():
    ggg = "SELECT storyId FROM story_entries where user == " + str(session['user']) + ";"
    rara = og.execute(ggg)
    stories = []#list of story IDs you're allowed to choose from
    i = 0
    for item in rara:
        stories.append(item[i])
        i+=1
    return stories


def buttonifyLinks(storyID):
    string = "<form action = '/view/'> <b>" 
    command = "SELECT Title, user from story_directory where storyId == " + str(storyID)+ ""
    poe = og.execute(command)
    f = ""
    for item in poe:
        f+= item[0]
        f+= item[1]
    string +=  "<b>Title, by User</b> <input type="text" name=str(storyID)><br><br>"
    string += " </form>  "


#hashing passwords
def hash(x):
    h = hashlib.sha3()
    h.update(x)
    return h.hexdigest()


#new user registering
def register(username, first, last, password):

    s = "SELECT username, password FROM user"
    t = og.execute(s)

    #checking if user is already registered
    for record in t:
        if record[0] == username:
            return "Whoops, this user is already registered!"

    #user is not already registered
    insert = "INSERT INTO user VALUES (%s, %s, %s, %s)"%(username, first, last, hash(password))
    og.execute(insert)

    db.commit()
    db.close()

        
#logging in
def checkLogin(username, password):

    s = "SELECT username, password FROM user"
    t = og.execute(s)

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

    ##ADDED ENTRIES

    if (request.form['entry2Add'] != ''):
        x = "Entry Successfully Added"
        name = session['user']
        entryText = request.form['entry2Add']


    ##Stories Created    
    if (request.form['entry2Start'] != ''):
        x = "Story Successfully Created"
    
    else:
        x = " "


    lis = storiesIcanView



    return render_template("main.html", user = session["user"], storiesToView= LINKS , storiestoAddto=LINKS, message = x) ## both are lists of links
    # message is either "entry successfully added" or "story successfully created"


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

##CREATE ACCOUNTS
@ramirez.route("/create/", methods = ["GET", "POST"])
def create():

    response = request.form
    username = response["user"]
    first = response["first"]
    last = response["last"]
    password = response["password"]
    session["user"] = username

    return render_template("login.html", result = register(username, first, last, password))


@ramirez.route('/view/')
def buster():
	return render_template("view.html", storyID = x)


@ramirez.route('/add/')
def theBrain():
    #each story that displays on the main page 
    storytoview = request.form['storyChosen']
    session['storyId'] = storytoview
	return render_template("add.html", title = "", user = "", lastentry = "")


@ramirez.route('/createstories/')
def francine():
	return render_template("create.html")


@ramirez.route('/settings/')
def muffy():
	return render_template("settings.html")

        
if __name__ == "__main__":
    ramirez.debug = True
    ramirez.run()
