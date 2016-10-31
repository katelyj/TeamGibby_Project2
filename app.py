#!/usr/bin/python
from flask import Flask, render_template, request, session, redirect, url_for
import csv 
import  #use sha256
import sqlite3
f = "database.db"
db = sqlite3.connect(f)
og = db.cursor()
d = {}

app = Flask(__name__)
app.secret_key = '\xbc!<\xf2\x9eW1\rm\xc4=\xc8\x90b\x8d?iA\xdf\x98'


def auth(user, pw):
	command = "SELECT "









@app.route('/')
def arthur():
	# if logged in --> main, if not login
	if len(session.keys()) != 0:
		return redirect(url_for('mrRatburn'))
	else:
		return redirect(url_for('doraWinafred'))


@app.route():
def mrRatburn():
	return render_template("main.html")


@app.route('/login/')
def doraWinafred():
	return render_template("login.html", message = "")



@app.route('/view/')
def buster():
	return render_template("view.html")


@app.route('/add/')
def theBrain():
	return render_template("add.html")



@app.route('/create/')
def francine():
	return render_template("create.html")


@app.route('/settings/')
def muffy():
	return render_template("settings.html")


