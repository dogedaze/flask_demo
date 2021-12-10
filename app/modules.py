import yfinance  as yf
from flask import render_template, flash, redirect, url_for,request,jsonify


#Function to Get Different Kinds Of Info From a Stock Ticker Directly Through API 
def ticker_info():
    ticker_name = request.args.get('symbol', default="AAPL")
    quote = yf.Ticker(ticker_name)
    ticker_data = quote.history(period="max")
    return  jsonify(ticker_data)
#Function to Pull Current Price from a Stock Ticker Directly Through API

def current_ticker_price():
    ticker_name = input('symbol', default="AAPL")
    ticker_symbol = yf.Ticker(ticker_name)
    ticker_data = ticker_symbol.history(period="min")
    ticker_open = ticker_data.filter(['Open'])
    ticker_open = ticker_open.rename(columns = {"Open": ticker_name}) 
    print(ticker_open)


import pymongo
import json
import requests
#retrieving historical prices from Apple.
historical_prices = requests.get('https://financialmodelingprep.com/api/v3/historical-chart/1min/AAPL?apikey=9cd6b96b4b472eb298b9178e91959c51')

#retrieving historical prices from Apple.
historical_prices = requests.get('https://financialmodelingprep.com/api/v3/historical-chart/1min/AAPL?apikey=9cd6b96b4b472eb298b9178e91959c51')

client = pymongo.MongoClient("mongodb://pythonforfinance:mypassword@cluster0-shard-00-00-apl4w.mongodb.net:27017,cluster0-shard-00-01-apl4w.mongodb.net:27017,cluster0-shard-00-02-apl4w.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client['historical_prices']
print (db)
earnings_surprises = requests.get ('https://financialmodelingprep.com/api/v3/earnings-surprises/AAPL?apikey=9cd6b96b4b472eb298b9178e91959c51')
earnings_surprises = earnings_surprises.json()
