#! /usr/bin/python
from elasticsearch import Elasticsearch, helpers
import pandas as pd

# Connection to the cluster
es = Elasticsearch(hosts = "http://@elasticsearch:9200")

def insert_elastic_search(df, index):

    print("df_klines")
    print(df)
  
    mapping = {
        "mappings": {
            "properties": {
                "timestamp": {"type": "date", "format": "epoch_millis"},
                "datetime": {"type": "date"},  # ISO-formatierte Zeit (von pandas)
                "symbol": {"type": "keyword"},

                # Kline-Daten
                "open": {"type": "float"},
                "high": {"type": "float"},
                "low": {"type": "float"},
                "close": {"type": "float"},
                "volume": {"type": "float"},
                "close_time": {"type": "date", "format": "epoch_millis"},
                "quote_asset_volume": {"type": "float"},
                "number_of_trades": {"type": "integer"},
                "taker_buy_base_asset_volume": {"type": "float"},
                "taker_buy_quote_asset_volume": {"type": "float"},
                "ignore": {"type": "float"},
                
                # Technische Indikatoren
                "sma_20": {"type": "float"},
                "ema_20": {"type": "float"},
                "rsi": {"type": "float"},
                "macd": {"type": "float"},
                
                # Volatilitätsmetriken
                "bb_width": {"type": "float"},
                "bb_high": {"type": "float"},
                "bb_low": {"type": "float"}
            }
        }
    }

    print("mapping")
    print(mapping)

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


def insert_fred_data_to_elasticsearch(df, index):

    print("index_fred")
    print(df)

    #print("to_json")

    #print(df.to_json(orient="records"))

    

    mapping = {
        "mappings": {
            "properties": {
                "date": { "type": "date"},
                "Fed_Funds_Rate": { "type": "float" },
                "Reverse_Repo_Rate": { "type": "float" },
                "Treasury_Bill_3M": { "type": "float" },
                "Consumer_Price_Index": { "type": "float" },
                "PCE_Price_Index": { "type": "float" },
                "Core_Inflation_Rate": { "type": "float" },
                "Unemployment_Rate": { "type": "float" },
                "Nonfarm_Payrolls": { "type": "float" },
                "GDP_Nominal": { "type": "float" },
                "GDP_Real": { "type": "float" },
                "Consumer_Sentiment": { "type": "float" },
                "Money_Supply_M2": { "type": "float" },
                "VIX_Index": { "type": "float" }
            }
        }
    }

    print("mapping_fred")
    print(mapping)

    # Create the index with the mapping
    if not es.indices.exists(index=index):
        es.indices.create(index=index, body=mapping)
   
    # Bulk import the data
    def bulk_data_generator(df):
        for _, row in df.iterrows():
            yield {
                "_index": index,
                "_source": row.dropna().to_dict()
            }

    helpers.bulk(es, bulk_data_generator(df)) 



def insert_ecb_data_elasticsearch(df, index):
    """
    Insertiert EZB-Daten (DataFrame mit 'date' & 'value') in Elasticsearch.

    :param df: Pandas DataFrame mit Spalten 'date', 'value' (+ optional weitere)
    :param index: Zielindex in Elasticsearch (z.B. 'us_market' oder 'ecb_data')
    """

    print("index")
    print(index)

    print("df")
    print(df)

    mapping = {
        "mappings": {
            "properties": {
                "date": {
                    "type": "date"
                },
                "Long_Term_Interest_Rate": {
                    "type": "float"            # Long_Term_Interest_Rate
                },
                "Inflation_HICP": {
                    "type": "float"            # Inflation_HICP
                },
                "Money_Supply_M3": {
                    "type": "float"            # Money_Supply_M3
                },
                "EURUSD_Exchange_Rate": {
                    "type": "float"            # EURUSD_Exchange_Rate
                },
                "GDP_Real": {
                    "type": "float"            # GDP_Real
                },
                "Government_Bonds_10Y": {
                    "type": "float"            # Government_Bonds_10Y
                }
            }
        }
    }



    print("mapping_ecb")
    print(mapping)

    # Create the index with the mapping
    if not es.indices.exists(index=index):
        es.indices.create(index=index, body=mapping)
   
    # Bulk import the data
    def bulk_data_generator(df):
        for _, row in df.iterrows():
            yield {
                "_index": index,
                "_source": row.dropna().to_dict()
            }

    helpers.bulk(es, bulk_data_generator(df)) 

def insert_wbdata_elasticsearch(df, index):
    """
    Insertiert World Bank Daten (z. B. GDP, Inflation etc.) in Elasticsearch.

    Erwartet Spalten im DataFrame wie:
    - 'date': Zeitstempel im ISO-Format
    - 'country': Ländername oder Code
    - 'indicator_name': Name des Indikators (z. B. GDP, Inflation, etc.)
    - 'value': Messwert

    :param df: Pandas DataFrame mit World Bank Daten
    :param index: Zielindex in Elasticsearch (z.B. 'wb_macro_data')
    """

    mapping = {
        "mappings": {
            "properties": {
                "date": {"type": "date"},                   # ISO 8601 Zeitformat
                "country": { "type": "keyword" },
                "GDP_growth": { "type": "float" },
                "Inflation": { "type": "float" },
                "Debt_GDP_ratio": { "type": "float" },
                "Exports": { "type": "float" },
                "Imports": { "type": "float" },
                "Unemployment_rate": { "type": "float" }
            }
        }
    }

    # Index erstellen, wenn noch nicht vorhanden
    if not es.indices.exists(index=index):
        es.indices.create(index=index, body=mapping)

    # Generator für Bulk-Einträge
    def bulk_generator(df):
        for _, row in df.iterrows():
            doc = row.to_dict()
            yield {
                "_index": index,
                "_source": doc
            }

    # Daten einfügen
    helpers.bulk(es, bulk_generator(df))
    print(f"✅ {len(df)} WB-Dokumente in Elasticsearch eingefügt (Index: {index})")


def insert_order_data_elasticsearch(df, index):
    """
    Insertiert World Bank Daten (z. B. GDP, Inflation etc.) in Elasticsearch.

    Erwartet Spalten im DataFrame wie:
    - 'date': Zeitstempel im ISO-Format
    - 'country': Ländername oder Code
    - 'indicator_name': Name des Indikators (z. B. GDP, Inflation, etc.)
    - 'value': Messwert

    :param df: Pandas DataFrame mit World Bank Daten
    :param index: Zielindex in Elasticsearch (z.B. 'wb_macro_data')
    """

    mapping = {
        "mappings": {
            "properties": {
                "date": {"type": "date"},                   # ISO 8601 Zeitformat
                "country": { "type": "keyword" },
                "GDP_growth": { "type": "float" },
                "Inflation": { "type": "float" },
                "Debt_GDP_ratio": { "type": "float" },
                "Exports": { "type": "float" },
                "Imports": { "type": "float" },
                "Unemployment_rate": { "type": "float" }
            }
        }
    }

    # Index erstellen, wenn noch nicht vorhanden
    if not es.indices.exists(index=index):
        es.indices.create(index=index, body=mapping)

    # Generator für Bulk-Einträge
    def bulk_generator(df):
        for _, row in df.iterrows():
            doc = row.to_dict()
            yield {
                "_index": index,
                "_source": doc
            }

    # Daten einfügen
    helpers.bulk(es, bulk_generator(df))
    print(f"✅ {len(df)} WB-Dokumente in Elasticsearch eingefügt (Index: {index})")