#! /usr/bin/python

import pandas as pd
import sys

# Build dataframe
def build_trad_data_frame(df):

    df['BTC_price_change'] = df['BTC_close'].pct_change()
    df['ETH_price_change'] = df['ETH_close'].pct_change()

    df['BTC_volatility'] = df['BTC_close'].rolling(window=3).apply(lambda x: x.max() - x.min())
    df['ETH_volatility'] = df['ETH_close'].rolling(window=3).apply(lambda x: x.max() - x.min())

    df['BTC_ETH_ratio'] = df['BTC_close'] / df['ETH_close']

    df.dropna(inplace=True)

    return df
