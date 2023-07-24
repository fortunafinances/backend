from tables import db, User, Acc, AccStock, User, Trade, Transfer, Stock
from datetime import datetime, date
import pytz
from sqlalchemy import exc
import sys

def addUser(userId, username, nickname, email, picture, dateOfBirth, onboardingComplete):
    existing_user = User.query.get(userId)
    if existing_user is not None:  # if the user already exists
        updated_user = updateUser(existing_user, username, nickname, email, picture, dateOfBirth, onboardingComplete)
        db.session.commit()
        return "userId already exists, necessary fields were updated", True, updated_user
    
    user = User(
        userId = userId,
        username = username,
        nickname = nickname,
        email = email,
        picture = picture,
        dateOfBirth = dateOfBirth,
        registerDate = date.today(),
        onboardingComplete = False
    )

    db.session.add(user)
    db.session.commit()
    return "Success", False, user


def updateUser(existing_user, username, nickname, email, picture, dateOfBirth, onboardingComplete):
    # the below functionality only updates the field if it has been provided by the frontend
    # a default value of None is given for non inserted fields in graphql
    if username is not None:
        existing_user.username = username
    if nickname is not None:
        existing_user.nickname = nickname
    if email is not None:
        existing_user.email = email
    if dateOfBirth is not None:
        existing_user.dateOfBirth = dateOfBirth
    if picture is not None:
        existing_user.picture = picture
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
    



