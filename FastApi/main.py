from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

app = FastAPI()

model_path = "/app/data/crypto_model.joblib"

try:
    model = joblib.load(model_path)
    model_loaded = True
except Exception as e:
    model_loaded = False
    load_error = str(e)

model = joblib.load(model_path)
feature_names = [
    "BTC_ETH_ratio", "BTC_price_change", "BTC_volatility", "BTC_volume", 
    "ETH_close", "ETH_price_change", "ETH_volatility", "ETH_volume", 
    "BTC_lag_1", "BTC_lag_3", "ETH_lag_1", "ETH_lag_3"
]

@app.get("/health")
def health_check():
    """Überprüft den API- und Modellstatus."""
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
       
        input_data = pd.DataFrame([list(data.features.values())], columns=feature_names) 
        btc_close_pred = model.predict(input_data)
        
        return {"BTC_close_prediction": btc_close_pred[0]}
    except Exception as e:
        return {"error": str(e)}
