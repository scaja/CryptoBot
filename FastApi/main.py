from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

#model = joblib.load("../regression/crypto_model.joblib")

app = FastAPI()

# Modellpfad (bereits korrekt angegeben)
model_path = "/home/lj/Desktop/DataScientest/CryptoBot/regression/crypto_model.joblib"

# Modell laden
model = joblib.load(model_path)

# Feature-Namen
feature_names = [
    "BTC_ETH_ratio", "BTC_price_change", "BTC_volatility", "BTC_volume", 
    "ETH_close", "ETH_price_change", "ETH_volatility", "ETH_volume", 
    "BTC_lag_1", "BTC_lag_3", "ETH_lag_1", "ETH_lag_3"
]

@app.post("/predict")
def predict(features: dict):
    try:
        # Features als DataFrame formatieren
        input_data = pd.DataFrame([list(features.values())], columns=feature_names)
        
        # Vorhersage für BTC_close
        btc_close_pred = model.predict(input_data)
        
        return {"BTC_close_prediction": btc_close_pred[0]}
    except Exception as e:
        return {"error": str(e)}
