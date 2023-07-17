from tables import *
import sys
sys.path.insert(0, '../server')
from apiRequests import get_stock_list, get_stock_quote
from dataProcessing import handle_quote_data, handle_stock_list

# Inserting an account into the database.
def addAcc(name, cash):
    acc = Acc(
        name = name,
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
    
#makes and API call and returns a list of available stock symbols
def stock_list():
    data = get_stock_list('US')
    return handle_stock_list(data)

#function that updates the stock table
#can add a new stock or update the stock prices
def fillStocks():
    stockList = stock_list()
    for x in stockList:
        existing_stock = Stock.query.filter_by(ticker=x).first()
        data = get_stock_quote(x)
        price = handle_quote_data(data, x)
        # check if stock exists in table already
        if existing_stock is None:
            newStock = addNewStock(price)
            if newStock is not None:
                db.session.add(newStock)
        else:
            updateStock(existing_stock, price)
    db.session.commit()

#helper function that adds a new stock to the db
def addNewStock(price):
    if price is None:
        print("Error: price is None")
        return None
    try:
        newStock = Stock(
            ticker = price.ticker, 
            currPrice = price.curr_price, 
            highPrice = price.high_price, 
            lowPrice = price.low_price, 
            openPrice = price.opening_price, 
            prevClosePrice = price.previous_closing_price)
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

