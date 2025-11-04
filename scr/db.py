import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
from sqlalchemy import inspect
import pandas as pd

# === Database path ===
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
DB_PATH = os.path.join(BASE_DIR, "project.db")

# === Database engine ===
Engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
meta = MetaData()


# === Table definitions ===
def init_db():
    """Initialize the SQLite database and create all required tables."""

    # --- RAW RAINFALL DATA ---
    if not inspect(Engine).has_table("raw_rainfall"):
        Table(
            "raw_rainfall",
            meta,
            Column("id", Integer, primary_key=True),
            Column("state", String),
            Column("district", String),
            Column("year", Integer),
            Column("month", String),
            Column("rainfall_mm", Float),
            Column("source_raw", String),
            Column("source_url", String),
        )

    # --- RAW CROP PRODUCTION DATA ---
    if not inspect(Engine).has_table("raw_crop"):
        Table(
            "raw_crop",
            meta,
            Column("id", Integer, primary_key=True),
            Column("state", String),
            Column("district", String),
            Column("year", Integer),
            Column("season", String),
            Column("crop", String),
            Column("area_ha", Float),
            Column("production_tonnes", Float),
            Column("source_raw", String),
            Column("source_url", String),
        )

    # --- AGGREGATED RAINFALL (STATE-YEAR LEVEL) ---
    if not inspect(Engine).has_table("rainfall_annual_state"):
        Table(
            "rainfall_annual_state",
            meta,
            Column("id", Integer, primary_key=True),
            Column("state_code", String),
            Column("year", Integer),
            Column("annual_rainfall_mm", Float),
            Column("source_url", String),
        )

    # --- AGGREGATED CROP PRODUCTION (STATE-YEAR LEVEL) ---
    if not inspect(Engine).has_table("crop_state_year"):
        Table(
            "crop_state_year",
            meta,
            Column("id", Integer, primary_key=True),
            Column("state_code", String),
            Column("crop_id", String),
            Column("year", Integer),
            Column("production_tonnes", Float),
            Column("area_ha", Float),
            Column("source_url", String),
        )

    # --- Create all defined tables ---
    meta.create_all(Engine)
    print(f"✅ Database initialized at: {DB_PATH}")


# === DataFrame I/O Helpers ===
def write_df(table_name, df: pd.DataFrame, if_exists="append"):
    """Write DataFrame to SQLite."""
    df.to_sql(table_name, Engine, if_exists=if_exists, index=False)


def read_sql(query):
    """Read SQL query into a DataFrame."""
    return pd.read_sql(query, Engine)


# === Run directly ===
if __name__ == "__main__":
    init_db()
