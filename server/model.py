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
        
class Activity:
    def __init__(self, accountId, date, type, description, amount):
        self.accountId = accountId
        self.date = date
        self.type = type
        self.description = description
        self.amount = amount

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

# returns a list of holdings for an account ID to display on the
# holdings table
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

    return returned_holdings

# returns a list of activities for an account ID to display on the
# activity table
@query.field("activity")
def resolve_activity(_, info, input):
    account_id = input.get("accId")  # gets the accId field from the input type AccIdInput

    returned_activities = []

    trades_list = getters.getTrades(account_id)
    for trade in trades_list:
        new_amount = trade['tradePrice'] * trade['tradeQty']
        new_description = ''
        if trade['side'] == 'Buy':
            new_amount *= -1   # buy is a subtraction from account total
            new_description = 'Bought ' + str(trade['tradeQty']) + ' shares of ' + \
                                str(trade['ticker']) + ' @ ' + str(trade['tradePrice'])
        else:
            new_description ='Sold ' + str(trade['tradeQty']) + ' shares of ' + \
                                str(trade['ticker']) + ' @ ' + str(trade['tradePrice'])
        new_activity = Activity(
            accountId=trade["accId"],
            date=trade["tradeDate"],
            type="Trade",
            description=new_description,
            amount= new_amount
        )
        returned_activities.append(new_activity)

    transfer_list = getters.getTransfers(account_id)
    for transfer in transfer_list:
        transfer_amount = transfer['transferAmt']
        new_description = 'Transfer in'
        if transfer['sendAccId'] == account_id:
            transfer_amount *= -1
            new_description = 'Transfer out'

        new_activity = Activity(
            accountId=account_id,
            date=transfer["date"],
            type="Transfer",
            description=new_description,
            amount=transfer_amount
        )
        returned_activities.append(new_activity)

    return returned_activities


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

