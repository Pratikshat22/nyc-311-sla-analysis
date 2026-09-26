import pandas as pd
from sqlalchemy import create_engine

# --- Connection setup ---
# Replace 'ohmine' if your password is different
engine = create_engine("mysql+pymysql://root:Pratiksha@localhost/nyc311_sla")

# --- Load cleaned data ---
df = pd.read_csv("data/processed/311_cleaned_data.csv")
print("Loaded cleaned data:", df.shape)

# --- Build dim_agency ---
dim_agency = df[["agency", "agency_name"]].drop_duplicates().reset_index(drop=True)
dim_agency["agency_id"] = dim_agency.index + 1
dim_agency.to_sql("dim_agency", engine, if_exists="append", index=False)
print("dim_agency loaded:", dim_agency.shape)

# --- Build dim_complaint_type ---
dim_complaint_type = df[["complaint_type", "descriptor"]].drop_duplicates().reset_index(drop=True)
dim_complaint_type["complaint_type_id"] = dim_complaint_type.index + 1
dim_complaint_type.to_sql("dim_complaint_type", engine, if_exists="append", index=False)
print("dim_complaint_type loaded:", dim_complaint_type.shape)

# --- Build dim_location ---
dim_location = df[["borough", "incident_zip", "community_board", "latitude", "longitude"]].drop_duplicates().reset_index(drop=True)
dim_location["location_id"] = dim_location.index + 1
dim_location.to_sql("dim_location", engine, if_exists="append", index=False)
print("dim_location loaded:", dim_location.shape)

# --- Build dim_date (from created_date + closed_date, combined unique dates) ---
df["created_date"] = pd.to_datetime(df["created_date"])
df["closed_date"] = pd.to_datetime(df["closed_date"])

all_dates = pd.concat([df["created_date"], df["closed_date"]]).dropna().dt.date.unique()
dim_date = pd.DataFrame({"full_date": all_dates})
dim_date["full_date"] = pd.to_datetime(dim_date["full_date"])
dim_date["year"] = dim_date["full_date"].dt.year
dim_date["month"] = dim_date["full_date"].dt.month
dim_date["day"] = dim_date["full_date"].dt.day
dim_date["day_of_week"] = dim_date["full_date"].dt.day_name()
dim_date["is_weekend"] = dim_date["full_date"].dt.dayofweek >= 5
dim_date["quarter"] = dim_date["full_date"].dt.quarter
dim_date = dim_date.sort_values("full_date").reset_index(drop=True)
dim_date["date_id"] = dim_date.index + 1
dim_date.to_sql("dim_date", engine, if_exists="append", index=False)
print("dim_date loaded:", dim_date.shape)

print("All dimension tables loaded successfully.")