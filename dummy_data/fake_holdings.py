class Holding:
    def __init__(self, account_id, ticker, name, quantity, price):
        self.account_id = account_id
        self.ticker = ticker
        self.name = name
        self.quantity = quantity
        self.price = price

holding1 = Holding('123', 'TSLA', 'Tesla', 300, 26976)
holding2 = Holding('123', 'APPL', 'Apple', 20, 1311)
holding3 = Holding('123', 'AMZN', 'Amazon', 2, 301245)
holding4 = Holding('123', 'FORT', 'Fortuna', 521, 4523)

holding_list = [holding1, holding2, holding3, holding4]
