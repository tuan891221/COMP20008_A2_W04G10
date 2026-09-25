"""
Reusable preprocessing logic adapted from W04G10 members' COMP20008 A1 code.

Important:
- This module reuses the team's code logic, not the A1 processed dataset.
- For A2, run these functions on the ORIGINAL Melbourne data downloaded
  directly from Inside Airbnb.
"""

from __future__ import annotations

import csv
import json
import re
from typing import Iterable

import numpy as np
import pandas as pd


# Exact schema observed in the cleaned/modified A1 listings file supplied
# in the uploaded assignment1 archive. A2 must NOT use that dataset.
A1_CURATED_COLUMNS = {
    "id", "name", "description", "host_id", "host_identity_verified",
    "host_is_superhost", "host_listings_count", "neighbourhood_cleansed",
    "latitude", "longitude", "property_type", "room_type", "accommodates",
    "bathrooms_text", "bedrooms", "beds", "amenities", "price",
    "minimum_nights", "maximum_nights", "availability_365",
    "has_availability", "number_of_reviews", "first_review", "last_review",
    "review_scores_rating", "review_scores_cleanliness",
    "review_scores_value", "reviews_per_month",
}


def validate_a2_source(df: pd.DataFrame) -> None:
    """Reject the known 29-column A1 curated dataset.

    This is a guard against accidental reuse of the A1 teaching dataset.
    It is not intended to prove that any arbitrary file is an official
    Inside Airbnb download, so the download source/date must still be recorded.
    """
    columns = set(df.columns)

    if len(df.columns) == len(A1_CURATED_COLUMNS) and columns == A1_CURATED_COLUMNS:
        raise ValueError(
            "This file matches the 29-column cleaned/modified A1 dataset. "
            "A2 requires the original dataset downloaded directly from "
            "Inside Airbnb. Replace data/listings.csv with the original file."
        )


def parse_price_value(value):
    """Convert Inside Airbnb price strings using the team's A1 parsing rule."""
    if pd.isna(value):
        return np.nan

    match = re.search(
        r"^\s*\$?\s*(\d+(?:,\d{3})*)(?:\.(\d+))?\s*$",
        str(value),
    )
    if not match:
        return np.nan

    integer_part = match.group(1).replace(",", "")
    decimal_part = match.group(2)

    if decimal_part:
        return float(f"{integer_part}.{decimal_part}")
    return float(integer_part)


def add_clean_price(
    df: pd.DataFrame,
    source: str = "price",
    target: str = "price_clean",
) -> pd.DataFrame:
    out = df.copy()
    out[target] = out[source].apply(parse_price_value)
    return out


def parse_amenities(value) -> list[str]:
    """Parse the JSON-style amenities field into a Python list.

    The A1 team used corrected parsing instead of splitting on commas.
    JSON parsing is retained here, with a conservative fallback for malformed
    rows so diagnostics can identify them instead of silently miscounting.
    """
    if pd.isna(value):
        return []

    if isinstance(value, list):
        return value

    text = str(value).strip()
    if text in {"", "[]"}:
        return []

    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return parsed
    except (json.JSONDecodeError, TypeError):
        pass

    # Fallback adapted from another group member's A1 solution: strip the
    # outer brackets and let csv.reader respect quoted commas.
    inner = text
    if len(inner) >= 2 and inner[0] in "[{" and inner[-1] in "]}":
        inner = inner[1:-1]
    if inner == "":
        return []

    try:
        return [
            item.strip()
            for item in next(csv.reader([inner], skipinitialspace=True))
            if item.strip() != ""
        ]
    except Exception:
        # Last-resort conservative fallback.
        return re.findall(r'"(?:[^"\\]|\\.)*"', text)


def count_amenities_value(value) -> int:
    return len(parse_amenities(value))


def add_amenity_count(
    df: pd.DataFrame,
    source: str = "amenities",
    target: str = "amenity_count",
) -> pd.DataFrame:
    out = df.copy()
    out[target] = out[source].apply(count_amenities_value)
    return out


_BATH_NUMBER_RE = re.compile(
    r"^(\d+(?:\.\d+)?)\s+(?:shared\s+|private\s+)?baths?$",
    re.IGNORECASE,
)


def parse_bathrooms_text(value):
    """Derive the A1-style numeric bathroom variable from bathrooms_text."""
    if pd.isna(value):
        return np.nan

    text = str(value).strip()

    # A1 treated Half-bath / Shared half-bath / Private half-bath as 0.5.
    if "half-bath" in text.lower():
        return 0.5

    match = _BATH_NUMBER_RE.match(text)
    if match:
        return float(match.group(1))

    return np.nan


def add_bathrooms_numeric(
    df: pd.DataFrame,
    source: str = "bathrooms_text",
    target: str = "bathrooms",
) -> pd.DataFrame:
    out = df.copy()
    out[target] = out[source].apply(parse_bathrooms_text)
    return out


_BEDROOM_DESC_RE = re.compile(
    r"(\d+(?:\.\d+)?)[ -]?(?:bedrooms?|bdr|br)\b",
    re.IGNORECASE,
)


def extract_bedrooms_from_description_value(value):
    if pd.isna(value):
        return np.nan

    match = _BEDROOM_DESC_RE.search(str(value))
    if match:
        return float(match.group(1))

    return np.nan


def add_bedrooms_from_description(
    df: pd.DataFrame,
    source: str = "description",
    target: str = "bedrooms_from_desc",
) -> pd.DataFrame:
    out = df.copy()
    out[target] = out[source].apply(extract_bedrooms_from_description_value)
    return out


def validate_melbourne_source(df: pd.DataFrame) -> None:
    """Reject a clearly non-Melbourne detailed listings file.

    This does not replace recording the official Inside Airbnb source URL/date.
    It catches accidental uploads from another city (for example Albany).
    """
    required = {"latitude", "longitude", "room_type", "price", "id"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Detailed listings file is missing required columns: {sorted(missing)}")

    lat = pd.to_numeric(df["latitude"], errors="coerce")
    lon = pd.to_numeric(df["longitude"], errors="coerce")
    if lat.notna().sum() == 0 or lon.notna().sum() == 0:
        raise ValueError("Cannot validate city because latitude/longitude are empty.")

    med_lat = float(lat.median())
    med_lon = float(lon.median())

    # Broad metro-Melbourne sanity bounds, intentionally wider than the CBD.
    if not (-39.5 <= med_lat <= -36.5 and 143.0 <= med_lon <= 146.5):
        raise ValueError(
            "This file does not appear to be Melbourne data. "
            f"Median coordinates are ({med_lat:.4f}, {med_lon:.4f}). "
            "Use the Melbourne, Victoria, Australia detailed listings.csv.gz "
            "from Inside Airbnb (16 June 2026 snapshot for this repository)."
        )
