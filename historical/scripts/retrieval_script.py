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

# Get klines from Market Data Endpoint
def get_historical_klines(symbol, interval, start_str):
    klines = client.get_historical_klines(symbol, interval, start_str)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    print(df.head(3))
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
    return df


#historical_trades = get_hist_trad_data(symbol, limit)

btc_data = get_historical_klines('BTCUSDT', '1m', '3 months ago UTC')
eth_data = get_historical_klines('ETHUSDT', '1m', '3 months ago UTC')

btc_data = btc_data.rename(columns={
    'close': 'BTC_close',
    'volume': 'BTC_volume'
})

eth_data = eth_data.rename(columns={
    'close': 'ETH_close',
    'volume': 'ETH_volume'
})

btc_data.head(3)

df = pd.merge(btc_data[['timestamp', 'BTC_close', 'BTC_volume']],
              eth_data[['timestamp', 'ETH_close', 'ETH_volume']],
              on='timestamp', how='inner')

df = preprocessing_script.build_trad_data_frame(df)
bulk_script.insert_elastic_search(df, "historical")