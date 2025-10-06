import pandas as pd
import numpy as np
from functools import partial


# Task 1

# Example user data with Indian names and cities
data = {
    "Name": ["Mitali", "Arjun", "Priya", "Rushi", "Geeta", "Rucha", "Kavita", "Nilesh"],
    "Age": [30, "thirty", 38, np.nan, 34, 40, "45", 20],
    "City": [
        "Mumbai",
        "Delhi",
        "Bengaluru",
        "Hyderabad",
        "Chennai",
        "Pune",
        "Kolkata",
        "Mumbai",
    ],
    "RegistrationDate": [
        "2021-01-15",
        "2021-06-20",
        "2022-03-10",
        np.nan,
        "2022-12-05",
        "2023-05-18",
        "2024-09-23",
        "2021-01-15",
    ],
}

# Convert dictionary to DataFrame
df = pd.DataFrame(data)

# Save as CSV file
df.to_csv("user_data.csv", index=False)
print("CSV file: user_data.csv")

# Load and display the saved data
df_loaded = pd.read_csv("user_data.csv")
print("\nLoaded DataFrame:")
print(df_loaded)


# Task 2
# Create custom index for all users
custom_index = ["user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8"]
s = pd.Series(df["Age"].values, index=custom_index)
print("\nCustom Series:")
print(s)

# Task 3
# Create a pandas dataframe
df = pd.DataFrame(data)

# Task 4
# Inspect the DataFrame
# Inspect basics
print("\nData types:")
print(df.dtypes)

print("\nFirst 5 rows:")
print(df.head(5))

print("\nLast 4 rows:")
print(df.tail(4))

print("\nSummary stats:")
print(df.describe())


# Task 5

# Perform data slicing by row position and column name

# Slice by row position (first 4 rows)
print("\nFirst 4 rows by position:")
print(df.iloc[0:4])

# Slice by column name
print("\nName and City columns:")
print(df[["Name", "City"]])

# Task 6
# Slice using boolean flags and data range
flags = [True, False, True, True, False, False, True, True]
print("\nRows selected by boolean flags:")
print(df[flags])

# Filter by range
temp_df = df.copy()
temp_df["Age"] = pd.to_numeric(temp_df["Age"], errors="coerce")

print("\nAges between 25 and 45:")
print(temp_df[(temp_df["Age"] >= 25) & (temp_df["Age"] <= 45)])

# Task 7
# Data cleaning with duplicated, nunique, drop_duplicates
# Check for duplicates
print("\nDuplicates:")
print(df.duplicated())

# Unique counts per column
print("\nUnique values per column:")
print(df.nunique())

# Drop duplicates
df_clean = df.drop_duplicates()
print("\nAfter dropping duplicates:")
print(df_clean)

# Task 8
# Safe type conversion with pd.to_numeric and pd.to_datetime

# Convert Age to numeric
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")

# Convert RegistrationDate to datetime
df["RegistrationDate"] = pd.to_datetime(df["RegistrationDate"], errors="coerce")

print("\nAfter type conversion:")
print(df.dtypes)
print("\nUpdated DataFrame:")
print(df)

# Task 9
# Set default values for missing data using .apply()


# Set default values for missing Age
def set_default(x):
    if pd.isna(x):
        return 35.0  # Default age for missing values
    return float(x)


# Apply to Age column
df["Age"] = df["Age"].apply(set_default)

print("\nAfter setting defaults for missing Age:")
print(df)

# Check for remaining missing values
print("\nMissing values count:")
print(df.isnull().sum())

# Task 10
# Data cleaning pipeline with .pipe() for type conversion


# Define a cleaning function
def convert_types(df: pd.DataFrame) -> pd.DataFrame:
    # Convert Age and RegistrationDate to correct types
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    df["RegistrationDate"] = pd.to_datetime(df["RegistrationDate"], errors="coerce")

    # Show data types and missing counts
    print("\nIn pipeline: dtypes after conversion")
    print(df.dtypes)
    print("Null counts:")
    print(df.isnull().sum())

    return df


# Reload original dataset
df = pd.read_csv("user_data.csv")

# Use pipe to apply cleaning function
df = df.pipe(convert_types)

print("\nFinal DataFrame after pipe:")
print(df)

# Task 11
# .pipe() with partial arguments and threshold


# Reload dataset
df = pd.read_csv("user_data.csv")


# Define a function that drops columns with missing data above a threshold
def drop_high_missing(df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    # Calculate missing percentage for each column
    missing_perc = df.isnull().mean()

    # Identify columns exceeding the threshold
    cols_to_drop = missing_perc[missing_perc > threshold].index

    # Drop those columns
    df = df.drop(columns=cols_to_drop)

    print(f"\nIn pipeline: Dropped columns with >{threshold*100}% missing values")
    print("Remaining columns:")
    print(df.columns)

    return df


# Use .pipe() with partial() to pass the threshold argument (20%)
df = df.pipe(partial(drop_high_missing, threshold=0.2))

print("\nFinal DataFrame after threshold pipe:")
print(df)
