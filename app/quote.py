import yfinance as yf
from flask import Flask, request, render_template, jsonify

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