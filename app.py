from flask import Flask, render_template, request, session, redirect, url_for
from utils import add, auth, mainpage, create
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = "Asdfasdfasdf"

#root

@app.route("/")## i think this is fine
def root():
    if 'user' in session: 
        return redirect(url_for("home"))
    return redirect(url_for("login"))


#login

@app.route("/login/")
def login():
    return render_template("login.html", result = "")


#authenticate users

@app.route("/authorize/", methods = ["POST"])
def authorize():
    response = request.form
    username = response["user"]
    password = response["password"]
    if auth.checkLogin(username, password): #successfully logged in
        session['user'] = username 
        return redirect(url_for("root"))
    else: #unsuccessful login
        return render_template("login.html", result = "Incorrect username or password.", loggedIn=False)



#registering a new user
@app.route("/createnewacc/", methods = ["POST"])
def createaccount():
    response = request.form
    username = response["user"]
    first = response["first"]
    last = response["last"]
    password = response["password"]
    if (auth.register(username, first, last, password)):
        return render_template("login.html", result = "account successfully created", loggedIn=False)
    else:
        return render_template("login.html", result = "Sorry, this username has already been taken", loggedIn=True)



#homepage for logged in users
@app.route("/home/")
def home():
    return render_template("main.html", addlinks = mainpage.storiesToAddTo(session['user']) , viewlinks = mainpage.storiesICanView(session['user']), loggedIn=True)



#making a new story
@app.route("/newStory/", methods=["GET","POST"])# new stories
def newStory():
    if request.method == "GET":
        return render_template("newStory.html", loggedIn=True)
    else:
        title = request.form["title"]
        story = request.form["story"]
        user = session['user']
        storyid = create.findNextStoryID()
        create.addNewStory(storyid, title, user, story)
        return redirect("/story/" + str(storyid))



#variable link of a story
@app.route("/story/<storyid>/", methods=["GET","POST"]) # where the story is added and stuff
def story(storyid):
    if request.method == "GET":
        if mainpage.contributed(session['user'], storyid):
            li = add.return_Last_Entry_and_title_user(storyid)
            print "TESTISTEOISJDFOL"
            print mainpage.wholeStory(storyid)
            return render_template("story.html",title = li[0], story = mainpage.wholeStory(storyid), write=False, loggedIn=True) #CHANGE LATER FOR INPUTS
        else: 
            li = add.return_Last_Entry_and_title_user(storyid)
            return render_template("story.html", title = li[0], lastEntry = li[2], write=True, loggedIn=True)
    else:
        user = session['user']
        entry = add.findNextEntryNum(storyid)
        story = request.form['story']
        storyid = int(storyid)
        add.addEntry(storyid, entry, user, story)
        li = add.return_Last_Entry_and_title_user(storyid)
        return render_template("story.html", title = li[0], story = mainpage.wholeStory(storyid), write=False, loggedIn=True)



#account settings
@app.route("/settings/")
def settings():
    return render_template("settings.html")

#changing a password
@app.route("/changePass/", methods = ["POST"])
def changePass():
    if auth.changeP(session['user'], request.form['old'], request.form['new']):
        return render_template("main.html", message = "password changed", addlinks = mainpage.storiesToAddTo(session['user']) , viewlinks = mainpage.storiesICanView(session['user']), loggedIn=True)
    else:
         return render_template("main.html", message = "incorrect old password", addlinks = mainpage.storiesToAddTo(session['user']) , viewlinks = mainpage.storiesICanView(session['user']), loggedIn=True)


#logging out
@app.route("/logout/", methods = ["GET","POST"])
def logout():
    session.pop("user")
    return redirect(url_for("root"))


if __name__ == "__main__":
    app.debug = True
    app.run()

