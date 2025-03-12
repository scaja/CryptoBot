# Binance Historical Data Regression and Prediction

## Overview

This project is designed to download historical market data from Binance via their API. Once the historical data is fetched, a regression model is built based on the data. The model is then saved for future use. 

In addition, a streaming process can be initiated, which loads the saved model and makes real-time predictions based on incoming streaming data. The predictions are used to make buy/sell decisions for cryptocurrencies.

## Features

1. **Historical Data Download:**
   - Fetches historical data from Binance using their API.
   - The data includes market data such as open, high, low, close prices, and volume for selected symbols like BTC/USDT and ETH/BTC.

2. **Data Preprocessing:**
   - The raw historical data is processed to calculate relevant features such as price changes, volatility, and ratios between different cryptocurrency pairs.

3. **Model Building:**
   - Using the preprocessed historical data, a regression model is built to predict the closing price of a selected cryptocurrency pair (e.g., BTC/USDT).
   - The model is trained using machine learning techniques and then saved for future predictions.

4. **Model Deployment & Prediction:**
   - The saved regression model can be loaded for making predictions.
   - A streaming process can be started, where real-time market data is processed, and the model generates predictions.
   - The prediction is used to make a buy or sell decision based on the predicted price.

5. **Prediction-Driven Decision Making:**
   - The system can trigger buy/sell decisions by analyzing the prediction from the model.

## Technologies Used

- **Binance API**: For downloading historical data and real-time market data.
- **Python**: For data processing, model building, and prediction.
- **FastAPI**: For serving predictions via a web API.
- **Elasticsearch**: For storing historical data and making it accessible for further analysis.
- **Docker**: For containerizing the services and ensuring easy deployment.
- **PySpark**: For distributed data processing in case of large datasets.
- **Scikit-learn**: For building regression models.

## Project Workflow

1. **Step 1 - Historical Data Retrieval:**
   - Use the Binance API to fetch historical market data.
   - Data is processed to compute relevant features, such as percentage changes, volatility, and asset ratios.

2. **Step 2 - Model Training:**
   - The preprocessed data is used to train a regression model (e.g., Linear Regression).
   - The trained model is saved for future use.

3. **Step 3 - Model Loading & Prediction:**
   - The saved model is loaded and used to predict the closing price based on real-time data.
   - The predictions are analyzed and used to make buy/sell decisions.

4. **Step 4 - Streaming Data:**
   - The system listens to real-time data from Binance, processes it, and uses the model to make predictions.
   - Actions can be triggered based on the predictions, such as buy or sell orders.

## Requirements

To run this project, you will need the following tools and libraries:

- **Docker**: To run the containerized services.
- **Python 3.8+**: Required for running the backend code.
- **Binance API Key**: You will need a valid Binance API key and secret for accessing the historical and real-time market data.

Install the required Python packages using the following command:



## Running the Project

1. **Set up the environment**: 
   - Create a `.env` file and add your Binance API credentials:
     ```env
     BINANCE_API_KEY=<your-api-key>
     BINANCE_API_SECRET=<your-api-secret>
     ```

2. **Start the Docker containers**:
   - Use the following command to start all services:
     ```bash
     docker-compose up --build
     ```

3. **Access FastAPI**:
   - Once the containers are running, the FastAPI service will be available at `http://localhost:8000`. You can access the `/predict` endpoint to get predictions based on real-time data.

4. **Start the streaming process**:
   - The streaming service will automatically use the regression model to predict and make decisions based on live data from Binance.

## Project Structure

- **`/historical/`**: Contains scripts for downloading, preprocessing the data, and training the regression model.
- **`/FastApi/`**: Contains the FastAPI app to serve predictions via an API.
- **`/streaming/`**: Contains scripts for handling real-time streaming data and making predictions.
- **`/models/`**: Directory for storing saved models (regression model, scaler).
- **`/docker-compose.yml`**: Configuration file for running the services with Docker.

## Conclusion

This project leverages Binance’s API to create a data-driven model that can predict cryptocurrency price movements and make buy/sell decisions based on those predictions. The system is designed to handle both historical data for model training and real-time data for predictions, offering a powerful tool for cryptocurrency trading automation.

Feel free to explore, modify, and enhance the project as needed!

# CryptoBot

<details>
<summary>setup vm</summary>

## add new repository in git browser

git clone https://github.com/scaja/CryptoBot.git  
cd CryptoBot  
git add .gitignore  
git commit -m "add gitignore"  
git push  
source myenv/bin/activatesource  


## virtual environment

sudo apt-get update  
sudo apt-get install python3.8-venv --fix-missing  
python3 -m venv myenv  
source myenv/bin/activate  


upgrade pip  
python3 -m pip install --upgrade pip  


## Create Kernel

pip3 install ipykernel  
python3 -m ipykernel install --user --name='vscode'  


## Start Jupiter

pip install notebook ipython  
jupyter notebook  
Install extensions also as host ssh  
restart VSCODE manuelly  

</details>

<details>
<summary>install packages</summary>

pip install pandas  
pip install python-dotenv  
pip install python-binance  
pip install websocket-client
pip install elasticsearch

</details>

<details>
<summary>unittest</summary>

python -m unittest discover

</details>

<details>
<summary>pyspark</summary>

## install Java

sudo apt update
sudo apt install openjdk-8-jre-headless -y
sudo apt install openjdk-8-jdk-headless -y

## install env

sudo apt install python3.8-venv -y

python3 -m venv .venv
. .venv/bin/activate
pip install notebook

## install spark

wget https://dst-de.s3.eu-west-3.amazonaws.com/pyspark_fr/spark.tgz

tar xzvf spark.tgz
sudo mv spark-3.5.0-bin-hadoop3/ /opt/spark

## set environment variable

export SPARK_HOME=/opt/spark
export PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH
export PYTHONPATH=$(ZIPS=("$SPARK_HOME"/python/lib/*.zip); IFS=:; echo "${ZIPS[*]}"):$PYTHONPATH

## 

rm spark.tgz
sed -i 's/rootLogger.level = info/rootLogger.level = error/' /opt/spark/conf/log4j2.properties.template
mv /opt/spark/conf/log4j2.properties.template /opt/spark/conf/log4j2.properties

</details>

<details>
<summary>commands</summary>

docker compose -f docker-compose-bot.yml up --build --force-recreate --renew-anon-volumes
docker compose -f docker-compose.yml up --build --force-recreate --renew-anon-volumes

</details>

docker compose -f docker-compose.yml up --build --force-recreate --renew-anon-volumes
docker compose -f docker-compose-bot.yml up --build --force-recreate --renew-anon-volumes

http://localhost:5601/app/dev_tools#/console


http://localhost:8000/docs#/default/health_check_health_get

curl -X 'GET' \
  'http://localhost:8000/health' \
  -H 'accept: application/json'

{
  "features": {
    "BTC_ETH_ratio": 42.76210676634886,
    "BTC_price_change": 0.00016184357266117022,
    "BTC_volatility": 43.33999999999651,
    "BTC_volume": 55.40676,
    "ETH_close": 1904.72,
    "ETH_price_change": 0.0012879349408864385,
    "ETH_volatility": 3.2799999999999727,
    "ETH_volume": 695.6582,
    "BTC_lag_1": 81445.99,
    "BTC_lag_3": 81422.88,
    "ETH_lag_1": 1902.06,
    "ETH_lag_3": 1896.47
  }
}

GET streaming/_search
{
  "query": {
    "match_all": {}
  }
}

DELETE streaming

GET streaming/_search
{
  "query": {
    "match": {
      "time_numeric": 1740490740
    }
  }
}

GET historical/_search
{
  "query": {
    "match_all": {}
  }
}