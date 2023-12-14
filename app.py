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

@app.route("/")
def index():
    check= db.execute("SELECT * FROM gym WHERE kind = :value",value="5KG-Dumbell")
    print(check)
    gym = db.execute("select * FROM gym")
    gymLen = len(gym)
    shoppingCart = []
    shopLen1 = len(shoppingCart)
    print(shopLen1)
    totItems= 0
    total=0
    display=0
    if 'user' in session:
        shoppingCart = db.execute("select image, SUM(qty), SUM(subTotal), price, id FROM cart")
        print(shoppingCart)
        shopLen = len(shoppingCart)
        print(shopLen)
        if any(cart_item['image'] is not None for cart_item in shoppingCart):
            print(shopLen)
            for i in range(shopLen):
                total += shoppingCart[i]["SUM(subTotal)"]
                totItems += shoppingCart[i]["SUM(qty)"]
            gym = db.execute("SELECT * FROM gym")
            gymLen = len(gym)
            return render_template ("index.html", gym=gym, shoppingCart=shoppingCart, gymLen=gymLen, shopLen=shopLen, total=total, totItems=totItems, display=display)
    return render_template ("index.html", gym=gym, shoppingCart=shoppingCart, gymLen=gymLen, shopLen=shopLen1, total=total, totItems=totItems, display=display)

@app.route("/purchase_history/")
def history():
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems=0
    total=0
    display=0
    print(session["uid"])
    mygym = db.execute("SELECT * FROM purchases WHERE uid=:value", value=session["uid"])
    print(mygym)
    mygymLen = len(mygym)
    return render_template("purchase_history.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session, mygym=mygym, mygymLen=mygymLen)

@app.route("/cart/")
def cart():
    if 'user' in session:
        totItems, total, display = 0, 0, 0
        shoppingCart = db.execute("SELECT image, SUM(qty), SUM(subTotal), price, id FROM cart")
        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]    
    return render_template("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session)

@app.route("/remove/", methods=["GET"])
def remove():
     out = int(request.args.get("id"))
     db.execute("DELETE from cart WHERE id=:id", id=out)
     totItems, total, display = 0, 0, 0
     shoppingCart = db.execute("SELECT image, SUM(qty), SUM(subTotal), price, id FROM cart")
     shopLen = len(shoppingCart)
     for i in range(shopLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(qty)"]
     display = 1
     return render_template ("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session)


@app.route("/filter/")
def filter():
    if request.args.get('sale'):
        query = request.args.get('sale')
        gym = db.execute("SELECT * FROM gym WHERE onSale = :query", query=query)
    
    if request.args.get('kind'):
        query = request.args.get('kind')
        gym = db.execute("SELECT * FROM gym WHERE kind = :query", query=query)
        
    if request.args.get('price'):
        query = request.args.get('price')
        gym = db.execute("SELECT * FROM gym")
        
    gymLen = len(gym)
    
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    if 'user' in session:
        
        shoppingCart = db.execute("SELECT image, SUM(qty), SUM(subTotal), price, id FROM cart")
        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
        
        return render_template ("index.html", shoppingCart=shoppingCart, gym=gym, shopLen=shopLen, gymLen=gymLen, total=total, totItems=totItems, display=display, session=session )
    
    return render_template ( "index.html", gym=gym, shoppingCart=shoppingCart, gymLen=gymLen, shopLen=shopLen, total=total, totItems=totItems, display=display)


@app.route("/buy/")
def buy():
    print("entering buy")
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    qty = int(request.args.get('quantity'))
    print(qty)
    if session:
        id = int(request.args.get('id'))
        goods = db.execute("SELECT * FROM gym WHERE id = :id", id=id)
        
        if(goods[0]["onSale"] == 1):
            price = goods[0]["onSalePrice"]
        else:
            price = goods[0]["price"]
        image = goods[0]["image"]
        subTotal = qty * price
        db.execute("INSERT INTO cart (id, qty, image, price, subTotal) VALUES (:id, :qty, :image, :price, :subTotal)", id=id, qty=qty, image=image, price=price, subTotal=subTotal)
        shoppingCart = db.execute("SELECT image, SUM(qty), SUM(subTotal), price, id FROM cart")
        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
        gym = db.execute("SELECT * FROM gym")
        gymLen = len(gym)
     
        return render_template ("index.html", shoppingCart=shoppingCart, gym=gym, shopLen=shopLen, gymLen=gymLen, total=total, totItems=totItems, display=display, session=session )

@app.route('/final/')
def finalpage():
    return render_template("final.html")

@app.route("/update/")
def update():
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    qty = int(request.args.get('quantity'))
    if session:
        id = int(request.args.get('id'))
        db.execute("DELETE FROM cart WHERE id = :id", id=id)
     
        gymitems = db.execute("SELECT * FROM gym WHERE id = :id", id=id)
       
        if(gymitems[0]["onSale"] == 1):
            price = gymitems[0]["onSalePrice"]
        else:
            price = gymitems[0]["price"]
        team = gymitems[0]["team"]
        image = gymitems[0]["image"]
        subTotal = qty * price
       
        db.execute("INSERT INTO cart (id, qty,image, price, subTotal) VALUES (:id, :qty,:image, :price, :subTotal)", id=id, qty=qty, image=image, price=price, subTotal=subTotal)
        shoppingCart = db.execute("SELECT image, SUM(qty), SUM(subTotal), price, id FROM cart")
        shopLen = len(shoppingCart)
   
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
       
        return render_template ("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session )


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    app.run(port=8080, debug = True)

       
