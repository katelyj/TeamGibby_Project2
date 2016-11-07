from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
from datetime import datetime

f = "data/database.db"
db = sqlite3.connect(f)
q = db.cursor()

print datetime.now().strftime('%Y-%m-%d %H:%M:%S')

