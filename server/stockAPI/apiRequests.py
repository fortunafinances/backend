import requests
from dotenv import load_dotenv
import os
import time
from requests.exceptions import HTTPError

load_dotenv()
finn_key = os.environ.get('FINN_API_KEY')
yahoo_key = os.environ.get('YAHOO_API_KEY')

MAX_REQUESTS = 60 #api request rate limit 
TIME_PERIOD = 60 # 60 seconds in a minute

start_time = time.time()
request_count = 0


#calls finnhub API and gets current price data
def get_stock_quote(symbol):
    global request_count
    global start_time

    url= "https://finnhub.io/api/v1/quote"
    token = finn_key
    params = {'symbol': symbol, 'token': token}

    try: 
        if request_count >= MAX_REQUESTS:
            time_waited = time.time() - start_time
            if time_waited < TIME_PERIOD:
                time_to_wait = TIME_PERIOD - time_waited
            print(f"Rate limt exceeded. Waiting for {time_to_wait: .2f} seconds")
            time.sleep(time_to_wait)

            request_count = 0
            start_time = time.time()

        response = requests.get(url, params=params)

        response.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occured: {http_err}')
    except Exception as e:
        print(f'Other exception occured: {e}')
    else:
        request_count += 1
        data = response.json()
        return data
    
#calls finhub api and gets a list of available stocks
def get_stock_list(exchange):
    url = "https://finnhub.io/api/v1/stock/symbol"
    token = finn_key
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
	    "X-RapidAPI-Key": yahoo_key,
	    "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return f"Error:{response.status_code}"