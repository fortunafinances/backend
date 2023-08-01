import requests
from dotenv import load_dotenv
import os

STOCK_LIST = {
    "AAPL": "Apple Inc.", 
    "GOOGL": "Alphabet Inc.", 
    "AMZN": "Amazon.com Inc.", 
    "MSFT": "Microsoft Corporation", 
    "META": "Meta Inc.", 
    "TSLA": "Tesla Inc.", 
    "JPM": "JPMorgan Chase & Co.", 
    "V": "Visa Inc.", 
    "JNJ": "Johnson & Johnson", 
    "BAC": "Bank of America Corp.", 
    "WMT": "Walmart Inc.", 
    "PG": "Procter & Gamble Co.", 
    "MA": "Mastercard Incorporated", 
    "UNH": "UnitedHealth Group Incorporated", 
    "HD": "The Home Depot Inc.",
    "DNUT": "Krispy Kreme Inc.",
    "ADI" : "Analog Devices, Inc.", 
    "AMAT" : "Applied Materials Inc.", 
    "T" : "AT&T Inc.", 
    "ADSK" : "Autodesk Inc.", 
    "BAX" : "Baxter International Inc", 
    "CBOE": "Cboe Global Markets Inc", 
    "C": "Citigroup Inc", 
    "DHR": "Danaher Corp", 
    "DIS": "The Walt Disney Co", 
    "DOW": "Dow Inc", 
    "ECL": "Ecolab Inc", 
    "EQR": "Equity Residential", 
    "EVRG": "Evergy Inc", 
    "TGT": "Target Corp.",
    "EXC": "Exelon Corp", 
    "FISV": "Fiserv Inc", 
    "GIS": "General Mills Inc", 
    "HON": "Honeywell International Inc.", 
    "HPE": "Hewlett Packard Enterprise Co.", 
    "HUM": "Humana Inc.", 
    "INTU": "Intuit Inc.", 
    "LHX": "L3Harris Technologies Inc.", 
    "MAR": "Marriott International Inc.", 
    "MCD": "McDonald's Corp.", 
    "MRK": "Merck & Co., Inc.", 
    "SOFI": "SoFi Technologies Inc.", 
    "MCO": "Moody's Corp.", 
    "MOS": "The Mosaic Co.", 
    "MTB": "M&T Bank Corp.",
    "SPGI": "S&P Global Inc.", 
    "SYF": "Synchrony Financial", 
    "TROW": "T. Rowe Price Group Inc.", 
    "TFC": "Truist Financial Corp", 
    "VZ": "Verizon Communications Inc." 
}

load_dotenv()
pschat_token = os.environ.get('PSCHAT_TOKEN')


def getGPTData(input):
    print(input)
    modelType = "gpt35turbo"

    # pass in token to headers for authentication 
    headers = {
        "Authorization": f"Bearer " + pschat_token,
        "Content-Type": "application/json",
    }
    data = {
        # promt to send to the chat box
        "message": f"""
                  You are a stock recommendation generator of a 
                   trading application for a financial service company.
                   Given this stock list: {STOCK_LIST},
                   take in {input} as the request categories from the user.
                   Based on these parameters, return a string array that 
                   contains only 5 tickers from the stock list that fall under
                   at least one of the categories the user requested.
                   Output should be something like ["TSLA", "JPM"].
                   Format it exactly like: ["TSLA", "JPM", "AAPL"].
                   Do not include any extraneous information. 
                   Only include the stocks in a list. This is important!
                   DO NOT SAY ANYTHING ELSE EXCEPT THE LIST!
                  """,
        # model of PS chat we want to use
        "options": {
            "model": modelType
        }
    }

    # try-except block sends POST request to the chatbot API using requests, with the prompt and headers
    # as param. Then the response is parsed as JSON
    try:
        url = "https://api.psnext.info/api/chat"

        # request response from chatbot
        response = requests.post(url, json=data, headers=headers)

        response_data = response.json()
        print(response_data)
        return response_data["data"]["messages"][2]["content"]
    
    # catch error if there's any
    except Exception as error:
        print("FAILED PROMPT")
        print(error)