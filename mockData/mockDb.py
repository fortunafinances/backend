from flask_sqlalchemy import SQLAlchemy

import sys
sys.path.insert(0, '../database')
from inserters import *
from getters import *


def initUsers():
    addUser("AUTHuser1", "username1", "usr1nickname", "user1@email.com", "picture", "03212000", True)
    addUser("AUTHuser2", "username2", "usr2nickname", "user2@email.com", "picture", "01301995", True)
    addUser("AUTHuser3", "username3", "usr3nickname", "user3@email.com", "picture", "12012001", True)

    # This needs to be done twice because the first time a user is added their onboarding is set to false
    addUser("AUTHuser1", "username1", "usr1nickname", "user1@email.com", "picture", "03212000", True)
    addUser("AUTHuser2", "username2", "usr2nickname", "user2@email.com", "picture", "01301995", True)
    addUser("AUTHuser3", "username3", "usr3nickname", "user3@email.com", "picture", "12012001", True)

def initAccs():
    addAcc("user1's brokerage account", "AUTHuser1", 10000.00)
    addAcc("user1's retirement account", "AUTHuser1", 5000.00)
    addAcc("user1's college fund account", "AUTHuser1", 2600.00)

    addAcc("user2's brokerage account", "AUTHuser2", 3000.00)
    addAcc("user3's brokerage account", "AUTHuser3", 7000.00)

def initBuyMarket():
    stocks = getStocks()
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





# def initTrades():
