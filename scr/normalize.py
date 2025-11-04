import os
import pandas as pd
from db import init_db, write_df
from fuzzywuzzy import process

# === Setup paths ===
BASE = os.path.join(os.path.dirname(__file__), '..')
DATA_DIR = os.path.join(BASE, 'data')
MAP_DIR = os.path.join(BASE, 'maps')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MAP_DIR, exist_ok=True)

init_db()

# === Ensure map files exist ===
state_map_path = os.path.join(MAP_DIR, 'state_map.csv')
crop_map_path = os.path.join(MAP_DIR, 'crop_map.csv')

if not os.path.exists(state_map_path):
    pd.DataFrame({
        "state_code": ["MH", "GJ", "UP", "TN", "KA"],
        "alias": ["maharashtra", "gujarat", "uttar pradesh", "tamil nadu", "karnataka"]
    }).to_csv(state_map_path, index=False)
    print(f"⚠️ Created default state_map.csv at {state_map_path}")

if not os.path.exists(crop_map_path):
    pd.DataFrame({
        "crop_id": ["RICE", "WHEAT", "MAIZE", "COTTON", "SUGARCANE"],
        "alias": ["rice", "wheat", "maize", "cotton", "sugarcane"]
    }).to_csv(crop_map_path, index=False)
    print(f"⚠️ Created default crop_map.csv at {crop_map_path}")

state_map = pd.read_csv(state_map_path)
crop_map = pd.read_csv(crop_map_path)


# === Helper functions ===
def canonical_state(name):
    if pd.isna(name) or not str(name).strip():
        return None
    name = name.strip().lower()
    exact = state_map[state_map['alias'].str.lower() == name]
    if not exact.empty:
        return exact.iloc[0]['state_code']
    best = process.extractOne(name, state_map['alias'].tolist())
    if best and best[1] >= 80:
        idx = state_map[state_map['alias'] == best[0]].index[0]
        return state_map.loc[idx, 'state_code']
    return None


def canonical_crop(name):
    if pd.isna(name) or not str(name).strip():
        return None
    name = name.strip().lower()
    exact = crop_map[crop_map['alias'].str.lower() == name]
    if not exact.empty:
        return exact.iloc[0]['crop_id']
    best = process.extractOne(name, crop_map['alias'].tolist())
    if best and best[1] >= 80:
        idx = crop_map[crop_map['alias'] == best[0]].index[0]
        return crop_map.loc[idx, 'crop_id']
    return None


# === Ingest functions ===
def ingest_raw_rainfall(path, source_url):
    print(f"🌧 Ingesting rainfall data from: {path}")
    df = pd.read_csv(path)
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

    # Normalize column names
    rename_map = {
        "subdivision": "state",      # The IMD dataset uses "SUBDIVISION"
        "year": "year",
        "annual": "annual_rainfall_mm"  # "ANNUAL" column is the yearly rainfall
    }
    df.rename(columns=rename_map, inplace=True)

    # Check required columns exist
    required_cols = ["state", "year", "annual_rainfall_mm"]
    for col in required_cols:
        if col not in df.columns:
            raise KeyError(f"Missing required column '{col}' in rainfall CSV")

    # Keep only relevant columns
    df = df[required_cols]
    df["source_raw"] = df.apply(lambda r: str(dict(r)), axis=1)
    df["source_url"] = source_url

    write_df("raw_rainfall", df)

    # Map to canonical state code
    df["state_code"] = df["state"].apply(canonical_state)

    # Aggregate by state-year
    agg = df.groupby(["state_code", "year"], as_index=False)["annual_rainfall_mm"].sum()
    agg["source_url"] = source_url

    write_df("rainfall_annual_state", agg)
    print(f"✅ Rainfall data ingested ({len(agg)} state-year rows)")


def ingest_raw_crop(path, source_url):
    print(f"🌾 Ingesting crop production data from: {path}")
    df = pd.read_csv(path)
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

    rename_map = {
        "state_name": "state",
        "district_name": "district",
        "crop": "crop",
        "season": "season",
        "area": "area_ha",
        "production": "production_tonnes",
        "year": "year",
    }
    df.rename(columns=rename_map, inplace=True)

    df = df.dropna(subset=["state", "year", "production_tonnes"], how="any")

    df["source_raw"] = df.apply(lambda r: str(dict(r)), axis=1)
    df["source_url"] = source_url

    write_df("raw_crop", df)

    df["state_code"] = df["state"].apply(canonical_state)
    df["crop_id"] = df["crop"].apply(canonical_crop)

    agg = (
        df.groupby(["state_code", "crop_id", "year"], as_index=False)
        .agg({"production_tonnes": "sum", "area_ha": "sum"})
    )
    agg["source_url"] = source_url

    write_df("crop_state_year", agg)
    print(f"✅ Crop data ingested ({len(agg)} state-crop-year rows)")


# === Run Ingestion ===
if __name__ == "__main__":
    rainfall_file = os.path.join(DATA_DIR, "imd_rainfall.csv")
    crop_file = os.path.join(DATA_DIR, "crop_district.csv")

    if os.path.exists(rainfall_file):
        ingest_raw_rainfall(rainfall_file, source_url="Local Rainfall Dataset")
    else:
        print("⚠️ Rainfall dataset not found:", rainfall_file)

    if os.path.exists(crop_file):
        ingest_raw_crop(crop_file, source_url="Local Crop Dataset")
    else:
        print("⚠️ Crop dataset not found:", crop_file)
