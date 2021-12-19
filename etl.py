# This is where you could keep your code that loads
# data in the database. It is not used by Flask but
# it is convenient to save in the same directory.

#SH
import yfinance as yf #Allows us to Use Yahoo Finance API 
import pandas as pd
import numpy as np
import json

#SH
#To setup the postgreSQL Database using PgAdmin

import psycopg2, os

print('Connecting to the PostgreSQL database...')
conn = psycopg2.connect(
    host="localhost",
    port='5432',
    database="postgres",
    user="postgres",
    password="123")
cur = conn.cursor()

#SH
# execute a statement
print('PostgreSQL database version:')
cur.execute('SELECT version()')

# display the PostgreSQL database server version
db_version = cur.fetchone()
print(db_version)

#CREATE THE TABLES TO BE USED IN THE DATABASE
createCmd = """
DROP TABLE IF EXISTS stock_prices;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS trades;

CREATE TABLE stock_prices (
                price_date date,
                ticker varchar(20) NOT NULL,
                price float NOT NULL,
                PRIMARY KEY (price_date, ticker)
                );
                
                CREATE TABLE trades (
                uid integer NOT NULL,
                ticker varchar(20) NOT NULL,
                trade_date date,
                amount integer
                );
        
                
                CREATE TABLE users (
                uid integer,
                user_name varchar (100),
                fantasy_name varchar (100),
                PRIMARY KEY (uid)
                );
            """
    
cur.execute(createCmd)
conn.commit()

#SH
#Specifying the Stock tickers to be pulled from the API
array = ["MSFT", "AAPL", "TSLA", "SONY", "MCD", "FB", "JPM", "DIS", "COST", "CVS", "NFLX", "SBUX", "UBER", 
         "NKE", "AMZN", "PFE", "GOOGL", "LRLCY", "DELL", "UNH", "SPY", "VTI", "VOO", "VWO", "VEA", "QQQ", 
         "IVV", "IEFA", "EFA", "AGG"]

#Loop to Pull the Data from the API
prices = []
for ticker in array:
    open_prices = yf.Ticker(ticker).history(period="6mo").filter(["Open"])
    open_prices.reset_index()
    open_prices["date"] = open_prices.index
    open_prices["ticker"] = ticker
    prices.extend(open_prices[["date", "ticker", "Open"]].values)
print(len(prices), "prices")

#SH
#Inserts the Data into the Table in PgAdmin SQL 
print(len(prices), "prices")
query = """INSERT INTO stock_prices(price_date,ticker,price) VALUES(%s, %s, %s)"""
cur.executemany(query, tuple(prices))
conn.commit()

#SH
#Pulling the Trade Data
trade_data = pd.read_csv("User_Trades.csv", skipinitialspace=True)
print(len(trade_data.values), "trades")

#SH
trade_data

#SH
#Inserting the Trade Data into PgAdmin SQL 
print(len(trade_data), 'trades')
query = """INSERT INTO trades(uid,ticker,trade_date,amount) VALUES(%s, %s, %s, %s)"""
cur.executemany(query, trade_data.values)
conn.commit()

#SH
# Filter data to only trades that have a price. The rest are bad/illegal trades that cannot be executed as they were done on days where you cannot trade
query = """
DROP TABLE IF EXISTS trades_clean;

select t.* 
into trades_clean
from trades t, stock_prices p
where t.trade_date = p.price_date
and t.ticker = p.ticker;
"""
cur.execute(query)
conn.commit()

#SH
# Pulling the User Data
user_data = pd.read_csv("User_Data.csv")
print(len(user_data.values), "users")

#SH
user_data

#SH
#Inserting the User Data into PgAdmin SQL

print(len(user_data.values), "users")
query = """INSERT INTO users(uid, user_name, fantasy_name) VALUES(%s, %s, %s)"""
cur.executemany(query, user_data.values)
conn.commit()

#SH
#Create the Total Changes Table Which Summarizes the Differences in Stock Balances Based on User Trades 

createCmd = """
DROP TABLE IF EXISTS total_changes;

SELECT uid, SUM(t.amount * p.price) AS final_change
INTO total_changes
FROM trades_clean t, stock_prices p
WHERE t.ticker = p.ticker
AND t.trade_date = p.price_date
GROUP BY uid

"""
    
cur.execute(createCmd)
conn.commit()

#SH
# Read data from PostgreSQL database table and load into a DataFrame instance

df_total_changes = pd.read_sql("SELECT * FROM \"total_changes\"", conn);
 
pd.set_option('display.expand_frame_repr', False);

# Print the DataFrame
df_total_changes

#SH
#Creates the Final Balances Table Which Summarizes the Total Balance in Stocks Users Still Have in Their Portfolio

createCmd = """
DROP TABLE IF EXISTS final_balances;

SELECT uid, t.ticker, SUM(t.amount* p.price) AS final_balance
INTO final_balances
FROM trades_clean t, stock_prices p
WHERE t.uid = t.uid
AND t.ticker = p.ticker
AND p.price_date = (SELECT MAX(price_date) FROM stock_prices)
GROUP BY uid, t.ticker

"""
    
cur.execute(createCmd)
conn.commit()

#SH
# Read data from PostgreSQL database table and load into a DataFrame instance

df_final_balance = pd.read_sql("SELECT * FROM \"final_balances\"", conn);
 
pd.set_option('display.expand_frame_repr', False);

# Print the DataFrame
df_final_balance.to_csv('df_final_balance.csv',index=False)


#SH
#Combining the Balance and the Changes to Get the Final Portfolio Amount

createCmd = """
DROP TABLE IF EXISTS final_summary;

SELECT u.user_name, u.fantasy_name, final_change, fb
INTO final_summary
FROM users u, (SELECT uid, SUM(final_balance) as fb 
FROM final_balances f GROUP BY uid) fb, total_changes t
WHERE t.uid = u.uid
AND u.uid = fb.uid
"""
    
cur.execute(createCmd)
conn.commit()

#SH
#To Check All The Trades Made By One User
#To Change Which User just update "WHERE uid =" to user you want to select

df_trades_user_1 = pd.read_sql("""
SELECT uid, ticker, amount
FROM trades_clean 
WHERE uid = 1 
GROUP BY uid, ticker, amount
""", conn);

# Print the DataFrame
df_trades_user_1

#SH
#To Check The Trade Balance Made By One User
#To Change Which User just update "WHERE uid =" to user you want to select

df_trades_user_1 = pd.read_sql("""
SELECT uid, ticker, sum(amount) FROM \"trades_clean\" WHERE uid = 1 GROUP BY uid, ticker
""", conn);

df_trades_user_2 = pd.read_sql("""
SELECT uid, ticker, sum(amount) FROM \"trades_clean\" WHERE uid = 2 GROUP BY uid, ticker
""", conn);
# Print the DataFrame

df_trades_user_1.to_csv('df_trades_user_1.csv',index=False)
df_trades_user_2.to_csv('df_trades_user_2.csv',index=False)
#SH
#To Check The Remaining Stocks and Balance For Each User
#To Change which User just change WHERE t.uid = to another uid

df_balance_user_1 = pd.read_sql("""
SELECT uid, t.ticker, SUM(t.amount), p.price, SUM(t.amount* p.price) AS final_balance
FROM trades_clean t, stock_prices p
WHERE t.uid = 1
AND t.ticker = p.ticker
AND p.price_date = (SELECT MAX(price_date) FROM stock_prices)
GROUP BY uid, t.ticker, p.price
""", conn);

# Print the DataFrame
df_balance_user_1.to_csv('df_balance_user_1.csv',index=False)

#SH
#Final Summaries for the Users

df_final_summary = pd.read_sql("SELECT * FROM \"final_summary\" ORDER BY fb - final_change DESC", conn);
 
pd.set_option('display.expand_frame_repr', False);

# Print the DataFrame
df_final_summary.to_csv('df_final_summary.csv',index=False)

#SH
#This is the Final Rankings of the Users Based on Their Final Portfolio Amount

df_final_portfolio_amount = pd.read_sql("SELECT user_name, fantasy_name, fb - final_change as final_portfolio_amount FROM \"final_summary\" ORDER BY final_portfolio_amount DESC", conn);
 
pd.set_option('display.expand_frame_repr', False);

df_final_portfolio_amount.to_csv('df_final_portfolio_amount.csv',index=False)