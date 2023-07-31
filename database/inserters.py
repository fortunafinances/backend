from tables import db, User, Acc, AccHistory, AccWatch, AccStock, User, Trade, Transfer, Stock, StockHistory
from datetime import datetime, date
import pytz
from sqlalchemy import exc
import sys

def addUser(userId, username, firstName, lastName, email, phoneNumber, picture, bankName, onboardingComplete):
    existing_user = User.query.get(userId)
    if existing_user is not None:  # if the user already exists
        updated_user = updateUser(existing_user, username, firstName, lastName, email, phoneNumber, picture, bankName, onboardingComplete)
        db.session.commit()
        return "userId already exists, necessary fields were updated", updated_user
    
    user = User(
        userId = userId,
        username = username,
        firstName = firstName,
        lastName = lastName,
        email = email,
        phoneNumber = phoneNumber,
        picture = picture,
        bankName = bankName,
        registerDate = date.today(),
        onboardingComplete = False
    )

    db.session.add(user)
    db.session.commit()
    return "Success", user


def updateUser(existing_user, username, firstName, lastName, email, phoneNumber, picture, bankName, onboardingComplete):
    # the below functionality only updates the field if it has been provided by the frontend
    # a default value of None is given for non inserted fields in graphql
    if username is not None:
        existing_user.username = username
    if firstName is not None:
        existing_user.firstName = firstName
    if lastName is not None:
        existing_user.lastName = lastName
    if email is not None:
        existing_user.email = email
    if phoneNumber is not None:
        existing_user.phoneNumber = phoneNumber
    if picture is not None:
        existing_user.picture = picture
    if bankName is not None:
        existing_user.bankName = bankName
    if onboardingComplete is not None:
        existing_user.onboardingComplete = onboardingComplete
    
    return existing_user
    


# Inserting an account into the database.
def addAcc(name, userId, cash):
    acc = Acc(
        name = name,
        userId = userId,
        cash = cash
    )
    db.session.add(acc)
    db.session.commit()
    return acc, "Account Inserted"

def addAccHistory(accId, value, date):
    accHistory = AccHistory(
        accId = accId,
        value = value,
        date = date
    )
    db.session.add(accHistory)
    db.session.commit()

def addAccWatch(accId, ticker):
    accWatch = AccWatch(
        accId = accId,
        ticker = ticker
    ) 
    db.session.add(accWatch)
    db.session.commit()
    
# Inserting an accStock into the database
def addAccStock(accId, ticker, stockQty):
    accStock = AccStock(
        accId = accId,
        ticker = ticker,
        stockQty = stockQty
    )
    db.session.add(accStock)
    db.session.commit()

# Inserting a Trade into the database
def addTrade(accId, type, side, status, tradeDate, ticker, tradePrice, tradeQty):
    trade = Trade(
        accId = accId,
        type = type,
        side = side,
        status = status,
        tradeDate = tradeDate,
        ticker = ticker,
        tradePrice = tradePrice,
        tradeQty = tradeQty
    )
    db.session.add(trade)
    db.session.commit()

# Inserting a Transfer into the database
def addTransfer(sendAccId, receiveAccId, transferAmt, date):
    transfer = Transfer(
        sendAccId = sendAccId,
        receiveAccId = receiveAccId,
        transferAmt = transferAmt,
        date = date,
    )
    db.session.add(transfer)
    db.session.commit()

def addStockHistory(ticker, price, date):
    stockHistory = StockHistory(
        ticker = ticker,
        price = price,
        date = date
    )
    db.session.add(stockHistory)
    db.session.commit()

# Buys a stock using the market order option
def buyMarket(accId, ticker, tradeQty):
    # Initial set up of grabbing the account, stockprice and the current time
    acc = Acc.query.get(accId)
    tradePrice = Stock.query.get(ticker).currPrice
    tradeDate = datetime.now(tz = pytz.timezone("US/Eastern")).isoformat()

    # Checks if the account has enough funds and 
    # to return success or error based on that
    if (acc.cash > tradePrice * tradeQty):
        # Update account cash value
        acc.cash -= tradePrice * tradeQty
        db.session.commit()

        addTrade(accId, "Market", "Buy", "Executed", 
                    tradeDate, ticker, tradePrice, tradeQty)

        # accStock existence check
        accStock = AccStock.query.filter_by(accId = accId, ticker = ticker).first()

        # updates the accStock if it exists, adds one if not
        if (accStock):
            accStock.stockQty += tradeQty
            db.session.commit()
        else:
            addAccStock(accId, ticker, tradeQty)

        return "Success"

    return "Error: Not enough funds in account"
            
# Sells a stock using the market order option
def sellMarket(accId, ticker, tradeQty):
    # Initial set up of grabbing the account, accStock
    # stockprice and the current time
    acc = Acc.query.get(accId)
    accStock = AccStock.query.filter_by(accId = accId, ticker = ticker).first()
    tradePrice = Stock.query.get(ticker).currPrice
    tradeDate = datetime.now(tz = pytz.timezone("US/Eastern")).isoformat()

    # Checks if the account has enough stocks 
    # and to return success or error based on that
    if (accStock and accStock.stockQty >= tradeQty):
        # update account cash value
        acc.cash += tradePrice * tradeQty

        addTrade(accId, "Market", "Sell", "Executed", 
                    tradeDate, ticker, tradePrice, tradeQty)
        
        # removes accStock if it reaches 0 or simply subtracts the amount
        if (accStock.stockQty == tradeQty):
            db.session.delete(accStock)
            db.session.commit()
        else:
            accStock.stockQty -= tradeQty
            db.session.commit()

        return "Success"
    
    return "Error: Not enough shares to sell"

#inserts new trade into trade table, specifically an unexecuted limit order
def placeBuyLimit(accId, ticker, tradeQty, limitPrice):
    acc = Acc.query.get(accId)
    tradeDate = datetime.now(tz = pytz.timezone("US/Eastern")).isoformat()

    if (acc.cash > limitPrice * tradeQty):
        #insert trade into table 
        #status = placed
        addTrade(accId, "Limit", "Buy", "Placed", tradeDate, ticker, limitPrice, tradeQty)
        return "Success"
    else:
        return "Error: Not enough funds in account."
    
def placeSellLimit(accId, ticker, tradeQty, limitPrice):
    accStock = AccStock.query.filter_by(accId = accId, ticker = ticker).first()
    tradeDate = datetime.now(tz = pytz.timezone("US/Eastern")).isoformat()

    if (accStock and accStock.stockQty >= tradeQty):
        addTrade(accId, "Limit", "Sell", "Placed", tradeDate, ticker, limitPrice, tradeQty)
        return "Success"
    else:
        return "Error: Not enough stock owned to sell"
    
def executeLimit(tradeId):
    trade = Trade.query.get(tradeId)
    acc = Acc.query.get(trade.accId)
    stockPrice = Stock.query.get(trade.ticker).currPrice
    totalPrice = trade.tradeQty * stockPrice
    accStock = AccStock.query.filter_by(accId = trade.accId, ticker = trade.ticker).first()
    print ("executeLimit() is being accessed")
    if trade.side == "Buy":
        print ("we buying")
        if (acc.cash > totalPrice):
            acc.cash -= totalPrice
        
            if (accStock):
                #add trade.tradeQty to stockQty
                accStock.stockQty += trade.tradeQty
            else:
                #add new acc stock
                addAccStock(trade.accId, trade.ticker, trade.tradeQty)
            trade.status = "Executed"
            trade.tradeDate = datetime.now(tz = pytz.timezone("US/Eastern")).isoformat()
            db.session.commit()
            return "Success"
        else:
            trade.status = "Expired"
            db.session.commit()
            return "Error: Not enough funds to execute Buy Limit order. Limit order has expired"
    

    if trade.side == "Sell":
        print ("we selling")
        if (AccStock and accStock.stockQty >= trade.tradeQty):
            acc.cash += totalPrice
            accStock.stockQty -= trade.tradeQty
            trade.status = "Executed"
            if (accStock.stockQty == 0):
                #remove stock from AccStocks
                deleteAccStock(accStock)
            db.session.commit()
            return "Success"
        else:
            trade.status = "Expired"
            db.session.commit()
            return "Error: Not enough stocks owned to execute Sell Limit order. Limit order has expired."


def deleteAccStock(accStock):
    db.session.delete(accStock)
    db.session.commit()


# Transfers funds from one account to another. 
# Can involve an outside account in either direction or between accounts
def doTransfer(sendAccId, receiveAccId, transferAmt):
    # Initial set up of grabbing accounts and the current time
    sendAcc = Acc.query.get(sendAccId)
    receiveAcc = Acc.query.get(receiveAccId)
    date = datetime.now(tz = pytz.timezone("US/Eastern")).isoformat()

    # Allows the transfer if there is an external account
    # or the sender account has enough money
    if (sendAcc == None or sendAcc.cash > transferAmt):
        addTransfer(sendAccId, receiveAccId, transferAmt, date)

        # Removes cash from sender account if it's internal
        if (sendAcc):
            sendAcc.cash -= transferAmt
            db.session.commit()

        # Adds cash to the receiver account if it's internal
        if (receiveAcc):
            receiveAcc.cash += transferAmt
            db.session.commit()
        
        return "Success"
    
    return "Error: Not enough funds in sending account"

        
# Inserting a Stock into the database
def testStock(ticker, currPrice, highPrice, lowPrice, openPrice, prevClosePrice):
    stock1 = Stock(
        ticker = ticker, 
        currPrice = currPrice, 
        highPrice = highPrice, 
        lowPrice = lowPrice, 
        openPrice = openPrice, 
        prevClosePrice = prevClosePrice
    )
    db.session.add(stock1)
    db.session.commit()
    



