import sys

sys.path.insert(0, '../mockData')
from stockConfig import fillStocks

#calls api and updates database prices
fillStocks()


