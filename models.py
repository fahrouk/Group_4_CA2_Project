from app import db

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text)
    qty = db.Column(db.Integer)
    price = db.Column(db.Float)
    subTotal = db.Column(db.Float)

