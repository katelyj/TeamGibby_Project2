from flask import Flask, render_template, request, session, redirect, url_for
from utils import add, auth, mainpage, create
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = "Asdfasdfasdf"

@app.route("/")
def root():
    for user in session: 
        return redirect(url_for("main"))
    return redirect(url_for("login"))

@app.route("/login/", methods = ["POST", "GET"])
def login():
    return render_template("login.html", result = "")


@app.route("/authorize/", methods = ["POST"])
def authorize():
    response = request.form
    username = response["user"]
    password = response["password"]
    if auth.checkLogin(username, password): #successfully logged in
        session['user'] = username 
        return redirect(url_for("root"))
    else: #unsuccessful login
        return render_template("login.html", result = "Incorrect username or password.")


@app.route("/createnewacc/", methods = ["POST"])
def createaccount():
    response = request.form
    username = response["user"]
    first = response["first"]
    last = response["last"]
    password = response["password"]
    if (auth.register(username, first, last, password)):
        return render_template("login.html", result = "account successfully created")
    else:
        return render_template("login.html", result = "Sorry, this username has already been taken")

@app.route("/main/")
def main():
    return render_template("main.html")
    

@app.route("/logout/", methods = ["POST"])
def logout():
    if request.form["enter"] == "logout":
        session.pop("user")
    return redirect(url_for("auth"))

@app.route("/createstories/", methods = ["GET", "POST"])
def create():
    return render_template("create.html")

@app.route("/view/")
def view():
    stories_toview = mainpage.storiesICanView(session['user'])
    if len(stories_toview) != 0:
        stories_toview_links = mainpage.buttonifyLinks(stories_toview) 
    else: 
        stories_toview_links = "You haven't added to any stories yet!"

    return render_template("view.html", viewlinks = stories_toview_links)

@app.route("/add/")
def add():
    stories_toadd_links = mainpage.storiesToAddTo()
    return render_template("add.html", addlinks = stories_toadd_links)


@app.route("/add/form/")
def add_inprogress():
    ID = request.form['storytoaddto']
    session['id'] = ID
    stufftorender = add.return_Last_Entry_and_title_user(ID)
    return render_template("addform.html", title = stufftorender[0] , user = stufftorender[1], lastEntry = stufftorender[2])
    ##Adds story entry to the DB, returns to main
    ## story_entries (storyID INTEGER, entrynum INT, user TEXT, content TEXT)

@app.route("/add/done/")
def add_done():
    entrytext = request.form['entry2Add']
    user = session['user']
    storyid = session['id']
    entrynum = add.findNextEntryNum(storyid)
    add.addEntry(storyid, entrynum, user, entrytext)
    session.pop('id')
    return redirect(url_for("root"))

@app.route("/create/done/", methods = ["GET","POST"])
def create_done():
    return redirect(url_for("root"))
    ##Adds story entry to the DB

@app.route("/settings/")
def settings():
    return render_template("settings.html")

@app.route("/changePass/", methods = ["POST"])
def changePass():
    if auth.changeP(session['user'], request.form['old'], request.form['new']):
        return render_template("main.html", message = "password changed")
    else:
        return render_template("main.html", message = "old password incorrect")

@app.route("/createstoriesdb", methods = ['POST', 'GET'])
def createrstoriesdb():
    if request.method == 'POST':
        newStoryID = create.findNextStoryID()
        title = request.form['title']
        creator = session['user']
        content = request.form['content']
        create.addNewStory(newStoryID, title, creator, content)
        
if __name__ == "__main__":
    app.debug = True
    app.run()
