import json

#Price object
class Price:
    def __init__(self, ticker, curr_price, high_price, low_price, opening_price, previous_closing_price):
        self.ticker = ticker
        self.curr_price = curr_price
        self.high_price = high_price
        self.low_price = low_price
        self.opening_price = opening_price
        self.previous_closing_price = previous_closing_price
        #self.price_change = price_change

    def to_dict(self):
        return {
            'ticker': self.ticker,
            'curr_price': self.curr_price,
            'high_price': self.high_price,
            'low_price': self.low_price,
            'opening_price': self.opening_price,
            'previous_closing_price': self.previous_closing_price,
            #'price_changed': self.price_change,
        }


#function that processes the quote data returned from the stock api and returns rounded int price data as a Price object
def handle_quote_data(data, symbol):
    try:
        ticker = symbol
        curr_price = round(data['c'] * 100)
        high_price = round(data['h'] * 100)
        low_price = round(data['l'] * 100)
        opening_price = round(data['o'] * 100)
        previous_close_price = round(data['pc'] * 100)
        #price_change = round(data["d"] * 100)
    except KeyError as ke:
        print(f"KeyError: {ke}. This key does not exist in the provided data")
        return None
    except TypeError as te:
        print(f"TypeError: {te}. Expected a number for rounding but got a different type.")
        return None
    
    price = Price(ticker, curr_price, high_price, low_price, opening_price, previous_close_price)

    return price

#function that iterates through the stock list data returned from the stock api and returns a list of the first 100 available stock symbols
def handle_stock_list(data):
    if isinstance(data, str):
        parsed_list = json.load(data)
    else:
        parsed_list = data
    ticker = [item['symbol'] for item in parsed_list[:100]]
    return ticker

def handle_metadata(data):
    try:
        businessDescription = data.get('assetProfile', {}).get('longBusinessSummary')
        country = data.get('assetProfile', {}).get('country')
        sector = data.get('assetProfile', {}).get('sector')
        website = data.get('assetProfile', {}).get('website')
        officers = data.get('assetProfile', {}).get('companyOfficers', [])

        if officers:
            officer_title = officers[0].get('title')
            officer_name = officers[0].get('name')
        else:
            officer_title = None
            officer_name = None
        
        headOfficer = [officer_title, officer_name]

    except KeyError as ke:
        print(f"KeyError: {ke}. This key does not exist in the provided data")
        return None
    except TypeError as te:
        print(f"TypeError: {te}. Expected a number for rounding but got a different type.")
        return None

    metadata = [businessDescription, country, sector, website, headOfficer]    
    return metadata 