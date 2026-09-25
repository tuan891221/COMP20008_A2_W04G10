COMP20008 Assignment 2 — W04G10
================================

Files to submit
---------------
- code.ipynb
- README.txt

Research question
-----------------
Among Melbourne entire homes and apartments with valid nightly prices, do
location and amenities improve high-price prediction beyond property size
alone, and which attributes are most useful?

Data source
-----------
This code uses the ORIGINAL Melbourne Detailed Listings dataset downloaded
directly from Inside Airbnb, not the cleaned/modified Assignment 1 dataset.

Snapshot:
- Melbourne, Victoria, Australia
- 16 June 2026
- Detailed listings.csv.gz

The notebook automatically downloads the official source if data/listings.csv
is not present. The repository also records source metadata and a SHA256 hash.

Python environment
------------------
Recommended: Python 3.11

The tested package versions are:

    pandas==2.3.3
    numpy==2.3.5
    scipy==1.16.3
    scikit-learn==1.7.2
    matplotlib==3.10.6
    jupyter==1.1.1
    nbconvert==7.16.6
    ipykernel==6.31.0
    certifi==2026.5.20

Install them directly with:

    python -m pip install pandas==2.3.3 numpy==2.3.5 scipy==1.16.3 scikit-learn==1.7.2 matplotlib==3.10.6 jupyter==1.1.1 nbconvert==7.16.6 ipykernel==6.31.0 certifi==2026.5.20

How to run
----------
Place code.ipynb in a writable directory, start Jupyter there, and open:

    submission/code.ipynb

Run all cells from a fresh kernel, top to bottom.

The submitted notebook is self-contained: it does not import repository-local
src modules and does not require any development notebook or pre-generated
processed dataset. It creates data/ and output/ beneath the working directory.

The notebook will:
1. download/validate the original Melbourne Inside Airbnb data;
2. construct the eligible Entire home/apt cohort with valid positive price;
3. apply the three selected preprocessing tasks;
4. define the training-sample-Q75 high-price target and train/test split;
5. compute Pearson, Spearman, MI and NMI for all designed variable pairs;
6. tune/evaluate KNN and Decision Tree with 5-fold stratified CV;
7. compare size-only against size + location + amenities;
8. evaluate a majority-class baseline and bootstrap uncertainty;
9. apply embedded and filter feature selection;
10. identify and export a hard-case listing.

Generated outputs
-----------------
The notebook writes reproducible tables to:

    output/tables/

and figures to:

    output/figures/

It also writes the processed handoff dataset to:

    data/processed_listings.csv

Important
---------
Do not replace the source with the cleaned/modified Assignment 1 dataset.
The code contains guards against the known A1 teaching-data schema and
against a clearly non-Melbourne file.

The report text is authored separately by the group in accordance with the
subject's GenAI rules.
