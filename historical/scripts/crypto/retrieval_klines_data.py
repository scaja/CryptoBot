#! /usr/bin/python

# Import custom scripts for data preprocessing and database operations
import load_to_elastic as load_to_elastic

# Import required libraries
from dotenv import load_dotenv  # Library to load environment variables from a .env file
import pandas as pd  # Pandas for data manipulation
import os  # OS module to access environment variables
import time
import requests
from pathlib import Path


# Function to fetch historical market data (Klines/candlestick data)
def get_historical_klines(symbol, interval, start_date, end_date, limit=1000):

    """
    Fetches historical Kline (candlestick) data from Binance for a given symbol and interval.

    :param symbol: Trading pair symbol (e.g., 'BTCUSDT')
    :param interval: Time interval for each Kline (e.g., '1m', '1h', '1d')
    :param start_str: Start date/time for fetching historical data (e.g., '1 Jan, 2023')
    :return: Pandas DataFrame containing the historical market data
    """

    url = "https://api.binance.com/api/v3/klines"

    print("url_klines")
    print(url)

    # Convert dates to timestamps in milliseconds
    start_ts = int(pd.Timestamp(start_date).timestamp() * 1000)
    end_ts = int(pd.Timestamp(end_date).timestamp() * 1000)

    while start_ts < end_ts:

        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": start_ts,
            "limit": limit
        }
    
        response = requests.get(url, params=params)
        data = response.json()

        if not data:
            break  # Stop if no more data is returned
 
        # Update start timestamp to last returned timestamp + 1 ms
        start_ts = data[-1][0] + 1
    
        # Convert the raw data into a Pandas DataFrame with appropriate column names
        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])

        df["symbol"] = symbol

        # Convert timestamp from milliseconds to a readable datetime format
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')

        # Convert numeric columns to float for proper analysis
        df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)

        load_to_elastic.insert_elastic_search(df,"klines")

        time.sleep(0.5)

    return True # Return the processed DataFrame

        
get_historical_klines("BTCUSDT", "1m", "2025-03-30", "2025-03-31")



