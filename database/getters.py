import json
from flask import jsonify
from tables import *

# Tester function to test a query and relations 
def testRelations():
    # returns the array of orders of the acc w/ id 1
    trades = Acc.query.get(1).orders
    # gets the tradePrice of the 0th trade in the orders array
    print(trades[0].tradePrice)

# Returns a list of all of the stocks
def getStocks():
    stocks = (Stock.query.all())
    return (jsonify([stock.serialize() for stock in stocks]))

# Returns a list of all of the accs
def getAccs():
    accs = (Acc.query.all())
    return (jsonify([acc.serialize() for acc in accs]))