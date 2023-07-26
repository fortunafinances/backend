from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

import yfinance as yf
from datetime import datetime, date
import time
import logging

# Database file imports
import sys
sys.path.insert(0, '../../database')
from inserters import executeLimit, addStockHistory, addAccHistory
from getters import getLimit, getStock, getAccs, getAccTotalValue
from tables import db, AccHistory, StockHistory

sys.path.insert(0, '../../mockData')
from constants import SP_500
from stockConfig import fillStocks

scheduler = APScheduler()
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

# while True:
#     time.sleep(10)

def checkLimit():
    with scheduler.app.app_context():
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
    with scheduler.app.app_context():
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
    with scheduler.app.app_context():
        fillStocks()

def updateSP500():
    sp500 = yf.Ticker(SP_500)
    sp500Hist = StockHistory.query.filter(StockHistory.ticker == SP_500).all()

    if (len(sp500Hist) == 0):
        sp500Logs = sp500.history(period = "2y", interval = "1mo")
        sp500Logs = sp500Logs[["Close"]]

        for date, close in sp500Logs.iterrows():
            addStockHistory(SP_500, close["Close"], date.strftime('%Y-%m-%d'))
    else:
        sp500Log = sp500.history(period = "1mo", interval = "1mo")
        date = list(sp500Log.index)[0]
        sp500Log = sp500Log["Close"].values[:1][0]
        # print(date.strftime('%Y-%m-%d'))
        # print(StockHistory.query.filter(StockHistory.ticker == SP_500))
        # print(date, sp500Log)
        if (StockHistory.query.filter(StockHistory.ticker == SP_500,
                                     StockHistory.date == date.strftime('%Y-%m-%d')).first() == None):
            addStockHistory(SP_500, sp500Log, date.strftime('%Y-%m-%d'))   

def updateAccHistory():
    accs = getAccs()

    if (len(AccHistory.query.filter(AccHistory.date == date.today()).all()) == 0):
        for acc in accs:
            addAccHistory(acc["accId"], getAccTotalValue(acc["accId"]), date.today())
        
def runHistoryUpdates():        
    with scheduler.app.app_context():
        updateSP500()
        updateAccHistory()
        # print("this works")
        # inserters.addAcc("test",1,4.20)

stockMarketHours = CronTrigger(day_of_week='mon-fri', hour='9-16',minute='*/1', second='30')
endOfDay = CronTrigger(day_of_week='mon-fri', hour='16')

def schedule_jobs():
    # scheduler.add_job(id = "test", func=runHistoryUpdates, trigger="interval", seconds = 10)
    scheduler.add_job(id = "Stock Price Updates", 
                      func=updateStockPrice, 
                      trigger= stockMarketHours)
    scheduler.add_job(id = "Checks Limit Orders", 
                      func=checkLimit, 
                      trigger=stockMarketHours)
    scheduler.add_job(id = "Delete Expired Limit Orders",
                      func = limitExpired,
                      trigger = endOfDay)
    


# sp500Hist = list(sp500Hist["Close"])

# formatted_dates = [date.strftime("%Y-%m-%d") for date in dates]
# print(sp500Hist)

# data_dict = dict()

    # date = date.strftime('%Y-%m-%d')
    # close = close['Close']
    # data_dict[date] = close

