from flask_sqlalchemy import SQLAlchemy

import random
import sys
sys.path.insert(0, '../database')
from inserters import *
from getters import *
from constants import SP_500


def initUsers():
    addUser("auth0|64c922d8a9c248f78242a230", "claudia27", "Claudia", "Alves", "claudia_alves@email.com", "6177320019", "picture", "Fortuna", 5)
    addUser("AUTHuser2", "tyj", "Tyler", "Jones", "tyjones@email.com", "4017324554", "picture", "Fortuna", 5)
    addUser("AUTHuser3", "jr1", "JR", "Byers", "jr@email.com", "6174357213", "picture", "Fortuna", 5)
    addUser("auth0|64bff46269ace00bf6a23c03", "lindsay.rl", "Lindsay", "Liu", "rll46@duke.edu", "8646247257", "picture", "Fortuna", 5)
    addUser("auth0|64a5a9b2bb372f7bd87fc5e5", "linhvu", "Linh", "Vu", "linh.vu@publicissapient.com", "0000000000", "picture", "Fortuna", 5)
    addUser("auth0|64b7f9420f43178a8a19c036", "nrgbistro", "Nolan", "Gelinas", "nolangelinas@gmail.com", "1610308884", "picture", "Fortuna", 5)

    # Because the users are not being added through graphql,
    # we have to do a double insertiont to update their onboarding values
    addUser("auth0|64c922d8a9c248f78242a230", "claudia27", "Claudia", "Alves", "claudia_alves@email.com", "6177320019", "picture", "Fortuna", 5)
    addUser("AUTHuser2", "tyj", "Tyler", "Jones", "tyjones@email.com", "4017324554", "picture", "Fortuna", 5)
    addUser("AUTHuser3", "jr1", "JR", "Byers", "jr@email.com", "6174357213", "picture", "Fortuna", 5)
    addUser("auth0|64bff46269ace00bf6a23c03", "lindsay.rl", "Lindsay", "Liu", "rll46@duke.edu", "8646247257", "picture", "Fortuna", 5)
    addUser("auth0|64a5a9b2bb372f7bd87fc5e5", "linhvu", "Linh", "Vu", "linh.vu@publicissapient.com", "0000000000", "picture", "Fortuna", 5)
    addUser("auth0|64b7f9420f43178a8a19c036", "nrgbistro", "Nolan", "Gelinas", "nolangelinas@gmail.com", "1610308884", "picture", "Fortuna", 5)

def initAccs():
    addAcc("Brokerage account", "auth0|64c922d8a9c248f78242a230", 25000.00)
    addAcc("Retirement account", "auth0|64c922d8a9c248f78242a230", 5000.00)
    addAcc("College fund account", "auth0|64c922d8a9c248f78242a230", 2600.00)

    addAcc("Brokerage account", "AUTHuser2", 3000.00)
    addAcc("Brokerage account", "AUTHuser3", 7000.00)

    addAcc("College Fund", "auth0|64bff46269ace00bf6a23c03", 100000.00)
    addAcc("Brokerage account", "auth0|64a5a9b2bb372f7bd87fc5e5", 100000.00)
    addAcc("Brokerage account Fund", "auth0|64b7f9420f43178a8a19c036", 100000.00)
    

def initAccsHistory():
    accs = getAccs()

    for acc in accs:
        initAccHistory(acc["accId"])

def initAccHistory(accId):
    sp500Data = StockHistory.query.filter(StockHistory.ticker == SP_500) \
                            .order_by(StockHistory.date.asc()).all()
    acc = Acc.query.get(accId)
    
    for factor, sp500Log in enumerate(sp500Data, 52):
        value = acc.cash + (acc.cash * factor * 0.0005) + (sp500Log.price * random.randint(-5, 10) / 100.0) 
        # print(sp500Log.date, acc.cash, value, sp500Log.price, (value / acc.cash))
        addAccHistory(accId, value, sp500Log.date)

def initAccWatch():
    toggleAccWatch(6, "META")
    toggleAccWatch(6, "JPM")

    toggleAccWatch(7, "DNUT")
    toggleAccWatch(7, "V")
    toggleAccWatch(7, "HD")

    toggleAccWatch(8, "EXC")
    toggleAccWatch(8, "INTU")
    toggleAccWatch(8, "MAR")
    toggleAccWatch(8, "MRK")
    toggleAccWatch(8, "MTB")
    toggleAccWatch(8, "VZ")

def initBuyMarket():
    buyMarket(1, "V", 5)
    buyMarket(1, "JPM", 13)
    buyMarket(1, "JNJ", 8)
    buyMarket(1, "TGT", 17)
    buyMarket(1, "AAPL", 3)
    buyMarket(1, "SOFI", 43)
    buyMarket(1, "UNH", 4)

    buyMarket(2, "MSFT", 2)
    buyMarket(2, "DNUT", 4)
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


