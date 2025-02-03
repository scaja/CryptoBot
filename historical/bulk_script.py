#! /usr/bin/python
from elasticsearch import Elasticsearch, helpers
#import csv
import pandas as pd

def insert_elastic_search(df, index):
  
    print(index)

    # Connection to the cluster
    es = Elasticsearch(hosts = "http://@localhost:9200")

    print(df)

    # mapping
    #mapping = {
        #"mappings": {
            #"properties": {
                #"symbol": {"type": "text"},
                #"price": { "type": "float"},
                #"time": {"type": "date"}
                #}
            #}
        #}
    
    mapping = {
        "mappings": {
            "properties": {
                "timestamp": {"type": "date"},
                "BTC_close": { "type": "float"},
                "BTC_volume": {"type": "float"},
                "BTC_volume": {"type": "float"},
                "ETH_close": {"type": "float"},
                "ETH_volume": {"type": "float"},
                "BTC_price_change": {"type": "float"},
                "ETC_price_change": {"type": "float"},
                "BTC_volatility": {"type": "float"},
                "ETC_volatility": {"type": "float"},
                "BTC_ETC_ratio": {"type": "float"}
                }
            }
        }

    # Create the index with the mapping
    if not es.indices.exists(index=index):
        es.indices.create(index=index, body=mapping)
   
    # Bulk import the data
    def bulk_data_generator(df):
        for _, row in df.iterrows():
            yield {
                "_index": index,
                "_source": row.to_dict()
            }

    helpers.bulk(es, bulk_data_generator(df)) 
