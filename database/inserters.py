from tables import *

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