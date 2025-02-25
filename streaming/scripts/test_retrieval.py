#! /usr/bin/python

import test_preprocessing as test_preprocessing 
import test_bulk as test_bulk

import websocket
import json
from datetime import datetime, timezone

# Define symbols and interval
symbols = ["btcusdt", "ethbtc"]
interval = "1m"  

# Construct WebSocket URL for multiple streams
socket = f"wss://stream.binance.com:9443/stream?streams={'/'.join([f'{s}@kline_{interval}' for s in symbols])}"


def on_message(ws, message):
    """Handles incoming WebSocket messages for multiple kline data."""
    data = json.loads(message)
    
    # Extract kline data
    kline = data["data"]["k"]
    symbol = data["data"]["s"]

     # **Check if the Kline is finalized**
    if not kline["x"]:
        return  # Ignore non-final Klines

    streaming_df = test_preprocessing.build_streaming_df(kline, symbol)

    if not streaming_df:

        index = "streaming"
        streaming_data = test_bulk.insert_elastic_search(streaming_df, index)

        prediction_df = test_preprocessing.build_prediction_df(streaming_data)
    
        prediction = test_bulk.insert_prediction(prediction_df, index)

        print("prediction")
        print(prediction)

        #test_bulk.insert_prediction(index, , prediction)
    

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed.")
    #print("reconnecting")
    #reconnect()

def on_open(ws):
    print(f"Connected to Binance WebSocket for {symbols} @ {interval} interval.")

def reconnect():
    ws = websocket.WebSocketApp(socket, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

# Start WebSocket
ws = websocket.WebSocketApp(socket, on_message=on_message, on_error=on_error, on_close=on_close)
ws.on_open = on_open
ws.run_forever()