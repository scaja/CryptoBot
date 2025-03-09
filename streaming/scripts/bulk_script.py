#! /usr/bin/python

# Importing necessary libraries
from elasticsearch import Elasticsearch
import requests

# API URL for the prediction service (FastAPI container)
API_URL = "http://fastapi-container:8000/predict"

# Connect to the Elasticsearch cluster. 
# The host specifies the location of the Elasticsearch instance.
es = Elasticsearch(hosts="http://@elasticsearch:9200")

# Mapping defines the structure and data types of fields in the Elasticsearch index.
# It also defines how data should be interpreted (e.g., date, float, boolean).
mapping = {
    "mappings": {
        "properties": {
            # The timestamp field will store dates. `null_value` tells Elasticsearch how to handle missing data.
            "timestamp": {"type": "date", "null_value": None},

            # BTC_close field represents the closing price of Bitcoin. It's a float type with a `null_value` of None.
            "BTC_close": {"type": "float", "null_value": None},

            # BTC_volume field stores the trading volume of Bitcoin as a float.
            "BTC_volume": {"type": "float", "null_value": None},

            # ETH_close represents the closing price of Ethereum (ETH), stored as a float.
            "ETH_close": {"type": "float", "null_value": None},

            # ETH_volume represents the trading volume of Ethereum (ETH), stored as a float.
            "ETH_volume": {"type": "float", "null_value": None},

            # BTC_price_change is the percentage change in the price of Bitcoin.
            "BTC_price_change": {"type": "float", "null_value": None},

            # ETC_price_change stores the price change for Ethereum, another float field.
            "ETC_price_change": {"type": "float", "null_value": None},

            # BTC_volatility represents the volatility of Bitcoin's price, stored as a float.
            "BTC_volatility": {"type": "float", "null_value": None},

            # ETC_volatility is the volatility in the price of Ethereum.
            "ETC_volatility": {"type": "float", "null_value": None},

            # BTC_ETC_ratio represents the ratio of Bitcoin to Ethereum prices, stored as a float.
            "BTC_ETC_ratio": {"type": "float", "null_value": None},

            # BTC_close_prediction stores the predicted closing price of Bitcoin, represented as a float.
            "BTC_close_prediction": {"type": "float", "null_value": None},

            # BTC_buy_sell_signal is a boolean field indicating whether to buy or sell BTC.
            "BTC_buy_sell_signal": {"type": "boolean"},

            # time_numeric represents a timestamp as a long integer (in Unix time format).
            "time_numeric": {"type": "long", "null_value": None}
        }
    }
}


def insert_elastic_search(df, index):
    """
    Inserts a row from a DataFrame into an Elasticsearch index.
    
    Parameters:
    df (pd.DataFrame): The DataFrame containing the data to insert.
    index (str): The name of the Elasticsearch index.
    
    Returns:
    dict: A check of the inserted document for None values.
    """

    # Check if the Elasticsearch index exists; if not, create it with the predefined mapping
    if not es.indices.exists(index=index):
        es.indices.create(index=index, body=mapping)  # 'mapping' should be defined elsewhere in your code

    # Convert the first row of the DataFrame into a dictionary
    row = df.iloc[0].to_dict()

    # Extract a unique identifier for the document from the "time_numeric" field
    doc_id = row["time_numeric"]

    # Update the document in Elasticsearch; if it doesn't exist, insert it (upsert behavior)
    es.update(index=index, id=doc_id, body={"doc": row, "doc_as_upsert": True})

    # Call a function to check for None values in the inserted document
    return check_none_values(doc_id, index)  # This function should be defined to validate the inserted data


def check_none_values(current_timestamp, index):
    """
    Checks if the newly inserted document in Elasticsearch contains None values.
    
    Parameters:
    current_timestamp (int/str): The unique ID (timestamp) of the document in Elasticsearch.
    index (str): The name of the Elasticsearch index.

    Returns:
    list: If the document is valid, it returns a list from `prediction_enricher`, otherwise an empty list.
    """

    # Retrieve the document from Elasticsearch using the provided index and document ID (timestamp)
    response = es.get(index=index, id=current_timestamp)
    
    # Extract the document data from the response
    new_document = response["_source"]

    # Check if the document contains too few fields (possibly due to missing/None values)
    if len(new_document) < 10:  
        print("Error: Document contains None values. Aborting this step.")
        return []  # Return an empty list to indicate failure
    
    else:
        print("Well Done")  # Success message if the document is complete
        
        # Call the prediction_enricher function to further process the valid document
        previous_items = prediction_enricher(new_document, current_timestamp, index)  
        
        return previous_items  # Return the processed data
        
            
def prediction_enricher(new_document, current_timestamp, index):
    """
    Retrieves the last three documents from Elasticsearch that have a timestamp earlier than the given timestamp.
    If three documents are found, it returns them along with the new document.
    
    Parameters:
    new_document (dict): The newly inserted document in Elasticsearch.
    current_timestamp (int/str): The unique timestamp of the new document.
    index (str): The Elasticsearch index name.

    Returns:
    list: A list containing the new document and the last three previous documents if they exist.
          Otherwise, returns an empty list if there are not enough documents.
    """

    # Define a query to retrieve the last three documents before the given timestamp
    query_last_three_items = {
        "size": 3,  # Retrieve up to 3 previous documents
        "query": {
            "range": {  # Get documents with a timestamp earlier than current_timestamp
                "time_numeric": {
                    "lt": current_timestamp  # "lt" means "less than"
                }
            }
        },
        "sort": [{"time_numeric": {"order": "desc"}}]  # Sort by timestamp in descending order (latest first)
    }

    # Execute the query on Elasticsearch
    response = es.search(index=index, body=query_last_three_items)

    # Extract the last three documents from the Elasticsearch response
    documents_last_three_items = [hit["_source"] for hit in response["hits"]["hits"]]

    # Check if exactly 3 documents were retrieved
    if len(documents_last_three_items) == 3:
        return [new_document, documents_last_three_items]  # Return new document + previous 3 items
    else:
        print("Not enough documents")  # Print an error message if there are fewer than 3 documents
        return []  # Return an empty list to indicate insufficient data

    
def insert_prediction(df, index):
    """
    Sends a feature set from the given DataFrame to an external prediction API, retrieves the prediction,
    determines a buy/sell signal, and updates the Elasticsearch index with the results.

    Parameters:
    df (DataFrame): The input DataFrame containing cryptocurrency data.
    index (str): The name of the Elasticsearch index where the data will be updated.

    Returns:
    None
    """

    # Extract the actual BTC closing price from the DataFrame
    df_BTC_close = df["BTC_close"]

    # Define the feature names to be used for the prediction
    feature_names = [
        "BTC_ETH_ratio", "BTC_price_change", "BTC_volatility", "BTC_volume", 
        "ETH_close", "ETH_price_change", "ETH_volatility", "ETH_volume", 
        "BTC_lag_1", "BTC_lag_3", "ETH_lag_1", "ETH_lag_3"
    ]

    # Select the relevant feature columns from the DataFrame
    df_prediction = df[feature_names]  

    # Convert the first row of the DataFrame into a dictionary for API consumption
    features_dict = df_prediction.iloc[0].to_dict()

    # Prepare the JSON payload for the prediction API request
    payload = {"features": features_dict}

    # Send the request to the external prediction API
    response = requests.post(API_URL, json=payload)  
    response_data = response.json()  # Extract the JSON response from the API

    # Extract the predicted BTC closing price from the response
    btc_prediction = float(response_data["BTC_close_prediction"])

    # Determine the buy/sell signal based on the predicted and actual BTC close price
    signal = decision_buy_sell(df_BTC_close, btc_prediction)

    print("signal_1")
    print(signal)

    print("type_signal_1")
    print(type(signal))


    # Update the Elasticsearch index with the new prediction and buy/sell signal
    es.update(
        index=index,
        id=int(df.iloc[0]["time_numeric"]),  # Convert timestamp to integer ID for Elasticsearch
        body={
            "doc": {
                "BTC_close_prediction": btc_prediction,  # Store predicted BTC close price
                "BTC_ETH_ratio": float(df.iloc[0]["BTC_ETH_ratio"]),  # Store BTC/ETH ratio
                "BTC_buy_sell_signal": signal # Store the buy/sell signal
            },      
            "doc_as_upsert": True  # Insert if the document doesn't exist, update if it does
        }
    )


def decision_buy_sell(df_BTC_close, btc_prediction):
    """
    Determines whether to generate a buy/sell signal based on the predicted BTC closing price.

    Parameters:
    df_BTC_close (float or Series): The actual BTC closing price from the DataFrame.
    btc_prediction (float): The predicted BTC closing price.

    Returns:
    bool: True if the predicted price is higher than the actual price (buy signal), 
          False otherwise (sell signal).
    """

    # Compare the predicted BTC closing price with the actual closing price.
    # If the prediction is higher than the actual price, return True (buy signal),
    # otherwise return False (sell signal).
    signal = (btc_prediction > df_BTC_close).iloc[0]
    print("signal")
    print(signal)

    print("type_signal")
    print(type(signal))

    return signal


