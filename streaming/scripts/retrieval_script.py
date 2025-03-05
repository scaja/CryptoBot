#! /usr/bin/python

# Import necessary modules
import preprocessing_script as preprocessing_script  # Custom module for preprocessing
import bulk_script as bulk_script  # Custom module for bulk insertion into Elasticsearch

# Uncomment if you want to use Binance's Client library (not used in this script)
#from binance.client import Client

# Importing WebSocket and JSON libraries
import websocket
import json

# Define the symbols (cryptocurrency pairs) and the interval (time period for each kline/candle)
symbols = ["btcusdt", "ethusdt"]  # BTC/USDT and ETH/USDT
interval = "1m"  # 1-minute interval for each kline

# Construct the WebSocket URL for streaming kline (candlestick) data for multiple symbols
socket = f"wss://stream.binance.com:9443/stream?streams={'/'.join([f'{s}@kline_{interval}' for s in symbols])}"

# WebSocket on_message callback function to handle incoming data
def on_message(ws, message):
    """Handles incoming WebSocket messages for multiple kline data."""
    
    # Parse the incoming JSON message
    data = json.loads(message)
    
    # Extract kline data and symbol from the message
    kline = data["data"]["k"]
    symbol = data["data"]["s"]

    # **Check if the Kline is finalized** - Only process finalized (closed) kline data
    if not kline["x"]:
        return  # If kline is not finalized, ignore it

    # Use preprocessing script to build the streaming dataframe with the kline data and symbol
    streaming_df = preprocessing_script.build_streaming_df(kline, symbol)
    print("streaming_df", streaming_df)  # Print the constructed DataFrame

    # Define the Elasticsearch index where the data will be inserted
    index = "streaming"

    # Insert the constructed streaming data into Elasticsearch using the bulk script
    streaming_data = bulk_script.insert_elastic_search(streaming_df, index)
    print("streaming_data", streaming_data)  # Print the data inserted into Elasticsearch

    # If data was successfully inserted, proceed to build prediction DataFrame
    if len(streaming_data) != 0:
        # Build the prediction DataFrame using the streaming data
        prediction_df = preprocessing_script.build_prediction_df(streaming_data)
        print("prediction_df", prediction_df)  # Print the prediction DataFrame

        # Insert prediction data into Elasticsearch using the bulk script
        bulk_script.insert_prediction(prediction_df, index)

        print("Success")  # Indicate that the data was successfully inserted and processed

# WebSocket on_error callback function to handle any errors that occur
def on_error(ws, error):
    print(f"Error: {error}")  # Print the error message

# WebSocket on_close callback function to handle the closing of the WebSocket connection
def on_close(ws, close_status_code, close_msg):
    print('### closed ###')  # Indicate that the WebSocket connection is closed
    # Uncomment the following line to attempt reconnection when the connection is closed
    # reconnect()

# WebSocket on_open callback function to handle when the WebSocket connection is opened
def on_open(ws):
    print(f"Connected to Binance WebSocket for {symbols} @ {interval} interval.")  # Print connection status

# Function to reconnect the WebSocket if it gets disconnected (not used in this script directly)
def reconnect():
    # Create a new WebSocket connection and run it
    ws = websocket.WebSocketApp(socket, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open  # Set the on_open callback
    ws.run_forever()  # Run the WebSocket connection forever

# Create the WebSocketApp and start listening to incoming messages from Binance
ws = websocket.WebSocketApp(socket, on_message=on_message, on_error=on_error, on_close=on_close)
ws.on_open = on_open  # Set the on_open callback
ws.run_forever()  # Start the WebSocket connection and keep it open