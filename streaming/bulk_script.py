#! /usr/bin/python
from elasticsearch import Elasticsearch, helpers

def insert_elastic_search(df, index):
  
    # Connection to the cluster
    es = Elasticsearch(hosts = "http://@localhost:9200")

    # mapping
    mapping = {
        "mappings": {
            "properties": {
                "symbol": {"type": "text"},
                "price": { "type": "float"},
                "time": {"type": "date"}
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
