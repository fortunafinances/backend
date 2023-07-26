import pytz
from datetime import datetime, time
import flask_apscheduler 
import APScheduler

import sys
sys.path.insert(0, '../database')
from getters import getLimit, getStock
from inserters import executeLimit
from tables import db

sys.path.insert(0, '../mockData')
from stockConfig import fillStocks

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

def limitExpired():
    with scheduler.app_context()
    #changes status of expired limit orders from placed to expired
    today = datetime.now(tz=pytz.timezone("US/Eastern")).date()
    time_obj = time(9,30, tzinfo=pytz.timezone("US/Eastern"))
    trade_cutoff = datetime.combine(today, time_obj)

    limitList = getLimit()

    for trade in limitList:
        if (trade.date < trade_cutoff):
            trade.status = "Expired"
            db.session.commit()

def updateStockPrice():
    fillStocks()