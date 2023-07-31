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

def getSectorValue(accId, sector):
    sectorSum = 0.0
    sectorStocks = db.session.query(Acc, AccStock, Stock) \
        .join(AccStock, Acc.accId == AccStock.accId) \
        .join(Stock, AccStock.ticker == Stock.ticker) \
        .filter(Acc.accId == accId, Stock.sector == sector)
    
    for sectorStock in sectorStocks:
        sectorSum += sectorStock[1].stockQty * sectorStock[2].currPrice

    return sectorSum

def getPieStats(accId):
    sectors = db.session.query(Stock.sector).distinct()
    stats = dict()
    
    for sector in sectors:
        sectorValue = getSectorValue(accId, sector[0])
        if (sectorValue != 0.0):
            stats[sector[0]] = sectorValue

    return stats, "Success"

def getHoldingsValue(accId):
    acc = (Acc.query.get(accId))
    invest = 0.0

    # For loop to add up all of the investments 
    for accStock in acc.accStocks:
        invest += (Stock.query.get(accStock.ticker)).currPrice * accStock.stockQty
    
    return invest

def getAccTotalValue(accId):
    acc = Acc.query.get(accId)
    
    return (getHoldingsValue(accId) + acc.cash)

def getUserTotalValue(userId):
    accs = User.query.get(userId).accs
    total = 0.0

    for acc in accs:
        total += getAccTotalValue(acc.accId)
    
    return total
    

# Returns an account's monetary values in terms of total assets,
# investments and cash
def getDisplayBar(accId):
    acc = (Acc.query.get(accId))
    
    return {
        "total": getAccTotalValue(accId), 
        "invest": getHoldingsValue(accId), 
        "cash": acc.cash
        }

# Returns a list of stocks that the account owns and the respective
# prices of those stocks
def getHoldings(accId):
    accStocks = AccStock.query.filter(AccStock.accId == accId)
    holdings = list()

    # For loop to retrieve each holding in the accStocks list
    for holding in accStocks:
        stock = Stock.query.get(holding.ticker)
        holdings.append({
            "accStockId": holding.accStockId,
            "ticker": holding.ticker,
            "stockQty": holding.stockQty,
            "currPrice": stock.currPrice
            })
    return holdings

# Returns the contents of a singular stock
def getStock(ticker):
    stock = Stock.query.get(ticker)
    return stock.serialize()
    
def getStockHistory(ticker):
    stockHistory = StockHistory.query.filter(StockHistory.ticker == ticker)
    return [stockLog.serialize() for stockLog in stockHistory]

def getSectorStocks(sector):
    return Stock.query.filter(Stock.sector == sector) 

# Returns a list of all of the stocks
def getStocks():
    stocks = (Stock.query.all())
    list_of_stocks = [stock.serialize() for stock in stocks]
    return list_of_stocks

def getUserAcc(accId):
    return (Acc.query.get(accId)).serialize()

def getUserAccs(userId):
    accs = User.query.get(userId).accs
    return [acc.serialize() for acc in accs]

def getAccHistory(accId):
    try:
        accHistory = Acc.query.get(accId).accHistory
    except AttributeError:  # if the account ID doesn't exist
        return None

    return [accLog.serialize() for accLog in accHistory]

def getAccWatch(accId):
    accWatches = Acc.query.get(accId).accWatch

    return [accWatch.serialize() for accWatch in accWatches]

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

#helper method that returns a list of all limit orders that have not been executed and have not expired
def getLimit():
    openLimitOrders = (Trade.query.filter_by(type = 'Limit', status = 'Placed').all())
    listOfLimitOrders = [trade.serialize() for trade in openLimitOrders]
    return listOfLimitOrders

#helper method that returns a list of all the transfers associated with a certain account id
def getTransfers(accID):
    #transfers = (Transfer.query.filter_by(acc_id = accID).all())
    #list_of_transfers = [transfer.serialize() for transfer in transfers]
    list_of_incoming = [transfer.serialize() for transfer in Acc.query.get(accID).incoming]
    list_of_outgoing = [transfer.serialize() for transfer in Acc.query.get(accID).outgoing]
    full_list = list_of_incoming + list_of_outgoing
    return full_list