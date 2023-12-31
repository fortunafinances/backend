from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from threading import Lock

# Database import for model creating
db = SQLAlchemy()
db_lock = Lock()

class User(db.Model):
    # This data is fed from auth0 through frontend
    userId = db.Column(db.String, primary_key = True)
    username = db.Column(db.String, nullable = True)
    firstName = db.Column(db.String, nullable = True)
    lastName = db.Column(db.String, nullable = True)
    email = db.Column(db.String, nullable = True)
    phoneNumber = db.Column(db.String, nullable = True)
    picture = db.Column(db.String, nullable = True)
    bankName = db.Column(db.String, nullable = True)
    registerDate = db.Column(db.String, nullable = False)
    onboardingComplete = db.Column(db.Integer, nullable = False)

    def serialize(self):
        return {
            "userId": self.userId,
            "username": self.username,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "phoneNumber": self.phoneNumber,
            "picture": self.picture,
            "bankName": self.bankName,
            "registerDate": self.registerDate,
            "onboardingComplete": self.onboardingComplete
        }

# The accounts table
# Includes data on the name of the account,
# the user it belongs to and the amount of cash in the account
class Acc(db.Model):
    accId = db.Column(db.Integer, primary_key = True)
    userId = db.Column(db.String, db.ForeignKey("user.userId"), nullable = False)
    name = db.Column(db.String, nullable = False)
    cash = db.Column(db.Float, nullable = False)
    user = db.relationship("User", backref = db.backref("accs"), lazy = True)

    def serialize(self):
        return {
            "accId": self.accId,
            "userId": self.userId,
            "name": self.name,
            "cash": self.cash
        }

# AccHistory table
# Includes data on the holdings value of an account on a certain date
class AccHistory(db.Model):
    accHistoryId = db.Column(db.Integer, primary_key = True)
    accId = db.Column(db.Integer, db.ForeignKey("acc.accId"), nullable = False)
    value = db.Column(db.Float, nullable = False)
    date = db.Column(db.String, nullable = False)
    acc = db.relationship("Acc", backref = db.backref("accHistory"), lazy = True)

    def serialize(self):
        return {
            "accHistoryId": self.accHistoryId,
            "accId": self.accId,
            "value": self.value,
            "date": self.date
        }

# AccWatch table 
# Includes data on which account wants to keep track of which stock
class AccWatch(db.Model):
    accWatchId = db.Column(db.Integer, primary_key = True)
    accId = db.Column(db.Integer, db.ForeignKey("acc.accId"), nullable = False)
    ticker = db.Column(db.String, nullable = False)
    acc = db.relationship("Acc", backref = db.backref("accWatch"), lazy = True)

    def serialize(self):
        return {
            "accWatchId": self.accWatchId,
            "accId": self.accId,
            "ticker": self.ticker
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
    #identifying data
    ticker = db.Column(db.String, primary_key = True)
    companyName = db.Column(db.String)

    #price data
    currPrice = db.Column(db.Float, nullable = False)
    highPrice = db.Column(db.Float)
    lowPrice = db.Column(db.Float)
    openPrice = db.Column(db.Float)
    prevClosePrice = db.Column(db.Float)
    
    #meta data
    businessDescription = db.Column(db.String)
    sector = db.Column(db.String)
    country = db.Column(db.String)
    website = db.Column(db.String)
    officerTitle = db.Column(db.String)
    officerName = db.Column(db.String)

    def serialize(self):
        return {
            "ticker": self.ticker,
            "companyName": self.companyName,
            "currPrice": self.currPrice,
            "highPrice": self.highPrice,
            "lowPrice": self.lowPrice,
            "openPrice": self.openPrice,
            "prevClosePrice": self.prevClosePrice,
            "businessDescription": self.businessDescription,
            "sector": self.sector,
            "country": self.country,
            "website": self.website,
            "officerTitle": self.officerTitle,
            "officerName": self.officerName
        }

# StockHistory table
# Includes the stock's ticker and the price on a certain date
class StockHistory(db.Model):
    stockHistoryId = db.Column(db.Integer, primary_key = True)
    ticker = db.Column(db.String, nullable = False)
    price = db.Column(db.Float, nullable = False)
    date = db.Column(db.String, nullable = False)

    def serialize(self):
        return {
            "stockHistoryId": self.stockHistoryId,
            "ticker": self.ticker,
            "price": self.price,
            "date": self.date,
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
    # Possible statuses: "Placed" and "Executed" and "Expired"
    status = db.Column(db.String, nullable = False)
    tradeDate = db.Column(db.String, nullable = False)
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
    receiveAccId = db.Column(db.Integer, db.ForeignKey("acc.accId"), nullable = False)
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
            "date": self.date
        }