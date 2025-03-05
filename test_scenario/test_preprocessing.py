#! /usr/bin/python

import pandas as pd
from datetime import datetime, timezone

# Build dataframe
def build_streaming_df(kline, symbol):

    close_price = float(kline["c"])  
    high = float(kline["h"])
    low = float(kline["l"])

    price_change = (close_price - low) / low
    volatility = high - low

    stock_symbol = symbol[:3].upper()

    transformed_data = {
        "timestamp": datetime.fromtimestamp(kline["t"] / 1000, timezone.utc).isoformat(),  # Keep the original timestamp
        stock_symbol + "_close": float(kline["c"]),  
        stock_symbol + "_volume": float(kline["v"]),  
        stock_symbol + "_price_change": price_change,  
        stock_symbol + "_volatility": volatility, 
        "time_numeric": kline["t"] // 1000 
    }

    print("transformed_data:", transformed_data)


    structured_data = pd.DataFrame([transformed_data])


    print("structured_data:", structured_data)

    return structured_data

def build_prediction_df(streaming_data):

    flat_data = []

    for item in streaming_data:
        if isinstance(item, dict):
            flat_data.append(item)
        elif isinstance(item, list):
            flat_data.extend(item)

    df = pd.DataFrame(flat_data)
    df['BTC_ETH_ratio'] = df['BTC_close'] / df['ETH_close']

    df["BTC_lag_1"] = df["BTC_close"].shift(1)
    df["BTC_lag_3"] = df["BTC_close"].shift(3)
    df["ETH_lag_1"] = df["ETH_close"].shift(1)
    df["ETH_lag_3"] = df["ETH_close"].shift(3)

    df = df.dropna(subset=["BTC_lag_1", "BTC_lag_3", "ETH_lag_1", "ETH_lag_3"])

    return df

    
