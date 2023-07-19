import json
from flask import jsonify
import sys
from tables import *

# Tester function to test a query and relations 
def testRelations():
    # returns the array of orders of the acc w/ id 1
    trades = Acc.query.get(1).orders
    # gets the tradePrice of the 0th trade in the orders array
    print(trades[0].tradePrice)

# Returns an account's monetary values in terms of total assets,
# investments and cash
def getDisplayBar(accId):
    acc = (Acc.query.get(accId))
    total = 0
    invest = 0    

    # For loop to add up all of the investments 
    for accStock in acc.accStocks:
        invest += (Stock.query.get(accStock.ticker)).currPrice * accStock.stockQty
    total = acc.cash + invest
    
    return {"total": total, "invest": invest, "cash": acc.cash}

# Returns a list of stocks that the account owns and the respective
# prices of those stocks
def getHoldings(accId):
    accStocks = AccStock.query.filter(AccStock.accId == accId)
    holdings = list()

    # For loop to retrieve each holding in the accStocks list
    for holding in accStocks:
        stock = Stock.query.get(holding.ticker)
        holdings.append({
            "ticker": holding.ticker,
            "stockQty": holding.stockQty,
            "currPrice": stock.currPrice
            })
        
    return holdings

# Returns the contents of a singular stock
def getStock(ticker):
    stock = Stock.query.get(ticker)
    return stock.serialize()

# Returns a list of all of the stocks
def getStocks():
    stocks = (Stock.query.all())
    list_of_stocks = [stock.serialize() for stock in stocks]
    return list_of_stocks

# Returns a list of all of the accs
def getAccs():
    accs = (Acc.query.all())
    return [acc.serialize() for acc in accs]

#Returns a list of transfers and trades associated with a certain account id
def getActivity(accID):
    trades = getTrades(accID)
    transfers = getTransfers(accID)
    activity = trades + transfers
    return activity

#helper method that returns a list of all trades of a certain account id
def getTrades(accID):
    trades = (Trade.query.filter_by(accId = accID).all())
    list_of_trades = [trade.serialize() for trade in trades]
    return list_of_trades

#helper method that returns a list of all the transfers associated with a certain account id
def getTransfers(accID):
    #transfers = (Transfer.query.filter_by(acc_id = accID).all())
    #list_of_transfers = [transfer.serialize() for transfer in transfers]
    list_of_incoming = [transfer.serialize() for transfer in Acc.query.get(accID).incoming]
    list_of_outgoing = [transfer.serialize() for transfer in Acc.query.get(accID).outgoing]
    full_list = list_of_incoming + list_of_outgoing
    return full_list