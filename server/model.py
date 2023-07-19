from ariadne import QueryType, MutationType
from uuid import uuid4
import json 
import sys
sys.path.insert(1, '../mockData') 
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
                name,
                currPrice,
                highPrice,
                lowPrice,
                openPrice,
                prevClosePrice,
                description,
                sector,
                country,
                website,
                officerTitle,
                officerName):
       self.ticker = ticker
       self.name = name
       self.currPrice = currPrice
       self.highPrice = highPrice
       self.lowPrice = lowPrice
       self.openPrice = openPrice
       self.prevClosePrice = prevClosePrice
       self.description = description
       self.sector = sector
       self.country = country
       self.website = website
       self.officerTitle = officerTitle
       self.officerName = officerName

       
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
    def __init__(self, accountId, stockQuantity, stock):
        self.accountId = accountId
        self.stockQuantity = stockQuantity
        self.stock = stock
        
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
        ticker,
        tradePrice,
        tradeQty):
    date = 'dateshouldnotbeinserted'
    message = 'Trade Error in FLask Server resolve_trade_order function'
    if type == "Market":
        if side == "Buy":
            message = inserters.buyMarket(accID, ticker, tradeQty, date)
        if side == "Sell":
            message = inserters.sellMarket(accID, ticker, tradeQty, date)
    if type == "Limit":
        inserters.addTrade(accID, type, side, status, date, ticker, tradePrice, tradeQty)
        message = "Limit functionality has not been fully implemented"
    return message

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

        new_stock = resolve_one_stock(None, holding)
        new_holding = Holding( 
            account_id,
            holding["stockQty"],
            new_stock
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

# returns a list of activities for an account ID to display on the
# activity table
@query.field("oneStock")
def resolve_one_stock(_, input):
    ticker_input = input.get("ticker")  # gets the ticker field from the input type TickerInput

    stock = getters.getStock(ticker_input) # buzz method
    returned_stock = Stock(
                stock["ticker"],
                stock["companyName"],
                stock["currPrice"],
                stock["highPrice"],
                stock["lowPrice"],
                stock["openPrice"],
                stock["prevClosePrice"],
                stock["businessDescription"],
                stock["sector"],
                stock["country"],
                stock["website"],
                stock["officerTitle"],
                stock["officerName"]
    )
    return returned_stock


@query.field("stocks")
def resolve_stocks(_, info):
    list_of_stocks = getters.getStocks()

    returned_stocks = []
    for stock in list_of_stocks:
        new_stock = Stock( 
                stock["ticker"],
                stock["companyName"],
                stock["currPrice"],
                stock["highPrice"],
                stock["lowPrice"],
                stock["openPrice"],
                stock["prevClosePrice"],
                stock["businessDescription"],
                stock["sector"],
                stock["country"],
                stock["website"],
                stock["officerTitle"],
                stock["officerName"])
        returned_stocks.append(new_stock)
    
    return returned_stocks

