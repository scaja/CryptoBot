#!/bin/bash

# Dynamically set the PYTHONPATH for Spark by finding all .zip files in the Spark Python library directory
export PYTHONPATH=$(find "$SPARK_HOME/python/lib/" -name "*.zip" | tr '\n' ':')

# Start the retrieval script to fetch and preprocess historical data
python3 /historical/scripts/crypto/retrieval_klines_data.py

python3 /historical/scripts/crypto/retrieval_us_market_data.py

python3 /historical/scripts/crypto/retrieval_ecb_market_data.py

python3 /historical/scripts/crypto/retrieval_macro_economics_data.py

python3 /historical/scripts/crypto/retrieval_order_data.py

# Start the machine learning regression script to train and save the model
#python3 /historical/regression/ml_regression.py