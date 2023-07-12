from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AccStock(db.Model):
    accStockId = db.Column(db.Integer, primary_key = True)
    accId = db.Column(db.Integer, db.ForeignKey("acc.addId"), nullable = False)
    ticker = db.Column(db.String, nullable = False)
    cash = db.Column(db.Integer, nullable = False)
    acc = db.relationship("Acc", backref = db.backref("accStocks"), lazy = True)
