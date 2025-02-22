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

    structured_data = test_preprocessing.build_streaming_df(kline, symbol)

    index = "streaming"
    test_bulk.insert_elastic_search(structured_data, index)

    # Print structured data
    #print(structured_data)

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed. Reconnecting...")
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