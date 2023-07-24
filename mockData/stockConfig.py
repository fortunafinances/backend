from tables import Stock, db
from constants import STOCK_LIST
from stockAPI.apiRequests import get_stock_metadata, get_stock_quote
from stockAPI.dataProcessing import handle_metadata, handle_quote_data

#function that updates the stock table
#can add a new stock or update the stock prices
def fillStocks():
    for ticker, description in STOCK_LIST.items():
        data = get_stock_quote(ticker)
        price = handle_quote_data(data)
        existing_stock = Stock.query.get(ticker)
        
        if existing_stock:
            #update stock prices
            updateStock(existing_stock, price)
        else:
            #add new stock
            newStock = addNewStock(ticker, description, price)
            if newStock is not None:
                if newStock.businessDescription and newStock.sector:
                    db.session.add(newStock)
    db.session.commit()


#helper function that adds a new stock to the db
def addNewStock(ticker, description, price):
    data = get_stock_metadata(ticker)
    metadata = handle_metadata(data)

    if price is None:
        print("Error: price is None")
        return None
    try:
        newStock = Stock(
            ticker = ticker,
            companyName = description,
            currPrice = price.curr_price, 
            highPrice = price.high_price, 
            lowPrice = price.low_price, 
            openPrice = price.opening_price, 
            prevClosePrice = price.previous_closing_price,
            businessDescription = metadata.businessDescription,
            country = metadata.country,
            sector = metadata.sector,            
            website = metadata.website,
            officerTitle = metadata.headOfficer[0],
            officerName = metadata.headOfficer[1])

    except AttributeError as e:
        print(f"Error: {e}")
        return None

    return newStock

#helper function that updates the stock prices in the db
def updateStock(existing_stock, price):
        existing_stock.currPrice = price.curr_price
        existing_stock.highPrice = price.high_price
        existing_stock.lowPrice = price.low_price
        existing_stock.openPrice = price.opening_price
        existing_stock.prevClosePrice = price.previous_closing_price    

#makes and API call and returns a list of dictionaries, [ticker, companyName]
# def stock_list():
#     data = get_stock_list('US')
#     return handle_stock_list(data)

#function that clears the stock table in the db 
def clearStockTable():
    Stock.query.delete()
    db.session.commit()