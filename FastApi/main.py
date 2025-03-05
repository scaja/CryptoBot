from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml.feature import MinMaxScalerModel, VectorAssembler
from pyspark.ml.regression import LinearRegressionModel

# Initialize FastAPI application
app = FastAPI()

# Initialize Spark session with memory configuration
spark = SparkSession.builder \
    .appName("FastAPI-Spark") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

# Prepare the feature vector assembler for machine learning model
# These are the input features used for the prediction model
feature_names = [
    "BTC_ETH_ratio", "BTC_price_change", "BTC_volatility", "BTC_volume", 
    "ETH_close", "ETH_price_change", "ETH_volatility", "ETH_volume", 
    "BTC_lag_1", "BTC_lag_3", "ETH_lag_1", "ETH_lag_3"
]

# VectorAssembler is used to combine multiple columns into a single vector column
vector_assembler = VectorAssembler(inputCols=feature_names, outputCol="independent_features")

# Load the MinMaxScaler model (scales data to the range [0,1])
model_path_scaler = "/app/data/scaler_pyspark"
scaler_model = MinMaxScalerModel.load(model_path_scaler)

# Load the pre-trained regression model
model_path_regressor = "/app/data/regressor_pyspark"
try:
    # Try to load the linear regression model
    loaded_regressor = LinearRegressionModel.load(model_path_regressor)
    model_loaded = True  # Flag indicating the model has been loaded successfully
except Exception as e:
    model_loaded = False  # Flag indicating the model failed to load
    load_error = str(e)  # Capture the error message if loading fails

# Health check endpoint to check if the API and model are working fine
@app.get("/health")
def health_check():
    """Checks the health of the API and if the model is loaded correctly."""
    return {
        "status": "healthy",  # API is healthy
        "model_loaded": model_loaded,  # Boolean indicating if the model is loaded
        "error": load_error if not model_loaded else None  # If model is not loaded, return error message
    }

# Prediction input model using Pydantic for input validation
class PredictionInput(BaseModel):
    features: dict  # Dictionary containing the feature values for prediction

# Prediction endpoint to receive the input features and return the predicted value
@app.post("/predict")
def predict(data: PredictionInput):
    try:
        # Convert the input dictionary to a Pandas DataFrame
        df_prediction = pd.DataFrame([list(data.features.values())], columns=feature_names)
        
        # Convert the Pandas DataFrame to a Spark DataFrame
        df_prediction_spark = spark.createDataFrame(df_prediction)

        # Use VectorAssembler to transform the input features into a single feature vector
        df_prediction_spark = vector_assembler.transform(df_prediction_spark)
        
        # Apply MinMaxScaler to scale the features to the range [0,1]
        df_prediction_scaled = scaler_model.transform(df_prediction_spark)
        
        # Show the transformed and scaled DataFrame (for debugging purposes)
        df_prediction_scaled.show(truncate=False)

        # Use the loaded regression model to make a prediction
        predictions = loaded_regressor.transform(df_prediction_scaled)
        
        # Collect the prediction result
        prediction = predictions.select("prediction").collect()
        
        # Extract the predicted value (BTC close price prediction)
        prediction_value = prediction[0]["prediction"]

        # Return the prediction result as a JSON response
        return {"BTC_close_prediction": prediction_value}
    
    except Exception as e:
        # If any error occurs, return the error message
        return {"error": str(e)}
