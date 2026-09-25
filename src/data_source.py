"""
Official A2 data source helper for W04G10.

Downloads the original Melbourne Detailed Listings dataset directly from
Inside Airbnb and decompresses it to data/listings.csv.

Source snapshot:
Melbourne, Victoria, Australia — 16 June 2026
Detailed Listings: listings.csv.gz
"""

from __future__ import annotations

import gzip
import hashlib
import json
import shutil
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

MELBOURNE_SNAPSHOT_DATE = "2026-06-16"
MELBOURNE_LISTINGS_GZ_URL = (
    "https://data.insideairbnb.com/australia/vic/melbourne/"
    "2026-06-16/data/listings.csv.gz"
)


def _sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def ensure_melbourne_listings(
    csv_path: str | Path = "data/listings.csv",
    force: bool = False,
) -> Path:
    """Ensure the official Inside Airbnb Melbourne detailed listings CSV exists.

    If absent (or force=True), download the 16 June 2026 original
    listings.csv.gz directly from Inside Airbnb, decompress it, and write
    source metadata next to the CSV.

    Returns
    -------
    pathlib.Path
        Path to the decompressed listings.csv.
    """
    csv_path = Path(csv_path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    if csv_path.exists() and not force:
        return csv_path

    gz_path = csv_path.with_suffix(csv_path.suffix + ".gz")
    req = urllib.request.Request(
        MELBOURNE_LISTINGS_GZ_URL,
        headers={"User-Agent": "Mozilla/5.0 COMP20008-W04G10/1.0"},
    )

    print(f"Downloading original Inside Airbnb data:\n{MELBOURNE_LISTINGS_GZ_URL}")
    with urllib.request.urlopen(req, timeout=180) as response, gz_path.open("wb") as out:
        shutil.copyfileobj(response, out)

    print("Decompressing to:", csv_path)
    with gzip.open(gz_path, "rb") as src, csv_path.open("wb") as dst:
        shutil.copyfileobj(src, dst)

    metadata = {
        "city": "Melbourne",
        "region": "Victoria",
        "country": "Australia",
        "snapshot_date": MELBOURNE_SNAPSHOT_DATE,
        "source_type": "Inside Airbnb Detailed Listings",
        "source_url": MELBOURNE_LISTINGS_GZ_URL,
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "csv_sha256": _sha256(csv_path),
        "csv_bytes": csv_path.stat().st_size,
        "gz_bytes": gz_path.stat().st_size,
    }
    metadata_path = csv_path.parent / "SOURCE_METADATA.json"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    # Keep only the decompressed file required by the notebooks.
    gz_path.unlink(missing_ok=True)

    print("Downloaded:", csv_path)
    print("SHA256:", metadata["csv_sha256"])
    return csv_path
