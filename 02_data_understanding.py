#! /usr/bin/python
import bulk_script

# CryptoBot - data understanding historical #

# Import Libraries & API Keys
from binance.client import Client
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()
binance_api_key = os.getenv("BINANCE_API_KEY")
binance_api_secret = os.getenv("BINANCE_API_SECRET")
client = Client(binance_api_key, binance_api_secret, testnet=True)

# Historical Data (Market Data Endpoint) #

# https://binance-docs.github.io/apidocs/spot/en/#market-data-endpoints

# Trade based #

# These data reflect the completed transactions where buyers and sellers have executed their orders on the platform.

# Get trades from Market Data Endpoint
def get_hist_trad_data(symbol, limit):
    
    historical_trades = client.get_historical_trades(symbol=symbol, limit=limit)

    return historical_trades

# Build dataframe
def build_trad_data_frame(historical_trades):

    df = pd.DataFrame(historical_trades)
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    columns_to_keep = ['time', 'price']
    df = df[columns_to_keep]

    return df

# run script trades #

# Select parameters
symbol_array = ["BTCUSDT", "ETHBTC"] 
limit=1000

for symbol in symbol_array:

    trades = get_hist_trad_data(symbol, limit)
    df = build_trad_data_frame(trades)
    bulk_script.insert_elastic_search(df, symbol)