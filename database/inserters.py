from tables import *
from datetime import datetime, date
import pytz
import sys
sys.path.insert(0, '../server')
sys.path.insert(0, '../mockData')
from constants import STOCK_LIST
from apiRequests import get_stock_list, get_stock_metadata, get_stock_quote
from dataProcessing import handle_metadata, handle_quote_data

def addUser(username, nickname, email, picture):
    user = User(
        username = username,
        nickname = nickname,
        email = email,
        # dateOfBirth = dateOfBirth,
        picture = picture,
        
        registerDate = date.today()
    )
    db.session.add(user)
    db.session.commit()

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
    
#makes and API call and returns a list of dictionaries, [ticker, companyName]
# def stock_list():
#     data = get_stock_list('US')
#     return handle_stock_list(data)

#function that updates the stock table
#can add a new stock or update the stock prices
def fillStocks():
    for ticker, description in STOCK_LIST.items():
        data = get_stock_quote(ticker)
        price = handle_quote_data(data)
        existing_stock = Stock.query.get(ticker)
        
        if existing_stock is not None:
            #update stock prices
            updateStock(existing_stock, price)
        else:
            #add new stock
            newStock = addNewStock(ticker, description, price)
            if newStock is not None:
                if newStock.businessDescription is not None and newStock.sector is not None:
                    db.session.add(newStock)
    db.session.commit()


#helper function that adds a new stock to the db
def addNewStock(ticker, description, price):
    data = get_stock_metadata(ticker)
    metadata = handle_metadata(data)

    if price is None:
        print("Error: price is None")
        return None
    try:
        newStock = Stock(
            ticker = ticker,
            companyName = description,
            currPrice = price.curr_price, 
            highPrice = price.high_price, 
            lowPrice = price.low_price, 
            openPrice = price.opening_price, 
            prevClosePrice = price.previous_closing_price,
            businessDescription = metadata.businessDescription,
            country = metadata.country,
            sector = metadata.sector,            
            website = metadata.website,
            officerTitle = metadata.headOfficer[0],
            officerName = metadata.headOfficer[1])

    except AttributeError as e:
        print(f"Error: {e}")
        return None

    return newStock

#helper function that updates the stock prices in the db
def updateStock(existing_stock, price):
        existing_stock.currPrice = price.curr_price
        existing_stock.highPrice = price.high_price
        existing_stock.lowPrice = price.low_price
        existing_stock.openPrice = price.opening_price
        existing_stock.prevClosePrice = price.previous_closing_price    


#function that clears the stock table in the db 
def clearStockTable():
    Stock.query.delete()
    db.session.commit()

