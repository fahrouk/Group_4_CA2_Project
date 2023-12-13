from app import db

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text)
    qty = db.Column(db.Integer)
    price = db.Column(db.Float)
    subTotal = db.Column(db.Float)

class Purchases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Text)
    image = db.Column(db.Text)
    quantity = db.Column(db.Integer)
    date = db.Column(db.Date)

