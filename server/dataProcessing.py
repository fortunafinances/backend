import json


class Price:
    def __init__(self, ticker, curr_price, high_price, low_price, opening_price, previous_closing_price, price_change):
        self.ticker = ticker
        self.curr_price = curr_price
        self.high_price = high_price
        self.low_price = low_price
        self.opening_price = opening_price
        self.previous_closing_price = previous_closing_price
        self.price_change = price_change

    def to_dict(self):
        return {
            'ticker': self.ticker,
            'curr_price': self.curr_price,
            'high_price': self.high_price,
            'low_price': self.low_price,
            'opening_price': self.opening_price,
            'previous_closing_price': self.previous_closing_price,
            'price_changed': self.price_change,
        }


def handle_quote_data(data, symbol):
    ticker = symbol
    curr_price = round(data["c"] * 100)
    high_price = round(data["h"] * 100)
    low_price = round(data["l"] * 100)
    opening_price = round(data["o"] * 100)
    previous_close_price = round(data["pc"] * 100)
    price_change = round(data["d"] * 100)

    price = Price(ticker, curr_price, high_price, low_price, opening_price, previous_close_price, price_change)

    return price

def handle_stock_list(data):
    parsed_list = json.load(data)
    new_list = []
    ticker = [item['symbol'] for item in parsed_list]
    return ticker

