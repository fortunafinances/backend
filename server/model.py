from ariadne import QueryType, MutationType
from uuid import uuid4   

query = QueryType()
mutation = MutationType()



@mutation.field("orderCoffee")
def resolve_order_coffee(_, info, size, name, type):
    newOrder = Coffee(size, name, type)
    orders.append(newOrder)

    
    # message to database
    return newOrder


class Coffee:
   def __init__(self, size, name, coffee_type):
       self.size = size
       self.name = name
       self.type = coffee_type
       self.id = uuid4()    # universally unique identifier


orders = []

@query.field("orders")
def resolve_orders(_, info):
    return orders