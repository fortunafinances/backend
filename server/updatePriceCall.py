import os

import sys
sys.path.insert(0, '../mockData')
from stockConfig import fillStocks

import logging

logging.basicConfig(filename="tasks.log", level=logging.INFO, format = '%(asctime)s %(levelname)s %(name)s %(message)s')

logger = logging.getLogger(__name__)

#calls api and updates database prices
fillStocks()
logging.info('this file is being executed')


