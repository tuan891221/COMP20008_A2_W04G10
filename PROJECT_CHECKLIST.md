# W04G10 Assignment 2 Checklist

## Before analysis
- [ ] Official `listings.csv` placed in `data/`
- [ ] Dataset/version recorded
- [ ] RQ copied exactly from the group contract
- [ ] Eligible cohort rule agreed: Entire home/apt + valid positive nightly price

## Preprocessing
- [ ] Six distinct candidates named
- [ ] Dataset-specific evidence collected for all six
- [ ] Three selected
- [ ] Each selected task has a quantified selection justification
- [ ] Each selected task has a measurable before/after effect
- [ ] Alternatives considered for each selected task
- [ ] Limitations recorded

## Correlation
- [ ] Variable set justified against RQ
- [ ] Target or appropriate target representation included
- [ ] Every unique pair covered
- [ ] Pearson
- [ ] Spearman
- [ ] Mutual Information
- [ ] Normalised Mutual Information
- [ ] Inappropriate method/pair cases explicitly noted
- [ ] Agreement/divergence discussed using actual values
- [ ] Predictor-predictor relationships checked
- [ ] At least one downstream decision tied to the correlation results
- [ ] Non-causal language used

## Supervised learning
- [ ] KNN implemented
- [ ] Decision Tree implemented
- [ ] Outer split strategy justified with actual class balance
- [ ] 5-fold stratified CV used for tuning within training data
- [ ] Every tried hyperparameter score retained
- [ ] Default vs chosen value recorded for every changed hyperparameter
- [ ] Per-class precision/recall/F1 reported
- [ ] Additional metric(s) justified
- [ ] Majority-class/0R baseline evaluated using the same metrics
- [ ] Absolute improvement over baseline stated
- [ ] Uncertainty quantified for at least one metric/model
- [ ] Size-only vs size+location+amenities compared for the RQ

## Feature selection
- [ ] Embedded method
- [ ] Filter method
- [ ] Top 3 + scores from each
- [ ] Disagreement explained with actual ranking values
- [ ] One hard-case listing ID identified
- [ ] Actual attribute values quoted
- [ ] Concrete feature-set-specific ranking scenario discussed
- [ ] Limitations recorded

## Final consistency
- [ ] Same row counts wherever repeated
- [ ] Same threshold wherever repeated
- [ ] Same metric values wherever repeated
- [ ] Same feature rankings wherever repeated
- [ ] Figures/tables correctly labelled
- [ ] Report page limit checked
- [ ] Final code runs top-to-bottom from a fresh kernel
- [ ] README explains exactly how to reproduce outputs
