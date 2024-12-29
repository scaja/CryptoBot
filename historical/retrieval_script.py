#! /usr/bin/python

# Import scripts
import preprocessing_script as preprocessing_script
import bulk_script as bulk_script

# Import Libraries & API Keys
from binance.client import Client
from dotenv import load_dotenv
import pandas as pd
import os

# Historical Data (Market Data Endpoint) #
# https://binance-docs.github.io/apidocs/spot/en/#market-data-endpoints

# Load credentials
load_dotenv()
binance_api_key = os.getenv("BINANCE_API_KEY")
binance_api_secret = os.getenv("BINANCE_API_SECRET")
client = Client(binance_api_key, binance_api_secret, testnet=True)

# Get trades from Market Data Endpoint
def get_hist_trad_data(symbol, limit):
    
    historical_trades = client.get_historical_trades(symbol=symbol, limit=limit)

    return historical_trades

# run script trades #

# Select parameters
symbol_array = ["BTCUSDT", "ETHBTC"] 
limit=3
index = "historical"

for symbol in symbol_array:

    historical_trades = get_hist_trad_data(symbol, limit)
    df = preprocessing_script.build_trad_data_frame(historical_trades, symbol)
    bulk_script.insert_elastic_search(df, index)