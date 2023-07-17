from ariadne import QueryType, MutationType
from uuid import uuid4
import json 
import sys
sys.path.insert(1, '../dummy_data') 
import fake_holdings

sys.path.insert(1, '../database')
import inserters
import getters


query = QueryType()
mutation = MutationType()

#####################################################
#                   CLASSES                         #
#####################################################

class Stock:
    def __init__(self, 
                ticker,
                currPrice,
                highPrice,
                lowPrice,
                openPrice,
                prevClosePrice):
       self.ticker = ticker
       self.currPrice = currPrice
       self.highPrice = highPrice
       self.lowPrice = lowPrice
       self.openPrice = openPrice
       self.prevClosePrice = prevClosePrice

       
class Trade:
    def __init__(self, 
                accID,
                type,
                side,
                status,
                date,
                ticker,
                tradePrice,
                tradeQty):
       self.accID = accID
       self.type = type
       self.side = side
       self.status = status
       self.date = date
       self.ticker = ticker
       self.tradePrice = tradePrice
       self.tradeQty = tradeQty


#####################################################
#                   MUTATIONS                       #
#####################################################

# This resolver is for when the frontend executes a BUY
# or SELL trade 
@mutation.field("insertTrade")
def resolve_trade_order(_, info,
        accID,
        type,
        side,
        status,
        date,
        ticker,
        tradePrice,
        tradeQty):

    inserters.addTrade(accID,
                        type,
                        side,
                        status,
                        date, 
                        ticker, 
                        tradePrice, 
                        tradeQty)
    # need to send modification to update number of account stock
    
    return "Trade Inserted"

@mutation.field("insertTransfer")
def resolve_trade_order(_, info,
        sendAccId,
        receiveAccId,
        transferAmt,
        date
        ):
    
    inserters.addTransfer(sendAccId, 
                          receiveAccId, 
                          transferAmt, 
                          date)
    
    return "Transfer Inserted"


#####################################################
#                   QUERIES                         #
#####################################################

@query.field("trades")
def resolve_orders(_, info):
    # query database to get list of trades
    return orders


@query.field("holdings")
def resolve_holdings(_, info):
    return fake_holdings.holding_list

@query.field("stocks")
def resolve_stocks(_, info):
    list_of_stocks = getters.getStocks()

    returned_stocks = []
    for stock in list_of_stocks:
        new_stock = Stock( 
                stock["ticker"],
                stock["currPrice"],
                stock["highPrice"],
                stock["lowPrice"],
                stock["openPrice"],
                stock["prevClosePrice"])
        returned_stocks.append(new_stock)
    
    return returned_stocks

