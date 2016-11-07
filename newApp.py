from flask import Flask, render_template, request, session, redirect, url_for
from utils import add, auth, mainpage, create
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = "Asdfasdfasdf"

@app.route("/")## i think this is fine
def root():
    if 'user' in session: 
        return redirect(url_for("home"))
    return redirect(url_for("login"))
    

@app.route("/login/")
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
        return render_template("login.html", result = "Incorrect username or password.", loggedIn=False)




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



@app.route("/home/")#lists the stories that can be added to / viewed / button for creating new story LOL THIS IS WHAT IT WAS ORIGINALLY
def home():
    return render_template("main.html", addlinks = mainpage.storiesToAddTo(session['user']) , viewlinks = mainpage.storiesICanView(session['user']), loggedIn=True)


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
        add.addEntry(int(storyid), entry, user, story)
        li = add.return_Last_Entry_and_title_user(storyid)
        return render_template("story.html", title = li[0], story = mainpage.wholeStory(storyid), write=False, loggedIn=True)



@app.route("/settings/")
def settings():
    return render_template("settings.html")


@app.route("/changePass/", methods = ["POST"])
def changePass():
    if auth.changeP(session['user'], request.form['old'], request.form['new']):
        return render_template("main.html", message = "password changed")
    else:
        return render_template("main.html", message = "old password incorrect")
        
@app.route("/view/")
def view():
    stories_toview = mainpage.storiesICanView(session['user'])
    return render_template("view.html", viewlinks = stories_toview_links)



@app.route("/logout/", methods = ["GET","POST"])
def logout():
    session.pop("user")
    return redirect(url_for("root"))

        
if __name__ == "__main__":
    app.debug = True
    app.run()

#-----------------------------------------------------------------------------
#EVERYTHING WORKS ABOVE THIS LINE (Hopefully)


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


#create new stories
@app.route("/createstories/", methods = ["GET", "POST"])
def create():
    return render_template("create.html")
    
#add new stories to the database
@app.route("/createstoriesdb", methods = ['POST', 'GET'])
def createrstoriesdb():
    if request.method == 'POST':
        newStoryID = create.findNextStoryID()
        title = request.form['title']
        creator = session['user']
        content = request.form['content']
        create.addNewStory(newStoryID, title, creator, content)
        return redirect(url_for("main"))

