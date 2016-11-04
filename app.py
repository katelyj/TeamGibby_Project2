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


## Looks into the story entries DB for story IDs where the user matches the current user logged in
## Returns a list of story IDs that the user is able to read, because they have contributed to them

def storiesIcanView():
    ggg = "SELECT storyId FROM story_entries where user == " + str(session['user']) + ";"
    rara = og.execute(ggg)
    stories = []#list of story IDs you're allowed to choose from
    i = 0
    for item in rara:
        if (not(item[0] in stories)):
            stories.append(item[0])
    return stories

## Takes a list of (int) story ids, searches in the story directory for the stories you can view, because you have contributed to them
## returns a form full of buttons, where each button has the text "title, by user" , is named storytoread, and is matched with it's 
## story ID
def buttonifyLinks(storyID):
    Str = "<form action = '/view/'>" 
    command = "SELECT Title, user, storyId FROM story_directory WHERE storyId == " + str(storyID)+ ""
    poe = og.execute(command)
    for item in poe:
        f = ""
        f+= item[0] + " , by "
        f+= item[1] + 
        Str += "<button type = 'submit' name = 'storytoread' value = " + str(item[2]) + ">  " + f + "</button>"
        Str+= "<br>"
    Str += " </form>  "


##Returns a form full of buttons to the first 10 stories in the story directory database
def stories2Add2():
    Str = "form action= '/add/'>"
    command = "SELECT Title, user, storyID FROM story_directory"
    markSloan = og.execute(command)
    num = 0
    for manz in markSloan:
        if (num < 10):
            f = ""
            f += manz[0] + " , by "
            f += manz[1]
            Str +=  "<button type = 'submit' name = 'storytoaddto' value = " + str(manz[2]) + ">" + f +"</button>"
            Str += "<br>"
            num +=1
        else:
            break
    Str+= "</form>"


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
    ##def addEntry(storyId, entryNum, user, entryText):
    ##takes data from the request form that's passed to main from the add.html form
    if (request.form['entry2Add'] != ''):
        x = "Entry Successfully Added"
        name = session['user']
        entryText = request.form['entry2Add']
        ID = session['storyID']
        eNum = add.findNextEntryNum(ID)
        add.addEntry(ID, eNum, name, entryText) 


    ##Stories Created    
    if (request.form['entry2Start'] != ''):
        x = "Story Successfully Created"
        


    else:
        x = " "

    ##list is a list of story IDs of the stories that the user has added to
    lis = storiesIcanView()
    LINKS_View = buttonifyLinks(lis) ## All the stories u can view
    LINKS_Add = stories2Add2()


    return render_template("main.html", user = session["user"], storiesToView= LINKS_V , storiestoAddto=LINKS_A, message = x) ## both are lists of links
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


@ramirez.route('/createstory/')
def francine():
	return render_template("create.html")


@ramirez.route('/settings/')
def muffy():
	return render_template("settings.html")

        
if __name__ == "__main__":
    ramirez.debug = True
    ramirez.run()
