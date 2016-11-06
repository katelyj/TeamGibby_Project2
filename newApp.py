from flask import Flask, render_template, request, session, redirect, url_for
from utils import add, auth
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = "Asdfasdfasdf"

@app.route("/")
def root():
    for user in session: 
        return redirect(url_for("main"))
    return redirect(url_for("login"))

@app.route("/login/", methods = ["POST"])
def login():
    response = request.form
    username = response["user"]
    password = response["password"]
          
    if auth.checkLogin(username, password): #successfully logged in
        return redirect(url_for("/"))
        
    else: #unsuccessful login
        return render_template("login.html", result = "Incorrect username or password.")

@app.route("/main/")


@app.route("/logout/", methods = ["POST"])
def logout():
    if request.form["enter"] == "logout":
        session.pop("user")
    return redirect(url_for("auth"))

@app.route("/create/", methods = ["GET", "POST"])
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

if __name__ == "__main__":
    app.debug = True
    app.run()
