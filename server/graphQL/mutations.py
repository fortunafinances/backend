from ariadne import MutationType
from uuid import uuid4
import sys

from resolverClasses import User, Account, AccountWatch, ReturnAccount, ReturnAccountWatch, ReturnUser

sys.path.insert(1, '../database')
import inserters
from tables import db_lock



mutation = MutationType()

#####################################################
#                   MUTATIONS                       #
#####################################################
@mutation.field("insertUser")
def resolve_insert_user(_, info,
        userId,
        onboardingComplete = None,
        username = None,
        firstName = None,
        lastName = None,
        email = None,
        phoneNumber = None,
        picture = None,
        bankName = None
        ):
    with db_lock:
        message, returned_user = inserters.addUser(userId, username, firstName, lastName, email, phoneNumber, picture, bankName, onboardingComplete)
        new_user = User(returned_user.userId, 
                        returned_user.username, 
                        returned_user.firstName, 
                        returned_user.lastName,
                        returned_user.email,
                        returned_user.phoneNumber,
                        returned_user.picture,
                        returned_user.bankName,
                        returned_user.registerDate,
                        returned_user.onboardingComplete)
        
        return_user = ReturnUser(new_user, message)
        return return_user

@mutation.field("insertAccount")
def resolve_insert_account(_, info, name, userId):
    with db_lock:
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
        tradeQty,
        tradePrice):
    with db_lock:
        message = 'Trade Error in FLask Server resolve_trade_order function'
        if type == "Market":
            if side == "Buy":
                message = inserters.buyMarket(accID, ticker, tradeQty)
            if side == "Sell":
                message = inserters.sellMarket(accID, ticker, tradeQty)
        if type == "Limit":
            if side == "Buy":
                message = inserters.placeBuyLimit(accID, ticker, tradeQty, tradePrice)
            if side == "Sell":
                message = inserters.placeSellLimit(accID, ticker, tradeQty, tradePrice)
        return message

@mutation.field("insertTransfer")
def resolve_transfer_order(_, info,
        sendAccId,
        receiveAccId,
        transferAmt
        ):
    with db_lock:
        message = inserters.doTransfer(sendAccId, 
                            receiveAccId, 
                            transferAmt)
        
        return message

@mutation.field("toggleWatch")
def resolve_toggle_watch(_, info, 
        accId,
        ticker
        ):
    with db_lock:
        accWatch, message = inserters.toggleAccWatch(accId, ticker)
        new_acc_watch = AccountWatch(accWatch.accWatchId, accWatch.accId, accWatch.ticker)
        return_new_acc_watch = ReturnAccountWatch(new_acc_watch, message)

        return return_new_acc_watch
