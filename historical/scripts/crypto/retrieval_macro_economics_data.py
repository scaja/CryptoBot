import wbdata
import pandas as pd
from datetime import datetime

import load_to_elastic as load_to_elastic

# Länder
countries = ['US', 'EMU', 'JP', 'KR', 'TR']

print("url_macro")
print(countries)

# Indikatoren (Key = WB-Code, Value = Klarname)
indicators = {
    'NY.GDP.MKTP.KD.ZG': 'GDP_growth',
    'FP.CPI.TOTL.ZG': 'Inflation',
    'GC.DOD.TOTL.GD.ZS': 'Debt_GDP_ratio',
    'NE.EXP.GNFS.CD': 'Exports',
    'NE.IMP.GNFS.CD': 'Imports',
    'SL.UEM.TOTL.ZS': 'Unemployment_rate'
}

# Zeitraum
start_date = datetime(2015, 1, 1)
end_date = datetime(2016, 12, 31)
date_range = (start_date, end_date)

# Daten abrufen
all_data = []

for indicator_code, indicator_name in indicators.items():
    print(f"🔄 Abrufe {indicator_name}...")
    data = wbdata.get_data(
        indicator=indicator_code,
        country=countries,
        date=date_range,
        freq='M',
        parse_dates=True
    )
    df = pd.DataFrame(data)
    df['country'] = df['country'].apply(lambda x: x['value'] if isinstance(x, dict) else x)
    df['indicator_name'] = indicator_name
    all_data.append(df)

# Kombinieren
combined_df = pd.concat(all_data)

# Aufbereitung
combined_df = combined_df.pivot_table(index=['date', 'country'], columns='indicator_name', values='value').reset_index()

# Speichern
#combined_df.to_csv("worldbank_macro_data.csv", index=False)
#print("✅ Daten gespeichert als 'worldbank_macro_data.csv'")

# save to elastic 
load_to_elastic.insert_ecb_data_elasticsearch(combined_df, "macro_economics")