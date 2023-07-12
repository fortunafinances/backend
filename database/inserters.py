from tables import *


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

def testAccStock():
    accStock1 = AccStock(
        accId = 1,
        ticker = "TSLA",
        stockQty = 1 
    )
    db.session.add(accStock1)
    db.session.commit()

def testStock():
    stock1 = Stock(
        ticker = "TSLA", 
        currPrice = 20523, 
        highPrice = 24543, 
        lowPrice = 19234, 
        openPrice = 20326, 
        prevClosePrice = 21032
    )
    db.session.add(stock1)
    db.session.commit()

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

def testRelations():
    trades = Acc.query.get(1).orders
    print(trades[0].tradePrice)

# def testTransfer():
#     transfer1 = Transfer(
#         sendAccId = 1,
#         receiveAccId = 2,
#         transferAmt = 200,
#         date = "12/31/1969",
#     )
#     db.session.add(transfer1)
#     db.session.commit()