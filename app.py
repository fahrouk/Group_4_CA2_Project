from cs50 import SQL
from flask_session import Session
from flask import Flask, render_template,session, redirect,request
from datetime import datetime
import locale

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "CA2_Project"
Session(app)
