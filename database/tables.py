from flask_sqlalchemy import SQLAlchemy

# Database import for model creating
db = SQLAlchemy()

# The accounts table
# Includes data on the name of the account,
# the user it belongs to and the amount of cash in the account
class Acc(db.Model):
    accId = db.Column(db.Integer, primary_key = True)
    # userId = db.Column(db.Integer, db.ForeignKey("user.userId"), nullable = False)
    name = db.Column(db.String, nullable = False)
    cash = db.Column(db.Float, nullable = False)

    def serialize(self):
        return {
            "accId": self.accId,
            # "userId": self.userId,
            "name": self.name,
            "cash": self.cash
        }

# The AccStock table
# Includes data on the name of the stock,
# which account it belongs to and 
# the ticker and qty of the stock 
class AccStock(db.Model):
    accStockId = db.Column(db.Integer, primary_key = True)
    accId = db.Column(db.Integer, db.ForeignKey("acc.accId"), nullable = False)
    ticker = db.Column(db.String, nullable = False)
    stockQty = db.Column(db.Integer, nullable = False)
    acc = db.relationship("Acc", backref = db.backref("accStocks"), lazy = True)

    def serialize(self):
        return {
            "accStockId": self.accStockId,
            "accId": self.accId,
            "ticker": self.ticker,
            "stockQty": self.stockQty
        }

# The Stock table
# Includes data about the ticker, current,
# high, low, open and previous close prices
class Stock(db.Model):
    ticker = db.Column(db.String, primary_key = True)
    currPrice = db.Column(db.Float, nullable = False)
    highPrice = db.Column(db.Float)
    lowPrice = db.Column(db.Float)
    openPrice = db.Column(db.Float)
    prevClosePrice = db.Column(db.Float)

    def serialize(self):
        return {
            "ticker": self.ticker,
            "currPrice": self.currPrice,
            "highPrice": self.highPrice,
            "lowPrice": self.lowPrice,
            "openPrice": self.openPrice,
            "prevClosePrice": self.prevClosePrice
        }

# The trade table
# Includes data on the trade's type, side, status,
# trade date, ticker, trade price and qty with a 
# connection to an account
class Trade(db.Model):
    tradeId = db.Column(db.Integer, primary_key = True)
    accId = db.Column(db.Integer, db.ForeignKey("acc.accId"), nullable = False)
    # Possible types: "Limit" and "Market"
    type = db.Column(db.String, nullable = False)
    # Possible sides: "Buy" and "Sell"
    side = db.Column(db.String, nullable = False)
    # Possible statuses: "Placed" and "Executed"
    status = db.Column(db.String, nullable = False)
    tradeDate = db.Column(db.Integer, nullable = False)
    ticker = db.Column(db.String, nullable = False)
    tradePrice = db.Column(db.Float, nullable = False)
    tradeQty = db.Column(db.Integer, nullable = False)
    acc = db.relationship("Acc", backref = db.backref("orders"),lazy = True)

    def serialize(self):
        return {
            "tradeId": self.tradeId,
            "accId": self.accId,
            "type": self.type,
            "side": self.side,
            "status": self.status,
            "tradeDate": self.tradeDate,
            "ticker": self.ticker,
            "tradePrice": self.tradePrice,
            "tradeQty": self.tradeQty
        }

# The transfer table 
# Includes data about a transfer's amount, date 
# and the sender and receiver AccIds
class Transfer(db.Model):
    transferId = db.Column(db.Integer, primary_key = True)
    sendAccId = db.Column(db.Integer, db.ForeignKey("acc.accId"), nullable = False)
    receiveAccId = db.Column(db.Float, db.ForeignKey("acc.accId"), nullable = False)
    transferAmt = db.Column(db.Float, nullable = False)
    date = db.Column(db.String, nullable = False)
    sendAcc = db.relationship("Acc", foreign_keys = [sendAccId], backref = db.backref("outgoing", lazy = True))
    receiveAcc = db.relationship("Acc", foreign_keys = [receiveAccId], backref = db.backref("incoming"), lazy = True)

    def serialize(self):
        return {
            "transferId": self.transferId,
            "sendAccId": self.sendAccId,
            "receiveAccId": self.receiveAccId,
            "transferAmt": self.transferAmt,
            "date": self.date,
            "prevClosePrice": self.prevClosePrice
        }