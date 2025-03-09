#! /usr/bin/python

# Import custom scripts for data preprocessing and database operations
import preprocessing_script as preprocessing_script
import bulk_script as bulk_script

# Import required libraries
from binance.client import Client  # Binance API client for fetching market data
from dotenv import load_dotenv  # Library to load environment variables from a .env file
import pandas as pd  # Pandas for data manipulation
import os  # OS module to access environment variables

# Historical Data (Market Data Endpoint)
# Reference: https://binance-docs.github.io/apidocs/spot/en/#market-data-endpoints

# Load API credentials from the .env file
load_dotenv()  
binance_api_key = os.getenv("BINANCE_API_KEY")  # Fetch Binance API key
binance_api_secret = os.getenv("BINANCE_API_SECRET")  # Fetch Binance API secret

# Initialize Binance API client with testnet mode enabled (for safe testing)
client = Client(binance_api_key, binance_api_secret, testnet=True)

print("salut")

# Function to fetch historical market data (Klines/candlestick data)
def get_historical_klines(symbol, interval, start_str):

    """
    Fetches historical Kline (candlestick) data from Binance for a given symbol and interval.

    :param symbol: Trading pair symbol (e.g., 'BTCUSDT')
    :param interval: Time interval for each Kline (e.g., '1m', '1h', '1d')
    :param start_str: Start date/time for fetching historical data (e.g., '1 Jan, 2023')
    :return: Pandas DataFrame containing the historical market data
    """

    # Retrieve Kline data from Binance API
    klines = client.get_historical_klines(symbol, interval, start_str)

    # Convert the raw data into a Pandas DataFrame with appropriate column names
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])

    # Print the first three rows for verification
    print("df_head")
    print(df.head(3))

    # Convert timestamp from milliseconds to a readable datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Convert numeric columns to float for proper analysis
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)

    return df  # Return the processed DataFrame


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