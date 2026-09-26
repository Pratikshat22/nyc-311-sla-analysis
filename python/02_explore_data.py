import pandas as pd

# Load the raw data we just extracted
df = pd.read_csv("data/raw/311_raw_data.csv")

print("Shape (rows, columns):", df.shape)
print()

print("Column names and data types:")
print(df.dtypes)
print()

print("Missing values per column:")
print(df.isnull().sum())
print()

print("Number of duplicate rows:", df.duplicated().sum())
print()

print("First 3 rows:")
print(df.head(3))