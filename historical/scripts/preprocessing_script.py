#! /usr/bin/python

import pandas as pd
import sys  # Import sys module (though it is not used in this script)

# Function to preprocess and transform the given DataFrame
def build_trad_data_frame(df):
    """
    Processes a given DataFrame to calculate additional trading indicators.
    Includes price change percentage, volatility, and BTC/ETH ratio.
    """

    # Calculate the percentage change in closing prices for BTC and ETH
    df['BTC_price_change'] = df['BTC_close'].pct_change()  
    df['ETH_price_change'] = df['ETH_close'].pct_change()  

    # Compute volatility as the difference between the max and min closing prices
    # in a rolling window of 3 periods for BTC and ETH
    df['BTC_volatility'] = df['BTC_close'].rolling(window=3).apply(lambda x: x.max() - x.min())  
    df['ETH_volatility'] = df['ETH_close'].rolling(window=3).apply(lambda x: x.max() - x.min())  

    # Calculate the ratio of BTC closing price to ETH closing price
    df['BTC_ETH_ratio'] = df['BTC_close'] / df['ETH_close']  

    # Convert timestamp column to a datetime object for better time-based operations
    df["timestamp"] = pd.to_datetime(df["timestamp"])  

    # Convert the timestamp to a numeric format (Unix timestamp in seconds)
    df["time_numeric"] = df["timestamp"].astype('int64') // 10**9  

    # Remove any rows with NaN values resulting from rolling calculations
    df.dropna(inplace=True)  

    return df  # Return the transformed DataFrame
