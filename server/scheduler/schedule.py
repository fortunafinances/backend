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
from constants import SP_500

scheduler = APScheduler()

def updateSP500():
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
        # print(date.strftime('%Y-%m-%d'))
        # print(StockHistory.query.filter(StockHistory.ticker == SP_500))
        # print(date, sp500Log)
        if (StockHistory.query.filter(StockHistory.ticker == SP_500,
                                     StockHistory.date == date.strftime('%Y-%m-%d')).first() == None):
            inserters.addStockHistory(SP_500, sp500Log, date.strftime('%Y-%m-%d'))   

def updateAccHistory():
    accs = getters.getAccs()

    if (len(AccHistory.query.filter(AccHistory.date == date.today()).all()) == 0):
        for acc in accs:
            inserters.addAccHistory(acc["accId"], getters.getAccTotalValue(acc["accId"]), date.today())
        
def runHistoryUpdates():        
    with scheduler.app.app_context():
        updateSP500()
        updateAccHistory()
        # print("this works")
        # inserters.addAcc("test",1,4.20)

def schedule_jobs():
    scheduler.add_job(id = "test", func=runHistoryUpdates, trigger="interval", seconds = 10)


# sp500Hist = list(sp500Hist["Close"])

# formatted_dates = [date.strftime("%Y-%m-%d") for date in dates]
# print(sp500Hist)

# data_dict = dict()

    # date = date.strftime('%Y-%m-%d')
    # close = close['Close']
    # data_dict[date] = close

