import pytz
from datetime import datetime, time
import sys
sys.path.insert(0, '../database')
from getters import getLimit
from tables import db

#changes status of expired limit orders from placed to expired
today = datetime.now(tz=pytz.timezone("US/Eastern")).date()
time_obj = time(9,30, tzinfo=pytz.timezone("US/Eastern"))
trade_cutoff = datetime.combine(today, time_obj)

limitList = getLimit()

for trade in limitList:
    if (trade.date < trade_cutoff):
        trade.status = "Expired"
        db.session.commit()



