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

# Returns a list of all of the stocks
def getStocks():
    stocks = (Stock.query.all())
    list_of_stocks = [stock.serialize() for stock in stocks]
    return list_of_stocks

# Returns a list of all of the accs
def getAccs():
    accs = (Acc.query.all())
    return [acc.serialize() for acc in accs]

#Returns a list of transfers and trades associated with a certain acc_id
def getActivity(accID):
    trades = getTrades(accID)
    transfers = getTransfers(accID)
    activity = trades + transfers
    return activity

#helper method that returns a list of all trades of a certain account id
def getTrades(accID):
    trades = (Trade.query.filter_by(acc_id = accID).all())
    list_of_trades = [trade.serialize() for trade in trades]
    return list_of_trades

#helper method that returns a list of all the transfers associated with a certain account id
def getTransfers(accID):
    transfers = (Transfer.query.filter_by(acc_id = accID).all())
    list_of_transfers = [transfer.serialize() for transfer in transfers]
    return list_of_transfers