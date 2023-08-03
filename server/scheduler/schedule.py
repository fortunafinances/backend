from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
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
from tables import db, db_lock, AccHistory, StockHistory

sys.path.insert(0, '../../mockData')
from constants import SP_500, STOCK_LIST
from stockConfig import fillStocks

scheduler = APScheduler()
# logging.basicConfig()
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)


@scheduler.task("cron",id = "Check Limit Orders", day_of_week="mon-fri", hour = "9-16", minute = "*/3", second = "30")
def checkLimit():
    with scheduler.app.app_context():
        with db_lock:
            try:
                #checks database against open limit order price
                limitOrders = getLimit()

                for x in limitOrders:
                    limitPrice = x['tradePrice']
                    stock = getStock(x['ticker'])
                    currPrice = stock['currPrice']
                    print(f"These are the open limit orders: Stock {x['ticker']}: Limit Price: {limitPrice}, Current Price: {currPrice} Order Side: {x['side']} Stock Quantity: {x['tradeQty']}")

                    if (currPrice <= limitPrice and x['side'] == 'Buy'):
                        executeLimit(x['tradeId'])
                    elif (currPrice >= limitPrice and x['side'] == 'Sell'):
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
        print("scheduler activated, updating stocks")
        fillStocks()
            #print("stock prices updated successfully")
        print("finished updating stocks")

# The S&P 500 updater that runs every hour from 10:30 - 16:30 on
# Monday for the line graph
@scheduler.task("cron", id = "SP500", hour = "10-16", minute = 30)
def updateSP500():
    with scheduler.app.app_context():
        print("scheduler activated,updating sp500")
        # Retrieve weekly data from the past year
        sp500 = yf.Ticker(SP_500)
        sp500Logs = sp500.history(period = "1y", interval = "1d")
        sp500Logs = sp500Logs[["Close"]]

        # Insert each week that isn't in the database
        for date, close in sp500Logs.iterrows():
            with db_lock:
                if (StockHistory.query.filter(StockHistory.ticker == SP_500,
                    StockHistory.date == date.strftime('%Y-%m-%d')).first() == None):
                    addStockHistory(SP_500, close["Close"], date.strftime('%Y-%m-%d'))   

        print("finished updating sp500")
        
# The account history updater that runs every hour from 10:30 to 16:30 
# on Monday for the line graph
@scheduler.task("cron", id = "updateAccHistory", hour = "10-16", minute = 30)
def updateAccHistory():
    with scheduler.app.app_context():
        print("scheduler activated,updating accHistory")
        accs = getAccs()

        # Loop to update the data for each account if it's not in there
        for acc in accs:
            with db_lock:
                addAccHistory(acc["accId"], getAccTotalValue(acc["accId"]), date.today())

# The stock history updater that runs every hour from 10 to 17 and
# inserts the last 30d of performance for each stock
@scheduler.task("cron", id = "updateStockHistory", hour = "10-17")
def updateStockHistory():
    with scheduler.app.app_context():
        print("scheduler activated,updating stock history")

        # Updates every stock history in STOCK_LIST
        for stock in STOCK_LIST.keys():
            yfData = yf.Ticker(stock) 
            yfData = yfData.history(period = "1mo", interval = "1d")
            yfData = yfData[["Close"]]

            for date, close in yfData.iterrows():
                with db_lock:
                    if (StockHistory.query.filter(StockHistory.ticker == stock,
                            StockHistory.date == date.strftime('%Y-%m-%d')).first() == None):
                        addStockHistory(stock, close["Close"], date.strftime('%Y-%m-%d'))
