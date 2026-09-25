# Data folder

## Mandatory A2 source requirement

The teaching team issued an amendment: **A2 must use only the original datasets available directly from the Inside Airbnb website.**

**Do not use the cleaned/modified dataset supplied for Assignment 1.**

Place the original Melbourne detailed listings file here as:

```text
data/listings.csv
```

If Inside Airbnb provides a compressed `listings.csv.gz`, decompress it to `listings.csv` before running the current notebooks.

## Why the A1 CSV cannot be reused

The A1 listings file supplied in the group's archive is a curated 29-column dataset. It is useful for reviewing the team's A1 code, but it is not an acceptable A2 input under the amendment.

The A2 preprocessing notebook contains a schema guard that rejects that known A1 29-column schema.

## What may be reused from A1

The team's own A1 **code logic** may be reused and rerun on the original Inside Airbnb dataset. Reusable helpers are in:

```text
src/a1_reuse.py
```

This includes:
- cleaning the string `price` field;
- correctly counting the JSON-style `amenities` list;
- deriving a numeric bathroom count from `bathrooms_text`;
- optional bedroom extraction from description for diagnostics.

Do not copy A1 output values, row counts, mismatch percentages, or processed CSVs into A2. Recompute everything from the original A2 source data.

## Reproducibility

Record the exact Inside Airbnb download date/version used by the group. Do not silently swap dataset versions after analysis begins, because row counts, missingness, thresholds, correlations, feature rankings and model metrics may all change.

The notebooks look for both `data/listings.csv` and `../data/listings.csv`.

Recommended generated files:

```text
data/processed_listings.csv
data/split_assignments.csv
```

Do not commit unrelated personal files, credentials, or API keys.


## Current official snapshot used by this repository

- City: Melbourne, Victoria, Australia
- Snapshot date: **16 June 2026**
- File: **Detailed Listings — listings.csv.gz**
- Direct source: `https://data.insideairbnb.com/australia/vic/melbourne/2026-06-16/data/listings.csv.gz`

Run:

```bash
python scripts/download_melbourne_data.py
```

The script downloads directly from Inside Airbnb, decompresses the file to `data/listings.csv`, and writes `data/SOURCE_METADATA.json`.
