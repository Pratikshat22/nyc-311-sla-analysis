import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:Pratiksha@localhost/nyc311_sla")

df = pd.read_csv("data/processed/311_cleaned_data.csv", low_memory=False)
df["created_date"] = pd.to_datetime(df["created_date"])
df["closed_date"] = pd.to_datetime(df["closed_date"])

dim_agency = pd.read_sql("SELECT * FROM dim_agency", engine)
dim_complaint_type = pd.read_sql("SELECT * FROM dim_complaint_type", engine)
dim_location = pd.read_sql("SELECT * FROM dim_location", engine)
dim_date = pd.read_sql("SELECT * FROM dim_date", engine)
dim_date["full_date"] = pd.to_datetime(dim_date["full_date"])

dim_location_simple = dim_location[["location_id", "borough", "incident_zip", "community_board"]].drop_duplicates(
    subset=["borough", "incident_zip", "community_board"], keep="first"
)

df = df.merge(dim_agency, on=["agency", "agency_name"], how="left")
df = df.merge(dim_complaint_type, on=["complaint_type", "descriptor"], how="left")
df = df.merge(dim_location_simple, on=["borough", "incident_zip", "community_board"], how="left")

df["created_date_only"] = df["created_date"].dt.date
dim_date["date_only"] = dim_date["full_date"].dt.date
df = df.merge(
    dim_date[["date_id", "date_only"]].rename(columns={"date_id": "created_date_id"}),
    left_on="created_date_only", right_on="date_only", how="left"
)
df = df.drop(columns=["date_only"])

df["closed_date_only"] = df["closed_date"].dt.date
df = df.merge(
    dim_date[["date_id", "date_only"]].rename(columns={"date_id": "closed_date_id"}),
    left_on="closed_date_only", right_on="date_only", how="left"
)
df = df.drop(columns=["date_only"])

fact = df[[
    "unique_key", "agency_id", "complaint_type_id", "location_id",
    "created_date_id", "closed_date_id", "status", "open_data_channel_type",
    "resolution_hours"
]].rename(columns={"unique_key": "request_id"})

fact.to_sql("fact_service_requests", engine, if_exists="append", index=False, chunksize=5000)

print("Fact table loaded. Total rows:", len(fact))