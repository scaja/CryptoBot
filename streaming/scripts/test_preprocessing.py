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
        "utc_time": datetime.fromtimestamp(kline["t"] / 1000, timezone.utc).isoformat(),  # Keep the original timestamp
        stock_symbol + "_close": float(kline["c"]),  
        stock_symbol + "_volume": float(kline["v"]),  
        stock_symbol + "_price_change": price_change,  
        stock_symbol + "_volatility": volatility, 
        "timestamp": kline["t"] // 1000 
    }

    #print(transformed_data)

    structured_data = pd.DataFrame([transformed_data])

    print(structured_data)

    return structured_data

    
