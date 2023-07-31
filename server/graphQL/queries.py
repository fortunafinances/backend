from resolverClasses import Account, Order, DisplayBar, Holding, Activity, Stock, PieData, StockHistory, AccountHistory, LinePoint
from ariadne import QueryType
import asyncio
import os
import sys

# not sure why but this import needed this different 
# strucutre type
sys.path.append(os.getcwd() + '/..')
from genAi.queryPSChat import getGPTData

sys.path.insert(0, '../../database')
import getters
from tables import db_lock



query = QueryType()

#####################################################
#                   QUERIES                         #
#####################################################
@query.field("accounts")
def resolve_accounts(_, info, input):    
    userId = input.get("userId")  # gets the userId field from the input type UserIdInput
    accounts = getters.getUserAccs(userId)
    returned_accounts = []
    for account in accounts:
        new_account = Account(
            account["accId"],
            account["name"],
            account["cash"]
        )
        returned_accounts.append(new_account)
    return returned_accounts


@query.field("orders")
def resolve_orders(_, info, input):    
    account_id = input.get("accId")  # gets the accId field from the input type AccIdInput
    db_trades = getters.getTrades(account_id)
    
    returned_orders = []
    for trade in db_trades:

        new_stock = resolve_one_stock(None, None, trade)
        new_order = Order(
            trade["tradeId"],
            account_id,
            trade["type"],
            trade["side"],
            trade["status"],
            trade["tradePrice"],
            trade["tradeQty"],
            trade["tradeDate"],
            new_stock
        )
        returned_orders.append(new_order)

    return returned_orders

# returns a information for the display bar
@query.field("displayBar")
def resolve_holdings(_, info, input):
    account_id = input.get("accId")  # gets the accId field from the input type AccIdInput
    db_display_bar = getters.getDisplayBar(account_id)
    new_display_bar = DisplayBar( 
            db_display_bar["total"],
            db_display_bar["invest"],
            db_display_bar["cash"]
        )
    return new_display_bar

# returns a list of holdings for an account ID to display on the
# holdings table
@query.field("holdings")
def resolve_holdings(_, info, input):    
    account_id = input.get("accId")  # gets the accId field from the input type AccIdInput
    db_holdings = getters.getHoldings(account_id)

    returned_holdings = []
    for holding in db_holdings:

        new_stock = resolve_one_stock(None, None, holding)
        new_holding = Holding( 
            holding["accStockId"],
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
            id=trade["tradeId"],
            accId=trade["accId"],
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

        modified_id = str(transfer["transferId"]) + str(".5")
        new_activity = Activity(
            id=modified_id,
            accId=account_id,
            date=transfer["date"],
            type="Transfer",
            description=new_description,
            amount=transfer_amount
        )
        returned_activities.append(new_activity)

    return returned_activities

@query.field("accountHistorical")
def resolve_account_historical(_, info, input):
    account_id = input.get("accId")  # gets the accId field from the input type AccIdInput
    account_history = getters.getAccHistory(account_id)

    if account_history is None:
        return AccountHistory(None, None, None, "ERROR: Account does not have history in database")

    date_price_data = []
    for item in account_history:
        next_point = LinePoint(item["date"], item["value"])
        date_price_data.append(next_point)

    return_history = AccountHistory(account_history[0]["accHistoryId"],
                                account_history[0]["accId"],
                                date_price_data,
                                "Success")
    
    return return_history

# returns one stock given that stocks ticker
@query.field("oneStock")
def resolve_one_stock(_, info, input):
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

@query.field("stockHistorical")
def resolve_sp500_historical(_, info, input):
    ticker_input = input.get("ticker")
    stock_historical = getters.getStockHistory(ticker_input)
    if len(stock_historical) == 0:
        return StockHistory(None, None, None, "ERROR: Stock does not exist in database")

    date_price_data = []
    for item in stock_historical:
        next_point = LinePoint(item["date"], item["price"])
        date_price_data.append(next_point)

    return_history = StockHistory(stock_historical[0]["stockHistoryId"],
                                stock_historical[0]["ticker"],
                                date_price_data,
                                "Success")
    
    return return_history

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


@query.field("pieData")
def resolve_pieData(_, info, input):    
    account_id = input.get("accId")  # gets the accId field from the input type AccIdInput
    db_pie_data, message = getters.getPieStats(account_id)
    return_pie = PieData(db_pie_data, message)
    return return_pie

@query.field("allAccValue")
def resolve_all_account_value(_, info, input):
    userId = input.get("userId")  # gets the userId field from the input type UserIdInput
    accounts = getters.getUserAccs(userId)

    total = 0
    for account in accounts:
        account_info = getters.getDisplayBar(account.get('accId'))
        total += account_info.get('total')
    return total


@query.field("genAIQuery")
def resolve_genAI_Query(_, info, input):
    result = getGPTData(input)
    return result
