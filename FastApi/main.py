from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

model = joblib.load("crypto_model.joblib")

class PredictionRequest(BaseModel):
    features: list

app = FastAPI()

@app.post("/predict")
def predict(request: PredictionRequest):
    features = np.array(request.features).reshape(1, -1)
    prediction = model.predict(features)
    return {"prediction": prediction[0]}