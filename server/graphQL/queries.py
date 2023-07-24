from resolverClasses import Account, Order, DisplayBar, Holding, Activity, Stock
from ariadne import QueryType

import sys 
sys.path.insert(1, '../../database')
import getters

query = QueryType()

#####################################################
#                   QUERIES                         #
#####################################################
@query.field("accounts")
def resolve_accounts(_, info, input):
    userId = input.get("userId")  # gets the accId field from the input type AccIdInput
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