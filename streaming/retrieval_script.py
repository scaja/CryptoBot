#! /usr/bin/python

import preprocessing_script as preprocessing_script 
import bulk_script as bulk_script

#from binance import BinanceSocketManager
from binance.client import Client
from dotenv import load_dotenv
import websocket
import pandas as pd
import json
import os
import threading
import os

# Streaming Data (Websocket Market Endpoint) #
# https://binance-docs.github.io/apidocs/spot/en/#websocket-market-streams

# Load credentials
load_dotenv()
binance_api_key = os.getenv("BINANCE_API_KEY")
binance_api_secret = os.getenv("BINANCE_API_SECRET")
client = Client(binance_api_key, binance_api_secret, testnet=True)

# Get trades from Websocket Market Endpoint
def on_message(ws, message):
    msg = json.loads(message)
    print(msg)
    d = [(msg['T'],msg['p'])]
    df = pd.DataFrame.from_records(d)
    df_streaming_data = preprocessing_script.build_trad_data_frame(df, symbol)
    bulk_script.insert_elastic_search(df_streaming_data, index)
 
def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print('### closed ###')
    
def on_open(ws):
    print("Opened connection")
    # Start a timer to close the WebSocket after 5 seconds
    def stop_stream():
        print("Closing WebSocket after 5 seconds...")
        ws.close()
    
    timer = threading.Timer(5, stop_stream)
    timer.start()

# run script trades #

# Select parameters
symbol_array = ['btcusdt','ethbtc']
index = "streaming"

for symbol in symbol_array:

    df = pd.DataFrame()

    socket = f'wss://stream.binance.com:9443/ws/{symbol}@trade'

    print(socket)
    
    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_error=on_error,on_close=on_close)
    ws.run_forever()