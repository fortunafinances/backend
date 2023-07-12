from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Acc(db.Model):
    accId = db.Column(db.Integer, primary_key = True)
    userId = db.Column(db.Integer, db.ForeignKey("user.userId"), nullable = False)
    name = db.Column(db.String, nullable = False)
    cash = db.Column(db.Integer, nullable = False)