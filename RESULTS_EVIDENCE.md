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
| Numeric bathrooms derived from `bathrooms_text` | Yes | Missingness falls from 1,285 / 14,472 (8.88%) in the original numeric field to 1 / 14,472 (0.01%) after parsing |
| Distance from CBD | Yes | 14,472 valid coordinate pairs produce 14,472 distances; median 4.02 km, IQR 1.14–13.31 km |
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
| has_dedicated_workspace | 7,915 | 7,915 | 0 | 0 |
| has_washer | 13,333 | 13,029 | 304 | 0 |
| has_dryer | 12,850 | 8,954 | 3,896 | 0 |

### CBD-distance transformation impact

The all-row correlation analysis is descriptive/exploratory and is not used for model selection.

| Representation | Predictor | Pearson with high_price | Spearman with high_price |
|---|---|---:|---:|
| Before: raw coordinate | latitude | -0.023395 | -0.044620 |
| Before: raw coordinate | longitude | 0.101116 | 0.087377 |
| After: derived distance | distance_cbd_km | 0.151772 | 0.158402 |

Post-hoc held-out ablation with the full model's hyperparameters held fixed:

| Model | Macro-F1 change from adding distance | ROC-AUC change from adding distance |
|---|---:|---:|
| KNN | +0.011279 | +0.043962 |
| Decision Tree | +0.009513 | +0.010080 |

This ablation is an interpretation/sensitivity check, not a second model-selection step.

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
| KNN | size only | 0.816926 | 0.739680 | 0.813308 | 0.746125 | 0.597876 |
| KNN | size + location + amenities | 0.817617 | 0.732198 | 0.817652 | 0.743824 | 0.580952 |
| Decision Tree | size only | 0.824180 | 0.757990 | 0.820028 | 0.754895 | 0.631427 |
| Decision Tree | size + location + amenities | 0.830743 | 0.757502 | 0.837520 | 0.753867 | 0.624233 |

### Incremental full-feature changes vs size-only

| Model | Macro-F1 change | Accuracy change | ROC-AUC change |
|---|---:|---:|---:|
| KNN | -0.007482 | +0.000691 | +0.004344 |
| Decision Tree | -0.000488 | +0.006563 | +0.017493 |

### Selected hyperparameters

- KNN size-only: `n_neighbors=21, p=1, weights=uniform`
- KNN full: `n_neighbors=15, p=1, weights=distance`
- Decision Tree size-only: `max_depth=3, min_samples_leaf=15`
- Decision Tree full: `max_depth=5, min_samples_leaf=30`

KNN uses stable listing-ID ordering and single-thread brute-force neighbour search. The size-only training set contains 867 unique feature combinations among 11,577 rows. At the selected `k=21, p=1`, 96.68% of held-out rows have an exact distance tie across the neighbour boundary; this is retained as a measured limitation rather than hidden.

The canonical outputs were produced by GitHub Actions on Linux x86_64 with Python 3.11.16. Reversing only the training-row order changes size-only KNN macro-F1 by +0.003199 and ROC-AUC by -0.004882, directly confirming tie sensitivity. It does not change the conclusion that the full feature set fails to improve KNN macro-F1.

### Uncertainty

Decision Tree full-feature held-out macro-F1 bootstrap (2,000 resamples):
- bootstrap mean: 0.757433
- 95% percentile CI: [0.737865, 0.777451]

Paired bootstrap for full minus size-only held-out macro-F1 (2,000 paired resamples):

| Model | Observed difference | 95% percentile CI | P(full > size) |
|---|---:|---:|---:|
| KNN | -0.007482 | [-0.023638, 0.010606] | 0.2010 |
| Decision Tree | -0.000488 | [-0.011464, 0.010865] | 0.4595 |

Paired bootstrap for full minus size-only held-out ROC-AUC (2,000 paired resamples):

| Model | Observed difference | 95% percentile CI | P(full > size) |
|---|---:|---:|---:|
| KNN | +0.004344 | [-0.011125, 0.018990] | 0.7065 |
| Decision Tree | +0.017493 | [0.010455, 0.025160] | 1.0000 |

## Feature selection

| Embedded rank | Feature | DT importance | Filter rank | Feature | MI score |
|---:|---|---:|---:|---|---:|
| 1 | bedrooms | 0.780613 | 1 | bedrooms | 0.142634 |
| 2 | distance_cbd_km | 0.080485 | 2 | accommodates | 0.127700 |
| 3 | bathrooms | 0.059686 | 3 | bathrooms | 0.107099 |

Meaningful filter-over-embedded disagreement: `beds` (embedded rank 6, importance 0.001791; MI rank 4, score 0.094425). Zero-importance ties are excluded from this selection.

## Hard-case listing

| Field | Value |
|---|---:|
| Listing ID | 6520432 |
| Selection rule | Highest-confidence held-out Decision Tree misclassification |
| Price | AUD 399.25 |
| Training-Q75 threshold | AUD 385.15 |
| Price margin above threshold | AUD 14.10 |
| High-price target | 1 |
| Predicted high-price class | 0 |
| Predicted-class probability | 0.965924 |
| Probability of high price | 0.034076 |
| Split | test |
| Accommodates | 2 |
| Bedrooms | 1 |
| Beds | 1 |
| Bathrooms | 1 |
| Distance from CBD | 2.384247 km |
| Amenity count | 50 |

## Reproducibility status

All four development notebooks were executed sequentially by GitHub Actions on Linux x86_64 with fresh Python 3.11.16 kernels and the verified original Melbourne Inside Airbnb source. The standalone final `code.ipynb` was independently executed from a clean checkout on the same pinned Linux environment: all 38 code cells completed without errors and regenerated the required outputs without `src/` or development-notebook dependencies. A separate local macOS run also completed, but the Linux tables above are canonical because KNN's exact-distance ties cause small cross-platform differences.
