#! /usr/bin/python
# CryptoBot - data understanding historical

# 1. Import Libraries & API Keys
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

# print to json file
def print_to_json_file(filename,df):
  
    json_str = df.to_json(orient='records', date_format="iso")  

    with open(filename, "w") as file:
        file.write(json_str)
    print("Text file written!", filename)

# run script trades #

# Select parameters
symbol_array = ["BTCUSDT", "ETHBTC"] 
limit=1000

path = "data/historical_data/trades"
os.makedirs(path, exist_ok=True)

for symbol in symbol_array:

    filename = path + '/' + symbol + '.json'

    trades = get_hist_trad_data(symbol, limit)
    df = build_trad_data_frame(trades)
    print_to_json_file(filename, df)


