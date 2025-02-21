#! /usr/bin/python

import pandas as pd
from datetime import datetime, timezone
#import sys

# Build dataframe
def build_streaming_df(kline, symbol):

    timestamp = datetime.fromtimestamp(kline["t"] / 1000, timezone.utc).isoformat()
    time_numeric = kline["t"] // 1000  
    close_price = float(kline["c"])  
    volume = float(kline["v"])  
    high = float(kline["h"])
    low = float(kline["l"])

    # Compute volatility and price change
    price_change = (close_price - low) / low
    volatility = high - low

    # Structure the extracted data
    structured_data = {
        "symbol": symbol,
        "timestamp": timestamp,  # Now using ISO format with UTC timezone
        "close_price": close_price,
        "volume": volume,
        "price_change": price_change,
        "volatility": volatility,
        "time_numeric": time_numeric
    }

    return structured_data

    
