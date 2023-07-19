from flask_sqlalchemy import SQLAlchemy

import sys
sys.path.insert(0, '../database')
from inserters import *
from getters import *

# WILL BE REVAMPED AFTER AUTHENTICATION IMPLEMENTATION
def initUsers():
    addUser("user1", "user1@email.com", "2002-11-29")
    addUser("user2", "user2@email.com", "1998-01-03")
    addUser("user3", "user3@email.com", "2000-04-17")

def initAccs():
    addAcc("user1's brokerage account", 1, 10000.00)
    addAcc("user1's retirement account", 1, 5000.00)
    addAcc("user1's college fund account", 1, 2600.00)

    addAcc("user2's brokerage account", 2, 1000.00)
    addAcc("user3's brokerage account", 3, 1000.00)

def initBuyMarket():
    buyMarket(1, "TSLA", 5)
    buyMarket(1, "SOFI", 13)
    buyMarket(1, "TSLA", 5)




# def initTrades():
