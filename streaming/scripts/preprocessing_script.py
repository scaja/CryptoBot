#! /usr/bin/python

import pandas as pd
from datetime import datetime, timezone

# Function to build the streaming DataFrame from kline data
def build_streaming_df(kline, symbol):
    # Extract the closing price from the 'kline' object and convert it to a float
    close_price = float(kline["c"])  
    # Extract the highest price from the 'kline' object and convert it to a float
    high = float(kline["h"])
    # Extract the lowest price from the 'kline' object and convert it to a float
    low = float(kline["l"])

    # Calculate the price change as the ratio of the change from low to close price
    price_change = (close_price - low) / low
    # Calculate volatility as the difference between high and low prices
    volatility = high - low

    # Extract the stock symbol and ensure it's in uppercase and only the first 3 characters
    stock_symbol = symbol[:3].upper()

    # Create a dictionary with transformed data
    transformed_data = {
        # Convert the timestamp to ISO 8601 format
        "timestamp": datetime.fromtimestamp(kline["t"] / 1000, timezone.utc).isoformat(),  # Keep the original timestamp
        # Add the close price, volume, price change, and volatility for the symbol to the dictionary
        stock_symbol + "_close": float(kline["c"]),  
        stock_symbol + "_volume": float(kline["v"]),  
        stock_symbol + "_price_change": price_change,  
        stock_symbol + "_volatility": volatility, 
        # Store the timestamp in a numeric form (seconds since the Unix epoch)
        "time_numeric": kline["t"] // 1000 
    }

    # Print the transformed data to check the results
    print("transformed_data:", transformed_data)

    # Convert the transformed data into a pandas DataFrame
    structured_data = pd.DataFrame([transformed_data])

    # Print the structured data (DataFrame) for verification
    print("structured_data:", structured_data)

    # Return the DataFrame containing the transformed data
    return structured_data

# Function to build a DataFrame for prediction based on streaming data
def build_prediction_df(streaming_data):
    # An empty list to collect the flattened data (flat data structure)
    flat_data = []

    # Iterate over all items in the 'streaming_data'
    for item in streaming_data:
        # If the item is a dictionary, append it to the 'flat_data' list
        if isinstance(item, dict):
            flat_data.append(item)
        # If the item is a list, extend it and add the elements to the 'flat_data' list
        elif isinstance(item, list):
            flat_data.extend(item)

    # Convert the flattened data into a pandas DataFrame
    df = pd.DataFrame(flat_data)

    # Calculate the BTC-ETH ratio and add it as a new column to the DataFrame
    df['BTC_ETH_ratio'] = df['BTC_close'] / df['ETH_close']

    # Create lag features (1-day and 3-day lags) for BTC and ETH closing prices
    df["BTC_lag_1"] = df["BTC_close"].shift(1)  # 1-day lag for BTC
    df["BTC_lag_3"] = df["BTC_close"].shift(3)  # 3-day lag for BTC
    df["ETH_lag_1"] = df["ETH_close"].shift(1)  # 1-day lag for ETH
    df["ETH_lag_3"] = df["ETH_close"].shift(3)  # 3-day lag for ETH

    # Drop rows that have missing values for the lag features
    df = df.dropna(subset=["BTC_lag_1", "BTC_lag_3", "ETH_lag_1", "ETH_lag_3"])

    # Return the DataFrame with the new calculated features
    return df