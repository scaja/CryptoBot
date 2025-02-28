from fastapi import FastAPI
from pydantic import BaseModel
#import joblib
#import numpy as np
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml.feature import MinMaxScalerModel, VectorAssembler
from pyspark.ml.regression import LinearRegressionModel


app = FastAPI()

spark = SparkSession.builder \
    .appName("FastAPI-Spark") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

print("spark")
print(spark)

#model_path = "/app/data/crypto_model.joblib"
model_path_regressor = "/app/data/regressor_pyspark"
model_path_scaler = "/app/data/scaler_pyspark"

print("model_path_regressor")
print(model_path_regressor)

# try:
#     model = joblib.load(model_path)
#     model_loaded = True
# except Exception as e:
#     model_loaded = False
#     load_error = str(e)

try:
    loaded_regressor = LinearRegressionModel.load(model_path_regressor)
    model_loaded = True
except Exception as e:
    model_loaded = False
    load_error = str(e)


#model = joblib.load(model_path)
loaded_regressor = LinearRegressionModel.load(model_path_regressor)
scaler_model = MinMaxScalerModel.load(model_path_scaler)

feature_names = [
    "BTC_ETH_ratio", "BTC_price_change", "BTC_volatility", "BTC_volume", 
    "ETH_close", "ETH_price_change", "ETH_volatility", "ETH_volume", 
    "BTC_lag_1", "BTC_lag_3", "ETH_lag_1", "ETH_lag_3"
]

vector_assembler = VectorAssembler(inputCols=feature_names, outputCol="features")

@app.get("/health")
def health_check():
    """checks the api health."""
    return {
        "status": "healthy",
        "model_loaded": model_loaded,
        "error": load_error if not model_loaded else None
    }

class PredictionInput(BaseModel):
    features: dict

@app.post("/predict")
def predict(data: PredictionInput):
    try:

        print("hello")

        df_prediction = pd.DataFrame([list(data.features.values())], columns=feature_names) 

        print("df_prediction")
        print(df_prediction)

        df_prediction_spark = vector_assembler.transform(df_prediction)
        
        print("df_prediction_spark")
        print(df_prediction_spark)

        df_prediction_scaled = scaler_model.transform(df_prediction_spark)

        print("df_prediction_scaled")
        print(df_prediction_scaled)

        predictions = loaded_regressor.transform(df_prediction_scaled)
    
        predictions.select("BTC_close_prediction").show(5, truncate=False)

        print(predictions)
       
        
        # print("input_data")
        # print(input_data)
        # btc_close_pred = model.predict(input_data)

        # print("btc_close_pred")
        # print(btc_close_pred)

        return {"BTC_close_prediction": predictions[0]}
    except Exception as e:
        return {"error": str(e)}
