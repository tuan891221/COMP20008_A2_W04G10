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

## Exact scope of the Assignment 1 references

The amendment prohibits the cleaned/modified A1 **dataset**. It does not say that
all transformations previously used in A1 are forbidden.

The current A2 specification is explicit in section 3.3:

- `bathrooms` is the numeric variable the A1 pipeline derived from
  `bathrooms_text`, and the specification says to reuse it rather than
  re-parsing for the correlation task;
- `price` is described as cleaned per Assignment 1.

Accordingly, this project recomputes numeric bathrooms and cleaned price from
the original Inside Airbnb A2 download. Amenity parsing/counting and the
controlled amenity indicators are implemented in the A2 workflow and are not
claimed to be required A1 reuse. No A1 CSV is used as input.
