import sys
sys.path.insert(0, '../database')
from getters import getLimit, getStock
from inserters import executeLimit

def checkLimit():
    try:
        #checks database against open limit order price
        limitOrders = getLimit()
        print ("checking open limit orders")

        for x in limitOrders:
            limitPrice = x.tradePrice
            stock = getStock(x.ticker)

            if (limitPrice <= stock.currPrice):
                executeLimit(x.tradeId)
    except Exception as e:
        print(f'Eception in checkLimit: {e}')

