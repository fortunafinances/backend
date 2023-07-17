from flask import jsonify
import json
import requests
from dataProcessing import handle_quote_data

#calls finnhub API and gets current price data
def get_stock_quote(symbol):
    url= "https://finnhub.io/api/v1/quote"
    token = "cimn4r1r01qhp3kcngjgcimn4r1r01qhp3kcngk0"
    params = {'symbol': symbol, 'token': token}

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data
        # price = handle_quote_data(data, symbol)
        # return jsonify(price.to_dict())
    else:
        return f"Error:{response.status_code}"
    
#calls finhub api and gets a list of available stocks
def get_stock_list(exchange):
    url = "https://finnhub.io/api/v1/stock/symbol"
    token = "cimn4r1r01qhp3kcngjgcimn4r1r01qhp3kcngk0"
    params = {'exchange': exchange, 'token': token}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else: 
        return f"Error:{response.status_code}"

#calls yahoo api and gets the metadata for a certain stock
def get_stock_metadata(symbol):
    url = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/mo/module/{symbol}"
    querystring = {"symbol": {symbol}, "module":"asset-profile,financial-data,earnings"}
    headers = {
	    "X-RapidAPI-Key": "644b6f939cmsh7870173263c710dp1b2239jsn7d641867ae16",
	    "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return f"Error:{response.status_code}"