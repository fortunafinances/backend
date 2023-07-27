from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

import yfinance as yf
from datetime import datetime, date

# Database file imports
import sys
sys.path.insert(0, '../../database')
import inserters
import getters
from tables import db, Acc, AccHistory, StockHistory

sys.path.insert(0, '../../mockData')
from constants import SP_500, STOCK_LIST

scheduler = APScheduler()

@scheduler.task("cron", id = "SP500", day_of_week = "tue", hour = "10-16", minute = 30)
def updateSP500():
    with scheduler.app.app_context():
        sp500 = yf.Ticker(SP_500)
        sp500Hist = StockHistory.query.filter(StockHistory.ticker == SP_500).all()

        if (len(sp500Hist) == 0):
            sp500Logs = sp500.history(period = "2y", interval = "1mo")
            sp500Logs = sp500Logs[["Close"]]

            for date, close in sp500Logs.iterrows():
                inserters.addStockHistory(SP_500, close["Close"], date.strftime('%Y-%m-%d'))
        else:
            sp500Log = sp500.history(period = "1mo", interval = "1mo")
            date = list(sp500Log.index)[0]
            sp500Log = sp500Log["Close"].values[:1][0]
            if (StockHistory.query.filter(StockHistory.ticker == SP_500,
                                        StockHistory.date == date.strftime('%Y-%m-%d')).first() == None):
                inserters.addStockHistory(SP_500, sp500Log, date.strftime('%Y-%m-%d'))   

@scheduler.task("cron", id = "updateAccHistory",  day_of_week = "tue", hour = "10-16", minute = 30)
def updateAccHistory():
    with scheduler.app.app_context():
        accs = getters.getAccs()

        if (len(AccHistory.query.filter(AccHistory.date == date.today()).all()) == 0):
            for acc in accs:
                inserters.addAccHistory(acc["accId"], getters.getAccTotalValue(acc["accId"]), date.today())

@scheduler.task("cron", id = "updateStockHistory", hour = "10-17")
def updateStockHistory():
    with scheduler.app.app_context():
        for stock in STOCK_LIST.keys():
            yfData = yf.Ticker(stock)
            stockHistory = StockHistory.query.filter(StockHistory.ticker == stock).all()
            
            if(len(stockHistory) == 0):
                yfData = yfData.history(period = "1mo", interval = "1d")
                yfData = yfData[["Close"]]

                for date, close in yfData.iterrows():
                    inserters.addStockHistory(stock, close["Close"], date.strftime('%Y-%m-%d'))
            else:
                yfData = yfData.history(period = "1d", interval = "1d")
                date = list(yfData.index)[0]
                yfData = yfData["Close"].values[:1][0]

                if (StockHistory.query.filter(StockHistory.ticker == stock,
                                            StockHistory.date == date.strftime('%Y-%m-%d')).first() == None):
                    inserters.addStockHistory(stock, yfData, date.strftime('%Y-%m-%d'))

# new algorithm
# literally yoink everything and check if it's in the db, if not, add it. 
# no need to split it into if at least one record exists because what happens if it 
# doesn't run one day