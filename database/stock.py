from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Stock(db.Model):
    ticker = db.Column(db.String, primary_key = True)
    currPrice = db.Column(db.Integer, nullable = False)
    highPrice = db.Column(db.Integer)
    lowPrice = db.Column(db.Integer)
    openPrice = db.Column(db.Integer)
    prevClosePrice = db.Column(db.Integer)