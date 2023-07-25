import sys
sys.path.insert(0, '../database')
from getters import getLimit, getStock
from inserters import executeLimit

#checks database against open limit order price
limitOrders = getLimit()

for x in limitOrders:
    limitPrice = x.tradePrice
    stock = getStock(x.ticker)

    if (limitPrice <= stock.currPrice):
        executeLimit(x.tradeId)

