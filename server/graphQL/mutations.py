from ariadne import MutationType
from uuid import uuid4
import sys

from resolverClasses import User, Account, ReturnAccount

sys.path.insert(1, '../database')
import inserters



mutation = MutationType()

#####################################################
#                   MUTATIONS                       #
#####################################################
@mutation.field("insertUser")
def resolve_insert_user(_, info,
        userId,
        onboardingComplete = None,
        username = None,
        nickname = None,
        email = None,
        picture = None,
        dateOfBirth = None
        ):
    message, userAlreadyExisted, returned_user = inserters.addUser(userId, username, nickname, email, picture, dateOfBirth, onboardingComplete)
    new_user = User(returned_user.userId, 
                    returned_user.username, 
                    returned_user.nickname, 
                    returned_user.email,
                    returned_user.picture,
                    returned_user.dateOfBirth,
                    message, 
                    userAlreadyExisted, 
                    returned_user.onboardingComplete)
    return new_user

@mutation.field("insertAccount")
def resolve_insert_account(_, info, name, userId):
    db_acc, message = inserters.addAcc(name, userId, 0)
    new_account = Account(db_acc.accId, db_acc.name, db_acc.cash) 
    return_account = ReturnAccount(new_account, message)
    return return_account


# This resolver is for when the frontend executes a BUY
# or SELL trade 
@mutation.field("insertTrade")
def resolve_trade_order(_, info,
        accID,
        type,
        side,
        ticker,
        tradeQty):
    message = 'Trade Error in FLask Server resolve_trade_order function'
    if type == "Market":
        if side == "Buy":
            message = inserters.buyMarket(accID, ticker, tradeQty)
        if side == "Sell":
            message = inserters.sellMarket(accID, ticker, tradeQty)
    if type == "Limit":
        status = "Placed"
        date = "notrealdateforlimit"
        tradePrice = "45"
        inserters.addTrade(accID, type, side, status, date, ticker, tradePrice, tradeQty)
        message = "Limit functionality has not been fully implemented"
    return message

@mutation.field("insertTransfer")
def resolve_transfer_order(_, info,
        sendAccId,
        receiveAccId,
        transferAmt
        ):
    
    message = inserters.doTransfer(sendAccId, 
                          receiveAccId, 
                          transferAmt)
    
    return message


