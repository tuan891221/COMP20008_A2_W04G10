#!/usr/bin/env python3
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.data_source import ensure_melbourne_listings

if __name__ == "__main__":
    path = ensure_melbourne_listings(REPO_ROOT / "data" / "listings.csv")
    print(path.resolve())
