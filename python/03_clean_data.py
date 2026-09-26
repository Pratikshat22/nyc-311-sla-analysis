import pandas as pd

# Load raw data
df = pd.read_csv("data/raw/311_raw_data.csv", low_memory=False)

# Keep only the columns we actually need
columns_to_keep = [
    "unique_key", "created_date", "closed_date", "agency", "agency_name",
    "complaint_type", "descriptor", "location_type", "incident_zip",
    "borough", "community_board", "status", "resolution_description",
    "resolution_action_updated_date", "open_data_channel_type",
    "latitude", "longitude"
]
df = df[columns_to_keep]

# Convert date columns to proper datetime format
df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce")
df["closed_date"] = pd.to_datetime(df["closed_date"], errors="coerce")

# Calculate resolution time in hours (our key metric)

df["resolution_hours"] = (df["closed_date"] - df["created_date"]).dt.total_seconds() / 3600
# Check how many records have negative resolution time (data quality issue)
negative_count = (df["resolution_hours"] < 0).sum()
print(f"Records with negative resolution time: {negative_count}")

# These are logically impossible (closed before created) — treat as bad data, remove
df = df[(df["resolution_hours"].isna()) | (df["resolution_hours"] >= 0)]
# Drop rows where created_date itself is missing/broken (can't analyze without it)
df = df.dropna(subset=["created_date"])

# Clean up text fields: consistent uppercase, strip whitespace
text_columns = ["agency", "agency_name", "complaint_type", "descriptor",
                 "borough", "status", "open_data_channel_type"]
for col in text_columns:
    df[col] = df[col].astype(str).str.strip().str.upper()

# Save cleaned data
df.to_csv("data/processed/311_cleaned_data.csv", index=False)

print("Cleaning complete.")
print("Final shape:", df.shape)
print()
print("Resolution hours summary:")
print(df["resolution_hours"].describe())