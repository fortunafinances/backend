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

    #print('add trade resolver execution', file=sys.stdout)
    # add the trade to the database
    #inserters.testTrade()

    inserters.addTrade(accID, type, side, status, date, ticker, tradePrice, tradeQty)

    # need to send modification to update number of account stock
    
    
    return "Trade Inserted"


#####################################################
#                   QUERIES                         #
#####################################################

@query.field("trades")
def resolve_orders(_, info):
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

