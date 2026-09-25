#!/usr/bin/env python3
from pathlib import Path
import json
import sys

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.data_source import ensure_melbourne_listings, MELBOURNE_LISTINGS_GZ_URL
from src.a1_reuse import (
    validate_a2_source,
    validate_melbourne_source,
    add_clean_price,
    add_amenity_count,
    add_bathrooms_numeric,
)

DATA_PATH = ensure_melbourne_listings(REPO_ROOT / "data" / "listings.csv", force=True)
df_raw = pd.read_csv(DATA_PATH, low_memory=False)
validate_a2_source(df_raw)
validate_melbourne_source(df_raw)

df = df_raw.loc[df_raw["room_type"].eq("Entire home/apt")].copy()
df = add_clean_price(df, "price", "price_clean")
df = add_amenity_count(df, "amenities", "amenity_count")
df = add_bathrooms_numeric(df, "bathrooms_text", "bathrooms_a1")

valid_price = df["price_clean"].notna() & np.isfinite(df["price_clean"]) & df["price_clean"].gt(0)
eligible = df.loc[valid_price].copy()

# Distance from Melbourne CBD (approx. GPO / central Melbourne).
lat2 = np.radians(-37.8136)
lon2 = np.radians(144.9631)
lat1 = np.radians(pd.to_numeric(eligible["latitude"], errors="coerce"))
lon1 = np.radians(pd.to_numeric(eligible["longitude"], errors="coerce"))
dlat = lat1 - lat2
dlon = lon1 - lon2
a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
eligible["distance_cbd_km"] = 6371.0088 * 2 * np.arcsin(np.sqrt(a))

def missing_info(col):
    return {
        "missing_n": int(eligible[col].isna().sum()),
        "missing_pct": round(float(eligible[col].isna().mean() * 100), 2),
        "n_unique": int(eligible[col].nunique(dropna=True)),
    }

property_counts = eligible["property_type"].value_counts(dropna=False)
neighbour_counts = eligible["neighbourhood_cleansed"].value_counts(dropna=False)

summary = {
    "source_url": MELBOURNE_LISTINGS_GZ_URL,
    "raw_shape": [int(df_raw.shape[0]), int(df_raw.shape[1])],
    "median_latitude": float(pd.to_numeric(df_raw["latitude"], errors="coerce").median()),
    "median_longitude": float(pd.to_numeric(df_raw["longitude"], errors="coerce").median()),
    "entire_home_rows": int(len(df)),
    "eligible_valid_price_rows": int(len(eligible)),
    "eligible_pct_of_raw": round(float(len(eligible) / len(df_raw) * 100), 2),
    "price_describe": {k: (None if pd.isna(v) else float(v)) for k,v in eligible["price_clean"].describe(percentiles=[.25,.5,.75,.9,.95,.99]).to_dict().items()},
    "candidate_missingness": {c: missing_info(c) for c in [
        "accommodates","bedrooms","beds","bathrooms_text","bathrooms_a1",
        "latitude","longitude","amenities","amenity_count","property_type",
        "neighbourhood_cleansed","distance_cbd_km"
    ] if c in eligible.columns},
    "property_type_count": int(property_counts.size),
    "property_type_lt10_count": int((property_counts < 10).sum()),
    "neighbourhood_count": int(neighbour_counts.size),
    "amenity_count_describe": {k: float(v) for k,v in eligible["amenity_count"].describe(percentiles=[.25,.5,.75,.9,.95]).to_dict().items()},
    "distance_cbd_km_describe": {k: float(v) for k,v in eligible["distance_cbd_km"].describe(percentiles=[.25,.5,.75,.9,.95]).to_dict().items()},
    "bathrooms_a1_describe": {k: float(v) for k,v in eligible["bathrooms_a1"].dropna().describe(percentiles=[.25,.5,.75,.9,.95]).to_dict().items()},
    "top_property_types": {str(k): int(v) for k,v in property_counts.head(20).items()},
    "top_neighbourhoods": {str(k): int(v) for k,v in neighbour_counts.head(20).items()},
}

out = REPO_ROOT / "output" / "data_profile.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps(summary, indent=2))
