#!/bin/bash

# Dynamically set the PYTHONPATH for Spark by finding all .zip files in the Spark Python library directory
export PYTHONPATH=$(find "$SPARK_HOME/python/lib/" -name "*.zip" | tr '\n' ':')

# Start the retrieval script to fetch and preprocess historical data
python3 /historical/scripts/retrieval_script.py

# Start the machine learning regression script to train and save the model
python3 /historical/regression/ml_regression.py