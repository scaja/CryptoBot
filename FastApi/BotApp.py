# app.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib  # or pickle if you prefer
import numpy as np

# Load your trained model
model = joblib.load("crypto_model.joblib")

# Define request schema
class PredictionRequest(BaseModel):
    features: list

app = FastAPI()

@app.post("/predict")
def predict(request: PredictionRequest):
    # Convert input data into the right format
    features = np.array(request.features).reshape(1, -1)
    prediction = model.predict(features)
    return {"prediction": prediction[0]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)