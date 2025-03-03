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

# prepare vector assembler
feature_names = [
    "BTC_ETH_ratio", "BTC_price_change", "BTC_volatility", "BTC_volume", 
    "ETH_close", "ETH_price_change", "ETH_volatility", "ETH_volume", 
    "BTC_lag_1", "BTC_lag_3", "ETH_lag_1", "ETH_lag_3"
]

vector_assembler = VectorAssembler(inputCols=feature_names, outputCol="independent_features")

# load scaler 
model_path_scaler = "/app/data/scaler_pyspark"
scaler_model = MinMaxScalerModel.load(model_path_scaler)

# load regression
model_path_regressor = "/app/data/regressor_pyspark"
loaded_regressor = LinearRegressionModel.load(model_path_regressor)

try:
    loaded_regressor = LinearRegressionModel.load(model_path_regressor)
    model_loaded = True
except Exception as e:
    model_loaded = False
    load_error = str(e)

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

        # transform input data to spark dateframe
        df_prediction = pd.DataFrame([list(data.features.values())], columns=feature_names) 
        df_prediction_spark = spark.createDataFrame(df_prediction)

        # transform numbers to vectors
        df_prediction_spark = vector_assembler.transform(df_prediction_spark)
        
        # transform vector to 0 to 1 range
        df_prediction_scaled = scaler_model.transform(df_prediction_spark)
        df_prediction_scaled.show(truncate=False)

        # recieve prediction from model
        predictions = loaded_regressor.transform(df_prediction_scaled)
        prediction = predictions.select("prediction").collect() 
        prediction_value = prediction[0]["prediction"]

        #return prediction
        return {"BTC_close_prediction": prediction_value}
    except Exception as e:
        return {"error": str(e)}
