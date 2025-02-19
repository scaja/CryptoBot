#!/bin/bash

# Setze PYTHONPATH dynamisch für Spark
export PYTHONPATH=$(find "$SPARK_HOME/python/lib/" -name "*.zip" | tr '\n' ':')

# Starte das Retrieval-Skript
python3 /historical/scripts/retrieval_script.py
python3 /historical/regression/ml_regression.py