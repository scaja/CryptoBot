#! /usr/bin/python
from elasticsearch import Elasticsearch #, helpers
import joblib
import pandas as pd

# Connection to the cluster
es = Elasticsearch(hosts = "http://@localhost:9200")

mapping = {
    "mappings": {
        "properties": {
            "timestamp": {"type": "date", "null_value": None},
            "BTC_close": {"type": "float", "null_value": None},
            "BTC_volume": {"type": "float", "null_value": None},
            "ETH_close": {"type": "float", "null_value": None},
            "ETH_volume": {"type": "float", "null_value": None},
            "BTC_price_change": {"type": "float", "null_value": None},
            "ETC_price_change": {"type": "float", "null_value": None},
            "BTC_volatility": {"type": "float", "null_value": None},
            "ETC_volatility": {"type": "float", "null_value": None},
            "BTC_ETC_ratio": {"type": "float", "null_value": None},
            "BTC_close_prediction": {"type": "float", "null_value": None},
            "time_numeric": {"type": "long", "null_value": None}
        }
    }
}

def insert_elastic_search(df, index):
    print("df", df)
  
    # Create the index with the mapping
    if not es.indices.exists(index=index):
        es.indices.create(index=index, body=mapping)

    row = df.iloc[0].to_dict()
    print("row", row)
  
    doc_id = row["time_numeric"]
    print("doc_id", doc_id)


    es.update(index=index, id=doc_id, body={"doc": row, "doc_as_upsert": True})

    print("after update")

    return check_none_values(doc_id, index)


def check_none_values(current_timestamp, index):
  
    response = es.get(index=index, id=current_timestamp)
    new_document = response["_source"]

    print("new_document", new_document)
   
    if len(new_document) < 10:  
        print("Error: Document contains None values. Aborting this step.")
        return []
    else:
        print("Well Done")
        previous_items = prediction_enricher(new_document, current_timestamp, index)
        return previous_items
        
            
def prediction_enricher(new_document, current_timestamp, index):
    
    query_last_three_items = {
        "size": 3,
        "query": {
            "range": {
                "time_numeric": {
                    "lt": current_timestamp
                }
            }
        },
        "sort": [{"time_numeric": {"order": "desc"}}]
    }

    response = es.search(index=index, body=query_last_three_items)

    print("response", response)

    documents_last_three_items = [hit["_source"] for hit in response["hits"]["hits"]]

    print("documents_last_three_items", documents_last_three_items)

    if len(documents_last_three_items) == 3:
        return [new_document, documents_last_three_items]
    else:
        print("Not enought documents")
        return []
    
def insert_prediction(df, index):

    model_path = "/home/lj/Desktop/DataScientest/CryptoBot/models/crypto_model.joblib"
    model = joblib.load(model_path)
 
    feature_names = [
        "BTC_ETH_ratio", "BTC_price_change", "BTC_volatility", "BTC_volume", 
        "ETH_close", "ETH_price_change", "ETH_volatility", "ETH_volume", 
        "BTC_lag_1", "BTC_lag_3", "ETH_lag_1", "ETH_lag_3"
    ]

    df_prediction = df[feature_names] 
    btc_close_pred = model.predict(df_prediction)

    print("btc_close_pred")
    print(btc_close_pred)

    print("df_prediction")
    print(df_prediction)

    print("index")
    print(index)

    print("time_numeric")
    print(df.iloc[0]["time_numeric"])

    print("BTC_ETH_ratio")
    print(df.iloc[0]["BTC_ETH_ratio"])
    
        
    es.update(
        index=index,
        id=int(df.iloc[0]["time_numeric"]),
        body={
            "doc": {"BTC_close_prediction": float(btc_close_pred[0]),
                    "BTC_ETH_ratio": float(df.iloc[0]["BTC_ETH_ratio"])},
            "doc_as_upsert": True
        }
    )

    return btc_close_pred

