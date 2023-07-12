class Holding:
    def __init__(self, accountId, accStockId, ticker, name, stockQuantity, price):
        self.accountId = accountId
        self.accStockId = accStockId
        self.ticker = ticker
        self.name = name
        self.stockQuantity = stockQuantity
        self.price = price

holding1 = Holding('123', '32', 'TSLA', 'Tesla', 300, 26976)
holding2 = Holding('123', '72', 'APPL', 'Apple', 20, 1311)
holding3 = Holding('123', '5', 'AMZN', 'Amazon', 2, 301245)
holding4 = Holding('123', '2', 'FORT', 'Fortuna', 521, 4523)

holding_list = [holding1, holding2, holding3, holding4]
