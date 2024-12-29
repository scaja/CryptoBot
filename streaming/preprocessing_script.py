#! /usr/bin/python

import pandas as pd
import sys

# Build dataframe
def build_trad_data_frame(df, symbol):

    #print('hello')

    #df = pd.DataFrame(historical_trades)
    df.columns = ['time', 'price']
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    columns_to_keep = ['time', 'price']
    df = df[columns_to_keep]
    df["symbol"] = str(symbol.lower())

    print(df)

    #sys.exit()

    return df

    
