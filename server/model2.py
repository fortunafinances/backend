from ariadne import QueryType, MutationType
from uuid import uuid4   

query = QueryType()
mutation = MutationType()


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