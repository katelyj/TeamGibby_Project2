from flask import Flask, render_template, request, session, redirect, url_for
from utils import add, auth, mainpage
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

    #stories to view
    stories_toview = mainpage.storiesICanView(session['user'])
    if len(stories_toview) != 0:
        stories_toview_links = mainpage.buttonifyLinks(stories_toview) 
    else: 
        stories_toview_links = "You haven't added to any stories yet!"

    ##stories to add to
    stories_toadd_links = mainpage.storiesToAddTo()
    return render_template("main.html", viewlinks = stories_toview_links, addlinks = stories_toadd_links)
    

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
    return render_template("view.html")

@app.route("/add/")
def add():
    return render_template("add.html")

@app.route("/settings/")
def settings():
    return render_template("settings.html")

@app.route("/changePass/")
def changePass():
    return render_template("main.html", message = "password changed")

if __name__ == "__main__":
    app.debug = True
    app.run()
