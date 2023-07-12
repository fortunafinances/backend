from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Trade(db.Model):
    tradeId = db.Column(db.Integer, primary_key = True)
    accId = db.Column(db.Integer, db.ForeignKey("acc.accId"), nullable = False)
    type = db.Column(db.String, nullable = False)
    side = db.Column(db.String, nullable = False)
    tradeDate = db.Column(db.String, nullable = False)
    ticker = db.Column(db.String, nullable = False)
    status = db.Column(db.String, nullable = False)
    tradePrice = db.Column(db.Integer, nullable = False)
    tradeQty = db.Column(db.Integer, nullable = False)
    acc = db.relationship("Acc", backref = db.backref("orders"),lazy = True)