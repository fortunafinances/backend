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

# Returns a list of all of the stocks
def getStocks():
    stocks = (Stock.query.all())
    list_of_stocks = [stock.serialize() for stock in stocks]
    return list_of_stocks

# Returns a list of all of the accs
def getAccs():
    accs = (Acc.query.all())
    return [acc.serialize() for acc in accs]