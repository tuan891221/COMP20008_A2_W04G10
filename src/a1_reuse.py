"""Preprocessing helpers for the original Inside Airbnb A2 source data.

The A2 specification explicitly refers to the numeric ``bathrooms`` variable
derived from ``bathrooms_text`` by the Assignment 1 pipeline and to price
cleaned per Assignment 1.  These helpers reproduce those transformations on
the original A2 download; they never load or depend on the A1 cleaned dataset.
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


def _normalise_amenity_name(value) -> str:
    """Normalise one parsed amenity name without collapsing distinct names."""
    text = str(value).strip().casefold()
    text = text.replace("\xa0", " ").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", text)


# Match complete parsed amenity names.  Anchoring prevents false positives such
# as Hair dryer, Dishwasher, Pool table, Pool view, and Whirlpool appliances.
_CONTROLLED_AMENITY_PATTERNS = {
    "has_pool": re.compile(
        r"^(?:(?:private|shared) )?(?:(?:indoor|outdoor) )?pool(?: -.*)?$"
    ),
    "has_free_parking": re.compile(
        r"^free (?:(?:street|driveway) )?parking(?: (?:garage|lot))?"
        r"(?: on premises)?(?: -.*)?$"
    ),
    "has_kitchen": re.compile(
        r"^(?:kitchen|kitchenette|(?:(?:private|shared) )?outdoor kitchen"
        r"(?: with .*)?)$"
    ),
    "has_washer": re.compile(r"^(?:(?:free|paid) )?washer(?: -.*)?$"),
    "has_dryer": re.compile(r"^(?:(?:free|paid) )?dryer(?: -.*)?$"),
}

_CONTROLLED_AMENITY_NAMES = {
    "has_air_conditioning": {
        "air conditioning",
        "central air conditioning",
        "portable air conditioning",
        "window ac unit",
    },
}

CONTROLLED_AMENITY_FEATURES = (
    "has_pool",
    "has_free_parking",
    "has_air_conditioning",
    "has_kitchen",
    "has_washer",
    "has_dryer",
)


def amenity_indicator(items: Iterable[str], feature: str) -> int:
    """Return 1 when parsed amenities contain the controlled feature name."""
    names = {_normalise_amenity_name(item) for item in items}

    if feature in _CONTROLLED_AMENITY_NAMES:
        return int(bool(names & _CONTROLLED_AMENITY_NAMES[feature]))

    pattern = _CONTROLLED_AMENITY_PATTERNS.get(feature)
    if pattern is None:
        raise KeyError(f"Unknown controlled amenity feature: {feature}")
    return int(any(pattern.fullmatch(name) for name in names))


def add_amenity_indicators(
    df: pd.DataFrame,
    source: str = "amenities_list",
) -> pd.DataFrame:
    """Add controlled amenity indicators from a parsed amenity-list column."""
    out = df.copy()
    for feature in CONTROLLED_AMENITY_FEATURES:
        out[feature] = out[source].apply(
            lambda items, selected=feature: amenity_indicator(items, selected)
        )
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
