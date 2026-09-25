# A2 Data Amendment

The teaching team clarified the dataset rule for COMP20008 Assignment 2:

- Use **only the original datasets available directly from the Inside Airbnb website**.
- **Do not use the cleaned/modified dataset provided for Assignment 1**.
- Group members should make sure everyone is aware of this before beginning A2 analysis.

## Impact on W04G10

The group's A1 archives contain useful preprocessing code, but the A1 listings CSV itself must not be used as the A2 analysis dataset.

The inspected A1 listings CSV has **21,251 rows and 29 columns** and is a curated teaching dataset. These A1-specific row/column counts are recorded here only to prevent accidental reuse; they are **not A2 analysis results**.

For A2:
1. obtain the original Melbourne listings data directly from Inside Airbnb;
2. run the A1 cleaning logic again on that original data;
3. recompute all counts, percentages, correlations, thresholds, model scores and feature rankings from the A2 source data;
4. keep the raw A2 input unchanged and derive processed outputs reproducibly.

## A1 code that is relevant to A2

The uploaded A1 code contains:
- corrected price parsing;
- corrected amenity counting;
- bedroom extraction from description;
- bathroom extraction from `bathrooms_text` and description;
- diagnostic comparisons.

For the current A2 research question, the most directly reusable pieces are:
- cleaned nightly price;
- amenity count;
- numeric bathrooms from `bathrooms_text`.

The assignment specification explicitly refers to reusing the numeric bathroom variable derived by the Assignment 1 pipeline rather than independently inventing a new parsing rule.
