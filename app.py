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
db = SQL ( "sqlite:///data.db" )
@app.route("/")
def index():
    books = db.execute("select * FROM books")
    booksLen = len(books)
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems= 0
    total=0
    display=0
    if 'user' in session:
        shoppingCart = db.execute("select image, SUM(qty), SUM(subTotal), price, id FROM cart")
        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
        books = db.execute("SELECT * FROM books")
        booksLen = len(books)
        return render_template ("index.html", shoppingCart=shoppingCart, books=books, shopLen=shopLen, booksLen=booksLen, total=total, totItems=totItems, display=display, session=session )
    return render_template ("index.html", books=books, shoppingCart=shoppingCart, booksLen=booksLen, shopLen=shopLen, total=total, totItems=totItems, display=display)

@app.route("/login/", methods=["GET"])
def login():
