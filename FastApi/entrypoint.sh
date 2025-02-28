#!/bin/bash

# Setze PYTHONPATH dynamisch für Spark
export PYTHONPATH=$(find "$SPARK_HOME/python/lib/" -name "*.zip" | tr '\n' ':')

# Starte das main script
#python3 /app/main.py
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload