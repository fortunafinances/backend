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

class Holding:
    def __init__(self, accountId, ticker, name, stockQuantity, price):
        self.accountId = accountId
        self.ticker = ticker
        self.name = name
        self.stockQuantity = stockQuantity
        self.price = price


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
def resolve_holdings(_, info, input):

    account_id = input.get("accId")  # gets the accId field from the input type AccIdInput
    db_holdings = getters.getHoldings(account_id)

    returned_holdings = []
    for holding in db_holdings:
        new_holding = Holding( 
            account_id,
            holding["ticker"],
            "no name yet",
            holding["stockQty"],
            holding["currPrice"]
        )
        returned_holdings.append(new_holding)

    #holding1 = Holding('123', '32', 'TSLA', 'Tesla', 300, 26976)
    #holding2 = Holding('123', '72', 'APPL', 'Apple', 20, 1311)
    #holding3 = Holding('123', '5', 'AMZN', 'Amazon', 2, 301245)
    #holding4 = Holding('123', '2', 'FORT', 'Fortuna', 521, 4523)

    # acc id 44 exists in the database

    #holding_list = [holding1, holding2, holding3, holding4]
    return returned_holdings



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

