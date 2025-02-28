#! /usr/bin/python

import preprocessing_script as preprocessing_script 
import bulk_script as bulk_script

#from binance.client import Clientv
import websocket
import json

# Define symbols and interval
symbols = ["btcusdt", "ethusdt"]
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

    streaming_df = preprocessing_script.build_streaming_df(kline, symbol)
    print("streaming_df", streaming_df)

    index = "streaming"
    streaming_data = bulk_script.insert_elastic_search(streaming_df, index)
    print("streaming_data", streaming_data)

    if len(streaming_data) != 0:
        prediction_df = preprocessing_script.build_prediction_df(streaming_data)
        print("prediction_df", prediction_df)

        bulk_script.insert_prediction(prediction_df, index)

        print("Succcess")    
 
def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print('### closed ###')
    #print("reconnecting")
    #reconnect()
    
def on_open(ws):
    print(f"Connected to Binance WebSocket for {symbols} @ {interval} interval.")

def reconnect():
    ws = websocket.WebSocketApp(socket, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

# Select parameters
ws = websocket.WebSocketApp(socket, on_message=on_message, on_error=on_error, on_close=on_close)
ws.on_open = on_open
ws.run_forever()
