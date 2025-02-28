from pyspark.sql import SparkSession
from pyspark.sql.functions import lag
from pyspark.sql.window import Window
from pyspark.ml.feature import VectorAssembler, MinMaxScaler
from pyspark.ml.regression import LinearRegression
from elasticsearch import Elasticsearch
import os
from sklearn.linear_model import LinearRegression as SklearnLR
import joblib
import numpy as np

spark = SparkSession.builder.appName("BitcoinPricePrediction").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

es = Elasticsearch(hosts=["http://@elasticsearch:9200"])

response = es.search(index="historical", body={
    "query": {
        "match_all": {}
    },
    "size": 1000  
})

data = [hit["_source"] for hit in response["hits"]["hits"]]

spark = SparkSession.builder.appName("BitcoinPricePrediction").getOrCreate()

training_df = spark.createDataFrame(data)

window_spec = Window.orderBy("time_numeric")

training_df = training_df.withColumn("BTC_lag_1", lag("BTC_close", 1).over(window_spec))
training_df = training_df.withColumn("BTC_lag_3", lag("BTC_close", 3).over(window_spec))
training_df = training_df.withColumn("ETH_lag_1", lag("ETH_close", 1).over(window_spec))
training_df = training_df.withColumn("ETH_lag_3", lag("ETH_close", 3).over(window_spec))

training_df = training_df.na.drop()

training_df = training_df.orderBy("time_numeric")
split_index = int(training_df.count() * 0.8)
train_data = training_df.limit(split_index)
test_data = training_df.subtract(train_data)

print(f"Train: {train_data.count()} rows, Test: {test_data.count()} rows")

feature_cols = ["BTC_ETH_ratio",  "BTC_price_change" , "BTC_volatility", "BTC_volume", "ETH_close", "ETH_price_change", "ETH_volatility", "ETH_volume", "BTC_lag_1", "BTC_lag_3", "ETH_lag_1", "ETH_lag_3"]
featureassembler = VectorAssembler(inputCols=feature_cols,outputCol="independent_features")
train_data = featureassembler.transform(train_data)
test_data = featureassembler.transform(test_data)
print(train_data.show(5))

scaler = MinMaxScaler(inputCol="independent_features", outputCol="scaled_features")
scaler_model = scaler.fit(train_data)

train_data = scaler_model.transform(train_data)
test_data = scaler_model.transform(test_data)

train_data.show(2, truncate=False)
test_data.show(2, truncate=False)

finalized_train_data_output = train_data.select("scaled_features","BTC_close")
print(finalized_train_data_output.show(5))

regressor = LinearRegression(featuresCol="scaled_features", labelCol="BTC_close")
regressor = regressor.fit(finalized_train_data_output)

coefficients = regressor.coefficients.toArray()  
intercept = regressor.intercept   

sklearn_model = SklearnLR()
sklearn_model.coef_ = np.array(coefficients)  
sklearn_model.intercept_ = intercept 
sklearn_model.feature_names_in_ = np.array(feature_cols)

output_dir = "/historical/data"
os.makedirs(output_dir, exist_ok=True)

# save scaler
file_to_save_scaler = os.path.join(output_dir, "scaler_pyspark")
scaler_model.write().overwrite().save(file_to_save_scaler)

# save model in pyspark format
file_to_save_regressor = os.path.join(output_dir, "regressor_pyspark")
regressor.write().overwrite().save(file_to_save_regressor)

# save model in joblib format
file_path = os.path.join(output_dir, "crypto_model.joblib")
joblib.dump(sklearn_model, file_path)

os.chmod(file_path, 0o777)

print(f"File saved to: {file_path}")