from ariadne import QueryType, MutationType
from uuid import uuid4   

import sys
sys.path.insert(1, '../dummy_data') 
import fake_holdings

query = QueryType()
mutation = MutationType()


@mutation.field("orderCoffee")
def resolve_order_coffee(_, info, size, name, type):
    newOrder = Coffee(size, name, type)
    coffeeOrders.append(newOrder)

    # message to database
    return newOrder


class Coffee:
   def __init__(self, size, name, coffee_type):
       self.size = size
       self.name = name
       self.type = coffee_type
       self.id = uuid4()    # universally unique identifier

coffeeOrders = []

@query.field("coffeeOrders")
def resolve_orders(_, info):
    return orders

#############################################################
#############################################################
#############################################################

@mutation.field("mutateOrder")
def resolve_order_coffee(_, info,
        order_id, user_id, type, side,
        purchaseDate,
        stock_id,
        status,
        purchasePrice,
        quantity):
    newOrder = Order(order_id, user_id, type, side,
                     purchaseDate, stock_id, status,
                     purchasePrice, quantity)
    orders.append(newOrder)
    return newOrder

# Possible Buzz class
# class Orderr(db.Model):
#    order_id = db.Column(db.String, nullable = False)


class Order:
    def __init__(self, order_id,
        user_id, type, side,
        purchaseDate,
        stock_id, status, purchasePrice,
        quantity):
        self.order_id = order_id
        self.user_id = user_id
        self.type = type
        self.side = side
        self.purchaseDate = purchaseDate
        self.stock_id = stock_id
        self.status = status
        self.purchasePrice = purchasePrice
        self.quantity = quantity


orders = []

@query.field("orders")
def resolve_orders(_, info):
    return orders


@query.field("holdings")
def resolve_holdings(_, info):
    return fake_holdings.holding_list