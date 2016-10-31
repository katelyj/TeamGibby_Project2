#!/usr/bin/python
from flask import Flask, render_template, request
import csv 

app = Flask(__name__)

@app.route("/")
def hi():
	return render_template("main.html")



@app.route("/login/")


@app.route("/view/")



