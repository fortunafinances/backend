from flask_sqlalchemy import SQLAlchemy

import random
import sys
sys.path.insert(0, '../database')
from inserters import *
from getters import *
from constants import SP_500


def initUsers():
    addUser("AUTHuser1", "tyj", "Tyler", "Jones", "tyjones@email.com", "4017324554", "picture", "Fortuna", True)
    addUser("AUTHuser2", "jr1", "JR", "Byers", "jr@email.com", "6174357213", "picture", "Fortuna", True)
    addUser("AUTHuser3", "claudia27", "Claudia", "Alves", "claudia_alves@email.com", "6177320019", "picture", "Fortuna", True)

    # This needs to be done twice because the first time a user is added their onboarding is set to false
    addUser("AUTHuser1", "tyj", "Tyler", "Jones", "tyjones@email.com", "4017324554", "picture", "Fortuna", True)
    addUser("AUTHuser2", "jr1", "JR", "Byers", "jr@email.com", "6174357213", "picture", "Fortuna", True)
    addUser("AUTHuser3", "claudia27", "Claudia", "Alves", "claudia_alves@email.com", "6177320019", "picture", "Fortuna", True)

def initAccs():
    addAcc("Brokerage account", "AUTHuser1", 10000.00)
    addAcc("Retirement account", "AUTHuser1", 5000.00)
    addAcc("College fund account", "AUTHuser1", 2600.00)

    addAcc("Brokerage account", "AUTHuser2", 3000.00)
    addAcc("Brokerage account", "AUTHuser3", 7000.00)

def initAccsHistory():
    accs = getAccs()

    for acc in accs:
        initAccHistory(acc["accId"])

def initAccHistory(accId):
    sp500Data = StockHistory.query.filter(StockHistory.ticker == SP_500) \
                            .order_by(StockHistory.date.desc()).all()[:52]
    sp500Data = sp500Data[::-1]
    acc = Acc.query.get(accId)
    
    for factor, sp500Log in enumerate(sp500Data, 52):
        value = acc.cash + (acc.cash * factor * 0.0005) + (sp500Log.price * random.randint(-5, 10) / 100.0) 
        print(sp500Log.date, acc.cash, value, sp500Log.price, (value / acc.cash))
        addAccHistory(accId, value, sp500Log.date)

def initBuyMarket():
    buyMarket(1, "V", 5)
    buyMarket(1, "JPM", 13)
    buyMarket(1, "META", 5)

    buyMarket(2, "MSFT", 2)
    buyMarket(3, "BAC", 9)
    
    buyMarket(4, "HD", 3)
    buyMarket(5, "MA", 5)

def initSellMarket():
    sellMarket(1, "V", 5)
    sellMarket(1, "JPM", 7)

    sellMarket(4, "HD", 3)
    sellMarket(5, "MA", 3)

def initTransferIn():
    doTransfer(0, 1, 1000.00)
    doTransfer(0, 3, 300.00)

def initTransferOut():
    doTransfer(1, 0, 4000.83)
    doTransfer(5, 0, 143.47)

def initTransferBetween():
    doTransfer(1, 2, 384.32)
    doTransfer(3, 1, 643.87)


