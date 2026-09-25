# A2 Results Evidence Snapshot

**Purpose:** compact factual outputs from the successfully executed analysis pipeline.  
**Not report prose:** group members should write their own interpretation in accordance with the subject's GenAI policy.

## Source and cohort

| Item | Value |
|---|---:|
| Original Inside Airbnb Melbourne rows | 25,728 |
| Original columns | 90 |
| Entire home/apt rows | 18,829 |
| Eligible entire-home rows with valid positive price | 14,472 |
| Eligible share of raw data | 56.25% |
| Training rows | 11,577 |
| Test rows | 2,895 |
| Training-sample 75th-percentile price threshold | AUD 385.15 |
| Train high-price share | 25.00% |
| Test high-price share | 25.01% |

Official source snapshot: Melbourne, Victoria, Australia — 16 June 2026, Detailed Listings `listings.csv.gz`.

## Preprocessing evidence

| Candidate | Selected | Dataset evidence |
|---|---|---|
| Numeric bathrooms derived from `bathrooms_text` | Yes | 14,471 / 14,472 rows (99.99%) receive numeric bathrooms from 21 text categories |
| Distance from CBD | Yes | 14,472 / 14,472 rows; median 4.02 km |
| Amenity count + indicators | Yes | 13,995 unique raw amenity strings → 91 amenity-count values + 6 indicators |
| Special bedroom/bed missing treatment | No | Bedrooms missing 370 (2.56%); beds 549 (3.79%); handled inside model CV with median imputation |
| Property-type consolidation | No | 36 types; 17 have fewer than 10 eligible listings |
| Neighbourhood encoding/consolidation | No | 30 neighbourhood categories; 0 missing; distance-to-CBD used for location representation |

### Controlled amenity-indicator audit

| Indicator | Previous substring count | Controlled count | False-positive listings removed | Newly matched listings |
|---|---:|---:|---:|---:|
| has_pool | 4,610 | 4,465 | 145 | 0 |
| has_free_parking | 7,777 | 9,643 | 0 | 1,866 |
| has_air_conditioning | 11,455 | 11,455 | 0 | 0 |
| has_kitchen | 14,095 | 14,095 | 0 | 0 |
| has_washer | 13,333 | 13,029 | 304 | 0 |
| has_dryer | 12,850 | 8,954 | 3,896 | 0 |

## Target-association values

| Predictor | Pearson | Spearman | MI | NMI |
|---|---:|---:|---:|---:|
| accommodates | 0.472557 | 0.451785 | 0.106751 | 0.112332 |
| bedrooms | 0.517891 | 0.496979 | 0.126359 | 0.191129 |
| bathrooms | 0.454505 | 0.452333 | 0.106053 | 0.133476 |
| distance_cbd_km | 0.151772 | 0.158402 | 0.013411 | 0.012350 |
| amenity_count | 0.093304 | 0.106652 | 0.010542 | 0.009716 |

MI/NMI numeric variables use the notebook's quantile-discretisation implementation.

## Model results

| Model | Feature set | Accuracy | Macro-F1 | ROC-AUC | CV Macro-F1 | Class-1 F1 |
|---|---|---:|---:|---:|---:|---:|
| KNN | size only | 0.821071 | 0.743645 | 0.795945 | 0.745454 | 0.602761 |
| KNN | size + location + amenities | 0.824180 | 0.741687 | 0.827224 | 0.749937 | 0.595711 |
| Decision Tree | size only | 0.822798 | 0.754371 | 0.827199 | 0.755994 | 0.624726 |
| Decision Tree | size + location + amenities | 0.831779 | 0.759640 | 0.838081 | 0.753493 | 0.627960 |

### Incremental full-feature changes vs size-only

| Model | Macro-F1 change | Accuracy change | ROC-AUC change |
|---|---:|---:|---:|
| KNN | -0.001958 | +0.003109 | +0.031279 |
| Decision Tree | +0.005269 | +0.008981 | +0.010882 |

### Selected hyperparameters

- KNN size-only: `n_neighbors=21, p=1, weights=uniform`
- KNN full: `n_neighbors=31, p=1, weights=distance`
- Decision Tree size-only: `max_depth=5, min_samples_leaf=30, min_samples_split=2`
- Decision Tree full: `max_depth=5, min_samples_leaf=15, min_samples_split=2`

### Uncertainty

Decision Tree full-feature held-out macro-F1 bootstrap (2,000 resamples):
- bootstrap mean: 0.759487
- 95% percentile CI: [0.740448, 0.778740]

## Feature selection

| Embedded rank | Feature | DT importance | Filter rank | Feature | MI score |
|---:|---|---:|---:|---|---:|
| 1 | bedrooms | 0.780087 | 1 | bedrooms | 0.138877 |
| 2 | distance_cbd_km | 0.081151 | 2 | accommodates | 0.121966 |
| 3 | bathrooms | 0.059588 | 3 | bathrooms | 0.107577 |

## Hard-case listing

| Field | Value |
|---|---:|
| Listing ID | 1565029172672121402 |
| Hard-case feature | bedrooms |
| Bedrooms | 12 |
| Typical Q1 | 1 |
| Typical Q3 | 3 |
| IQR upper bound | 6 |
| Price | AUD 1,384 |
| High-price target | 1 |
| Split | train |
| Accommodates | 16 |
| Beds | 26 |
| Bathrooms | 12 |
| Distance from CBD | 14.339283 km |
| Amenity count | 19 |

## Reproducibility status

All four development notebooks were executed sequentially from fresh kernels using the verified original Melbourne Inside Airbnb source. The final `code.ipynb` was also executed in an otherwise empty temporary directory: all 38 code cells completed without errors, downloaded the recorded source checksum, and regenerated the full output set without `src/` or development-notebook dependencies.
