import pandas as pd
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import load_to_elastic as load_to_elastic



load_dotenv()

# Define FRED indicators with their series IDs
fred_series = {
    "Fed_Funds_Rate": "FEDFUNDS",
    "Reverse_Repo_Rate": "RRPONTSYD",
    "Treasury_Bill_3M": "DTB3",
    "Consumer_Price_Index": "CPIAUCSL",
    "PCE_Price_Index": "PCEPI",
    "Core_Inflation_Rate": "CORESTICKM159SFRBATL",
    "Unemployment_Rate": "UNRATE",
    "Nonfarm_Payrolls": "PAYEMS",
    "GDP_Nominal": "GDP",
    "GDP_Real": "GDPC1",
    "Consumer_Sentiment": "UMCSENT",
    "Money_Supply_M2": "M2SL",
    "VIX_Index": "VIXCLS"
}

# Replace this with your own FRED API key
#FRED_API_KEY = os.getenv("FRED_API_KEY")
FRED_API_KEY = "b104e526082a5ed96354a2ab5aaa7b39"

# Define API endpoint and date range
base_url = "https://api.stlouisfed.org/fred/series/observations"
start_date = "2015-01-01"
end_date = datetime.today().strftime('%Y-%m-%d')

print("url_fred")
print(base_url)

# Function to fetch data for a single series
def fetch_fred_data(series_id):
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": end_date
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    observations = data.get("observations", [])
    return pd.DataFrame({
        "date": [obs["date"] for obs in observations],
        series_id: [obs["value"] for obs in observations]
    })

# Fetch and merge all data series
combined_df = pd.DataFrame()
for name, series_id in fred_series.items():
    df = fetch_fred_data(series_id)
    if combined_df.empty:
        combined_df = df
    else:
        combined_df = pd.merge(combined_df, df, on="date", how="outer")

# Final cleaning
combined_df["date"] = pd.to_datetime(combined_df["date"], errors="coerce")
combined_df.sort_values("date", inplace=True)
combined_df.reset_index(drop=True, inplace=True)

for col in combined_df.columns:
    if col != "date":
        combined_df[col] = pd.to_numeric(combined_df[col], errors="coerce").astype("float64")

combined_df = combined_df.where(pd.notnull(combined_df), None)


# Save to CSV
#combined_df.to_csv("fred_us_economic_data.csv", index=False)

# save to elastic 
load_to_elastic.insert_fred_data_to_elasticsearch(combined_df, "usmarket")