from flask import jsonify
import json
import requests
from dataProcessing import handle_quote_data

def get_stock_quote(symbol):
    url= "https://finnhub.io/api/v1/quote"
    token = "cimn4r1r01qhp3kcngjgcimn4r1r01qhp3kcngk0"
    params = {'symbol': symbol, 'token': token}

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
<<<<<<< HEAD
        price = handle_quote_data(data, symbol)
        return jsonify(price.to_dict())
=======
        return data
        # price = handle_quote_data(data, symbol)
        # return jsonify(price.to_dict())
>>>>>>> dev
    else:
        return f"Error:{response.status_code}"
    
def get_stock_list(exchange):
    url = "https://finnhub.io/api/v1/stock/symbol"
    token = "cimn4r1r01qhp3kcngjgcimn4r1r01qhp3kcngk0"



