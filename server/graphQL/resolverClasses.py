#####################################################
#                   CLASSES                         #
#####################################################

class Stock:
    def __init__(self, 
                ticker = "",
                name = "",
                currPrice = 0.0,
                highPrice = 0.0,
                lowPrice = 0.0,
                openPrice = 0.0,
                prevClosePrice = 0.0,
                description = "",
                sector = "",
                country = "",
                website = "",
                officerTitle = "",
                officerName = ""):
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
    def __init__(self, id, accId, stockQuantity, stock):
        self.id = id
        self.accId = accId
        self.stockQuantity = stockQuantity
        self.stock = stock

class Order:
    def __init__(self, id, accountId, type, side, status, tradePrice, tradeQty, date, stock):
        self.id = id
        self.accId = accountId
        self.type = type
        self.side = side
        self.status = status
        self.tradePrice = tradePrice
        self.tradeQty = tradeQty
        self.date = date
        self.stock = stock

class Activity:
    def __init__(self, id, accId, date, type, description, amount):
        self.id = id
        self.accId = accId
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
    def __init__(self, userId, 
                username, 
                firstName,
                lastName, 
                email,
                phoneNumber,
                picture,
                bankName,   
                registerDate,
                onboardingComplete):
        self.userId = userId
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.phoneNumber = phoneNumber
        self.picture = picture
        self.bankName = bankName
        self.registerDate = registerDate
        self.onboardingComplete = onboardingComplete

class PieData:
    def __init__(self, dic_labels_values, message):
        self.labels = list(dic_labels_values.keys())
        self.values = list(dic_labels_values.values())
        self.message = message

class StockHistory:
    def __init__(self, id, ticker, data, message):
        self.id = id
        self.ticker = ticker
        self.data = data
        self.message = message

class AccountHistory:
    def __init__(self, id, accId, data, message):
        self.id = id
        self.accId = accId
        self.data = data
        self.message = message

class AccountWatch:
    def __init__(self, id, accId, ticker):
        self.id = id
        self.accId = accId
        self.ticker = ticker

class LinePoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y


################ RETURN CLASSES #########################
class ReturnUser:
    def __init__(self, user, message):
        self.user = user
        self.message = message

class ReturnAccount:
    def __init__(self, account, message):
        self.account = account
        self.message = message

class ReturnAccountWatch:
    def __init__(self, accountWatch, message):
        self.accountWatch = accountWatch
        self.message = message