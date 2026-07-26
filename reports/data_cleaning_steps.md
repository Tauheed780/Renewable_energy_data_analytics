# Phase 3: Data Cleaning — Renewable Energy Dataset

Input: `owid-energy-data.csv`
Output: `clean_energy_data.csv`

Run with: `python clean_energy_data.py`

## Steps

1. Load raw dataset
2. Inspect shape, dtypes, missing values, duplicates
3. Remove non-country aggregate rows (continents, income groups, "World", etc.)
4. Drop exact duplicate rows
5. Keep only relevant columns for the project (country, year, production/share metrics, population, GDP)
6. Handle missing values (forward-fill within each country's time series, then drop rows still missing core metrics)
7. Fix data types (year as int)
8. Remove/flag outliers in generation columns (negative values are invalid)
9. Save cleaned dataset to CSV

## Script

```python
import pandas as pd
import numpy as np

# ---------------------------------------------------------
# Step 1: Load raw dataset
# ---------------------------------------------------------
df = pd.read_csv("owid-energy-data.csv")
print("Raw shape:", df.shape)

# ---------------------------------------------------------
# Step 2: Inspect data
# ---------------------------------------------------------
print(df.info())
print(df.describe())
print("Missing values per column (top 10):")
print(df.isnull().sum().sort_values(ascending=False).head(10))
print("Duplicate rows:", df.duplicated().sum())

# ---------------------------------------------------------
# Step 3: Remove non-country aggregate rows
# ---------------------------------------------------------
# OWID includes regions/aggregates (continents, income groups, "World")
# that would double-count if left in with real countries.
aggregate_keywords = [
    "World", "Africa", "Asia", "Europe", "North America", "South America",
    "Oceania", "European Union", "income countries", "OECD", "OPEC",
    "Non-OECD", "USSR", "Central America", "Middle East"
]
mask_aggregate = df["country"].str.contains(
    "|".join(aggregate_keywords), case=False, na=False
)
df = df[~mask_aggregate].copy()
print("Shape after removing aggregates:", df.shape)

# ---------------------------------------------------------
# Step 4: Remove duplicates
# ---------------------------------------------------------
df.drop_duplicates(inplace=True)

# ---------------------------------------------------------
# Step 5: Keep only relevant columns
# ---------------------------------------------------------
relevant_cols = [
    "country", "year", "iso_code", "population", "gdp",
    "solar_electricity", "wind_electricity", "hydro_electricity",
    "other_renewable_electricity", "renewables_electricity",
    "renewables_share_energy", "renewables_share_elec",
    "solar_share_elec", "wind_share_elec", "hydro_share_elec",
    "fossil_electricity", "electricity_generation",
    "greenhouse_gas_emissions", "carbon_intensity_elec",
]
relevant_cols = [c for c in relevant_cols if c in df.columns]
df = df[relevant_cols].copy()

# ---------------------------------------------------------
# Step 6: Handle missing values
# ---------------------------------------------------------
# Forward-fill within each country's own time series (not across countries)
df.sort_values(["country", "year"], inplace=True)
fill_cols = [c for c in df.columns if c not in ("country", "year", "iso_code")]
df[fill_cols] = df.groupby("country")[fill_cols].transform(
    lambda s: s.ffill()
)

# Drop rows still missing the core renewable metrics after fill
core_cols = [c for c in ["renewables_electricity", "renewables_share_energy"] if c in df.columns]
df.dropna(subset=core_cols, how="all", inplace=True)

# ---------------------------------------------------------
# Step 7: Fix data types
# ---------------------------------------------------------
df["year"] = df["year"].astype(int)

# ---------------------------------------------------------
# Step 8: Remove invalid outliers (negative energy values)
# ---------------------------------------------------------
numeric_energy_cols = [c for c in df.columns if "electricity" in c or "share" in c]
for col in numeric_energy_cols:
    df.loc[df[col] < 0, col] = np.nan

# ---------------------------------------------------------
# Step 9: Save cleaned dataset
# ---------------------------------------------------------
df.to_csv("clean_energy_data.csv", index=False)
print("Cleaned shape:", df.shape)
print("Saved to clean_energy_data.csv")
```

## Notes
- Adjust `relevant_cols` if you decide to bring in more metrics (e.g. biofuel, per-capita figures) later.
- Forward-fill is done per-country to avoid leaking data across countries.
- Re-run this script any time the raw CSV is refreshed from OWID.
