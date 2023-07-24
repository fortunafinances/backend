#####################################################
#                   CLASSES                         #
#####################################################

class Stock:
    def __init__(self, 
                ticker,
                name,
                currPrice,
                highPrice,
                lowPrice,
                openPrice,
                prevClosePrice,
                description,
                sector,
                country,
                website,
                officerTitle,
                officerName):
       self.ticker = ticker
       self.name = name
       self.currPrice = currPrice
       self.highPrice = highPrice
       self.lowPrice = lowPrice
       self.openPrice = openPrice
       self.prevClosePrice = prevClosePrice
       self.description = description
       self.sector = sector
       self.country = country
       self.website = website
       self.officerTitle = officerTitle
       self.officerName = officerName

       
class Trade:
    def __init__(self, 
                accID,
                type,
                side,
                ticker,
                tradeQty):
       self.accID = accID
       self.type = type
       self.side = side
       self.ticker = ticker
       self.tradeQty = tradeQty

class Holding:
    def __init__(self, accountId, stockQuantity, stock):
        self.accountId = accountId
        self.stockQuantity = stockQuantity
        self.stock = stock

class Order:
    def __init__(self, accountId, type, side, status, tradePrice, tradeQty, date, stock):
        self.accId = accountId
        self.type = type
        self.side = side
        self.status = status
        self.tradePrice = tradePrice
        self.tradeQty = tradeQty
        self.date = date
        self.stock = stock

        
class Activity:
    def __init__(self, accountId, date, type, description, amount):
        self.accountId = accountId
        self.date = date
        self.type = type
        self.description = description
        self.amount = amount

class DisplayBar:
    def __init__(self, total, invest, cash):
        self.total = total
        self.invest = invest
        self.cash = cash

class Account:
    def __init__(self, accId, name, cash):
        self.accId = accId
        self.name = name
        self.cash = cash

class User:
    def __init__(self, userId, username, nickname, email, dateOfBirth, picture):
        self.userId = userId
        self.username = username
        self.nickname = nickname
        self.email = email
        self.dateOfBirth = dateOfBirth
        self.picture = picture
