from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Acc(db.Model):
    accId = db.Column(db.Integer, primary_key = True)
    # userId = db.Column(db.Integer, db.ForeignKey("user.userId"), nullable = False)
    name = db.Column(db.String, nullable = False)
    cash = db.Column(db.Integer, nullable = False)

class AccStock(db.Model):
    accStockId = db.Column(db.Integer, primary_key = True)
    accId = db.Column(db.Integer, db.ForeignKey("acc.accId"), nullable = False)
    ticker = db.Column(db.String, nullable = False)
    stockQty = db.Column(db.Integer, nullable = False)
    acc = db.relationship("Acc", backref = db.backref("accStocks"), lazy = True)

class Stock(db.Model):
    ticker = db.Column(db.String, primary_key = True)
    currPrice = db.Column(db.Integer, nullable = False)
    highPrice = db.Column(db.Integer)
    lowPrice = db.Column(db.Integer)
    openPrice = db.Column(db.Integer)
    prevClosePrice = db.Column(db.Integer)

class Trade(db.Model):
    tradeId = db.Column(db.Integer, primary_key = True)
    accId = db.Column(db.Integer, db.ForeignKey("acc.accId"), nullable = False)
    type = db.Column(db.String, nullable = False)
    side = db.Column(db.String, nullable = False)
    status = db.Column(db.String, nullable = False)
    tradeDate = db.Column(db.Integer, nullable = False)
    ticker = db.Column(db.String, nullable = False)
    tradePrice = db.Column(db.Integer, nullable = False)
    tradeQty = db.Column(db.Integer, nullable = False)
    acc = db.relationship("Acc", backref = db.backref("orders"),lazy = True)

# class Transfer(db.Model):
#     transferId = db.Column(db.Integer, primary_key = True)
#     sendAccId = db.Column(db.Integer, db.ForeignKey("acc.accId"), nullable = False)
#     receiveAccId = db.Column(db.Integer, db.ForeignKey("acc.accId"), nullable = False)
#     transferAmt = db.Column(db.Integer, nullable = False)
#     date = db.Column(db.String, nullable = False)
#     sendAcc = db.relationship("Acc", backref = db.backref("outgoing", lazy = True))
#     receiveAcc = db.relationship("Acc", backref = db.backref("incoming"), lazy = True)
