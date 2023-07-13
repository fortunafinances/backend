from tables import *
import sys
sys.path.insert(0, '../server')
from apiRequests import get_stock_list, get_stock_quote
from dataProcessing import handle_quote_data, handle_stock_list

# Static test method for inserting an account into the database.
def testAcc():
    acc1 = Acc(
        name = "Joe",
        cash = 1000
    )
    acc2 = Acc(
        name = "Cathy",
        cash = 500
    )
    db.session.add(acc1)
    db.session.commit()
    db.session.add(acc2)
    db.session.commit()

# Static test method for inserting an accStock into the database
def testAccStock():
    accStock1 = AccStock(
        accId = 1,
        ticker = "MSFT",
        stockQty = 1 
    )
    db.session.add(accStock1)
    db.session.commit()

# Static test method for inserting a Stock into the database
def testStock():
    stock1 = Stock(
        ticker = "MSFT", 
        currPrice = 8523, 
        highPrice = 10543, 
        lowPrice = 7834, 
        openPrice = 8326, 
        prevClosePrice = 9032
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


# Static test method for inserting a Trade into the database
def testTrade():
    trade1 = Trade(
        accId = 1,
        #tradeId = 1,
        type = "Buy",
        side = "Market",
        status = "Executed",
        tradeDate = "12/31/1969",
        ticker = "MSFT",
        tradePrice = 24523,
        tradeQty = 1
    )
    db.session.add(trade1)
    db.session.commit()

# Static test method for inserting a Transfer into the database
def testTransfer():
    transfer1 = Transfer(
        sendAccId = 1,
        receiveAccId = 2,
        transferAmt = 200,
        date = "12/31/1969",
    )
    db.session.add(transfer1)
    db.session.commit()
