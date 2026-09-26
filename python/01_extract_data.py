import requests
import pandas as pd

url = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"

all_records = []
limit = 50000
offset = 0

where_clause = "created_date >= '2025-03-01T00:00:00'"

while True:
    params = {
        "$limit": limit,
        "$offset": offset,
        "$where": where_clause,
        "$order": "created_date"
    }

    response = requests.get(url, params=params)
    batch = response.json()

    if len(batch) == 0:
        break

    all_records.extend(batch)
    print(f"Pulled {len(all_records)} records so far...")

    offset += limit

df = pd.DataFrame(all_records)
df.to_csv("data/raw/311_raw_data.csv", index=False)

print("Done. Total records saved:", len(df))