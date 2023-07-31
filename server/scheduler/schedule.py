from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from apscheduler.triggers.cron import CronTrigger
from threading import Lock
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
from constants import SP_500, STOCK_LIST
from stockConfig import fillStocks

scheduler = APScheduler()
db_lock = Lock()
# logging.basicConfig()
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)


@scheduler.task("cron",id = "Check Limit Orders", day_of_week="mon-fri", hour = "9-16", minute = "*/3")
def checkLimit():
    with scheduler.app.app_context():
        with db_lock:
            try:
                #checks database against open limit order price
                limitOrders = getLimit()
                print(f"These are the current limit orders: {limitOrders}")

                for x in limitOrders:
                    limitPrice = x['tradePrice']
                    stock = getStock(x['ticker'])
                    currPrice = stock['currPrice']
                    print(f"This is the limit & current price for {x['ticker']}: {limitPrice}, {currPrice}")

                    if (currPrice <= limitPrice):
                        executeLimit(x['tradeId'])
            except Exception as e:
                print(f'Exception in checkLimit: {e}')

@scheduler.task("cron",id = "Limit Purge", day_of_week="mon-fri", hour = "16", minute = "0")
def limitExpired():
    with scheduler.app.app_context():
        with db_lock:
            #changes status of expired limit orders from placed to expired
            today = datetime.now(tz=pytz.timezone("US/Eastern")).date()
            time_obj = time(9,30, tzinfo=pytz.timezone("US/Eastern"))
            trade_cutoff = datetime.combine(today, time_obj)

            limitList = getLimit()

            for trade in limitList:
                if (trade.date < trade_cutoff):
                    trade.status = "Expired"
                    db.session.commit()

@scheduler.task("cron",id = "Stock Price Updates", day_of_week="mon-fri", hour = "9-16", minute = "*/3")
def updateStockPrice():
    with scheduler.app.app_context():
        with db_lock:
            fillStocks()

@scheduler.task("cron", id = "SP500", day_of_week = "tue", hour = "10-16", minute = 30)
def updateSP500():
    with scheduler.app.app_context():
        sp500 = yf.Ticker(SP_500)
        sp500Logs = sp500.history(period = "1y", interval = "1wk")
        sp500Logs = sp500Logs[["Close"]]

        for date, close in sp500Logs.iterrows():
            if (StockHistory.query.filter(StockHistory.ticker == SP_500,
                StockHistory.date == date.strftime('%Y-%m-%d')).first() == None):
                addStockHistory(SP_500, close["Close"], date.strftime('%Y-%m-%d'))   

@scheduler.task("cron", id = "updateAccHistory",  day_of_week = "tue", hour = "10-16", minute = 30)
def updateAccHistory():
    with scheduler.app.app_context():
        accs = getAccs()

        if (len(AccHistory.query.filter(AccHistory.date == date.today()).all()) == 0):
            for acc in accs:
                addAccHistory(acc["accId"], getAccTotalValue(acc["accId"]), date.today())

@scheduler.task("cron", id = "updateStockHistory", hour = "10-17")
def updateStockHistory():
    with scheduler.app.app_context():
        # print("scheduler activated,updating stocks")
        for stock in STOCK_LIST.keys():
            yfData = yf.Ticker(stock) 
            yfData = yfData.history(period = "1mo", interval = "1d")
            yfData = yfData[["Close"]]

            for date, close in yfData.iterrows():
                if (StockHistory.query.filter(StockHistory.ticker == stock,
                        StockHistory.date == date.strftime('%Y-%m-%d')).first() == None):
                    addStockHistory(stock, close["Close"], date.strftime('%Y-%m-%d'))
