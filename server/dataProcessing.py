import json

#Price object
class Price:
    def __init__(self, curr_price, high_price, low_price, opening_price, previous_closing_price):
        self.curr_price = curr_price
        self.high_price = high_price
        self.low_price = low_price
        self.opening_price = opening_price
        self.previous_closing_price = previous_closing_price

#Metadata object
class Metadata:
    def __init__(self, businessDescription, country, sector, website, headOfficer):
        self.businessDescription = businessDescription
        self.country = country
        self.sector = sector
        self.website = website
        self.headOfficer = headOfficer


#function that processes the quote data returned from the stock api and returns rounded int price data as a Price object
def handle_quote_data(data):
    try:
        curr_price = data['c']
        high_price = data['h']
        low_price = data['l']
        opening_price = data['o']
        previous_close_price = data['pc']
    except KeyError as ke:
        print(f"KeyError: {ke}. This key does not exist in the provided data")
        return None
    except TypeError as te:
        print(f"TypeError: {te}. Expected a number for rounding but got a different type.")
        return None
    
    price = Price(curr_price, high_price, low_price, opening_price, previous_close_price)

    return price

#function that iterates through the stock list data returned from the stock api and returns a list of the first 100 available stock symbols
def handle_stock_list(data):
    parsed_list = data
    stocks = [{item['symbol']: item['description']} for item in parsed_list[:50]]

    return stocks

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

    metadata = Metadata(businessDescription, country, sector, website, headOfficer)    
    return metadata 