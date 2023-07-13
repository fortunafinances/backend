from ariadne import QueryType, MutationType
from uuid import uuid4   
import sys
sys.path.insert(1, '../dummy_data') 
import fake_holdings

sys.path.insert(1, '../database')
from inserters import testTrade


query = QueryType()
mutation = MutationType()

class Stock:
    def __init__(self, size, name, coffee_type):
       self.size = size
       self.name = name
       self.type = coffee_type
       self.id = uuid4()    # universally unique identifier


#####################################################
#                   MUTATIONS                       #
#####################################################

# This resolver is for when the frontend executes a BUY
# or SELL trade 
@mutation.field("insertTrade")
def resolve_trade_order(_, info,
        tradeID,
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
    testTrade()
    
    
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
    stock_list = []
    return stock_list

