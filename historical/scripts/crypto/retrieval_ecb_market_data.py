import requests
import pandas as pd
from datetime import datetime
import load_to_elastic as load_to_elastic

# Neue Basis-URL für die ECB Data Portal API
base_url = "https://data-api.ecb.europa.eu/service"

# Aktualisierte Serie-Definition (IDs musst du eventuell prüfen)
ecb_series_dict = {
    "Long_Term_Interest_Rate": ("IRS", "M.I9.L.L40.CI.0000.EUR.N.Z"),
    "Inflation_HICP": ("ICP", "M.U2.N.000000.4.INX"),
    "Money_Supply_M3": ("BSI", "M.U2.Y.V.M30.X.4.U2.2300.Z01.E"),
    "EURUSD_Exchange_Rate": ("EXR", "D.USD.EUR.SP00.A"),
    "GDP_Real": ("MPD", "Q.U2.YER.P.W24.0000"),
    "Government_Bonds_10Y": ("FM", "M.U2.EUR.4F.BB.U2_10Y.YLD")
}

start_period = "2015-05-01"
end_period = "2016-06-01"

print(f"ECB API Base URL: {base_url}")

all_dfs = []

for name, (dataset, series_key) in ecb_series_dict.items():
    print('series_key_ecb')
    print(series_key)
    url = f"{base_url}/data/{dataset}/{series_key}?startPeriod={start_period}&endPeriod={end_period}&format=sdmx-json"
    print("url_dynamic")
    print(url)
    
    headers = {"Accept": "application/vnd.sdmx.data+json"}  # sdmx-json Format

    print(f"Fetching {name} from ECB API...")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_data = response.json()

        # Zugriff auf die Daten
        series = json_data["dataSets"][0]["series"]
        structure = json_data["structure"]["dimensions"]["observation"][0]["values"]

        if not series:
            print(f"No series found for {name}.")
            continue

        series_data = list(series.values())[0]
        observations = series_data.get("observations", {})

        # Zeitachsen-Information holen
        dates = [entry['id'] for entry in structure]

        time_indices = [dates[int(idx)] for idx, obs in observations.items() if obs[0] is not None]
        values = [obs[0] for obs in observations.values() if obs[0] is not None]

        # DataFrame aufbauen
        df = pd.DataFrame({name: values}, index=pd.to_datetime(time_indices))

        print("df")
        print(df.head(10))
        df.index.name = "date"
        all_dfs.append(df)

    else:
        print(f"Failed to fetch {name}: {response.status_code}")
        print(response.text)  # Ausgabe der Fehlermeldung

# Zusammenfügen
if all_dfs:

    combined_df = pd.concat(all_dfs, axis=1).sort_index()

    # Final cleaning
    #combined_df["date"] = pd.to_datetime(combined_df["date"], errors="coerce")
    combined_df.sort_values("date", inplace=True)
    #combined_df.reset_index(drop=True, inplace=True)

    for col in combined_df.columns:
        if col != "date":
            combined_df[col] = pd.to_numeric(combined_df[col], errors="coerce").astype("float64")

    combined_df = combined_df.where(pd.notnull(combined_df), None)

    print("combined_df")
    print(combined_df)

    
    combined_df.to_csv("ecb_macro_data.csv")
    print("EZB-Daten gespeichert als ecb_macro_data.csv")

    # save to elastic 
    load_to_elastic.insert_ecb_data_elasticsearch(combined_df, "ecbmarket")
else:
    print("Keine EZB-Daten verfügbar.")

