from cs50 import SQL
from flask_session import Session
from flask import Flask, render_template,session, redirect,request, url_for
from datetime import datetime
import locale
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "CA2_Project"
Session(app)
db = SQL ("sqlite:///data.db")

@app.route("/login/", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/signup/", methods=["GET"])
def signup():
    return render_template("signup.html")

@app.route("/register/", methods=["POST"])
def registration():
    if request.method == "POST":
        uname = request.form["uname"]
        pwd = request.form["pwd"]
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]

        # Check if the username already exists
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=uname)
        if len(rows) > 0:
            return render_template("signup.html", msg="Username already exists!")

        # Insert new user into the database
        new = db.execute(
            "INSERT INTO users (username, password, fname, lname, email) VALUES (:uname, :pwd, :fname, :lname, :email)",
            uname=uname, pwd=pwd, fname=fname, lname=lname, email=email
        )

        return render_template("login.html")

    # If not a POST request, redirect to the signup page
    return redirect(url_for("signup"))

@app.route("/logout/")
def logout():
    db.execute("delete from cart")
    session.clear()
    return redirect("/")

@app.route("/logged/", methods=["POST"] )
def logged():
    user = request.form["uname"].lower()
    pwd = request.form["pwd"]

    if user == "" or pwd == "":
        return render_template("login.html")

    query = "SELECT * FROM users WHERE username = :user AND password = :pwd"
    rows = db.execute(query, user=user, pwd=pwd)

    if len(rows) == 1:
        # Set user information in the session
        session['user'] = user
        session['time'] = datetime.now()
        session['uid'] = rows[0]["id"]

        # Redirect to the home page or any other desired page
        return redirect(url_for('index'))
    return render_template ( "login.html", msg="invalid username or password." )
       
