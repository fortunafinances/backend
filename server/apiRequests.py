from flask import jsonify
import json
import requests

def get_stock_quote(symbol):
    url= "https://finnhub.io/api/v1/quote"
    token = "cimn4r1r01qhp3kcngjgcimn4r1r01qhp3kcngk0"
    params = {'symbol': symbol, 'token': token}

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        price = handle_quote_data(data)
        return jsonify(price.to_dict())
    else:
        return f"Error:{response.status_code}"

class Price:
    def __init__(self, curr_price, high_price, low_price, opening_price, previous_closing_price, price_change):
        self.curr_price = curr_price
        self.high_price = high_price
        self.low_price = low_price
        self.opening_price = opening_price
        self.previous_closing_price = previous_closing_price
        self.price_change = price_change

    def to_dict(self):
        return {
            'curr_price': self.curr_price,
            'high_price': self.high_price,
            'low_price': self.low_price,
            'opening_price': self.opening_price,
            'previous_closing_price': self.previous_closing_price,
            'price_changed': self.price_change,
        }


def handle_quote_data(data):
    curr_price = round(data["c"] * 100)
    high_price = round(data["h"] * 100)
    low_price = round(data["l"] * 100)
    opening_price = round(data["o"] * 100)
    previous_close_price = round(data["pc"] * 100)
    price_change = round(data["d"] * 100)

    price = Price(curr_price, high_price, low_price, opening_price, previous_close_price, price_change)

    return price

