#!/bin/bash

# Dynamically set the PYTHONPATH for Spark
# This command finds all .zip files in the SPARK_HOME/python/lib directory and
# concatenates them with colons (:) to set the PYTHONPATH, which helps Spark find
# Python libraries.
export PYTHONPATH=$(find "$SPARK_HOME/python/lib/" -name "*.zip" | tr '\n' ':')

# Start the main script with Uvicorn
# The 'uvicorn' command runs an ASGI application. 
# The '--host 0.0.0.0' option binds the server to all network interfaces, 
# making it accessible from any IP address.
# The '--port 8000' option sets the port number to 8000 for the application.
# The '--reload' option enables the automatic reloading of the application during development, 
# so changes in the code are automatically reflected without restarting the server.
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
