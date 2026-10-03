COMP20008 Assignment 2 - W04G10
================================

Submit these two files separately through A2: Code & Comments:

    code.ipynb
    README.txt

Do not submit a ZIP file or a __MACOSX folder.

Implementation summary
----------------------
The notebook answers the following research question:

Among Melbourne entire homes and apartments with valid nightly prices, do
location and amenities improve high-price prediction beyond property size
alone, and which attributes are most useful?

The notebook is standalone. It contains the full workflow for:

1. downloading and validating the original Inside Airbnb data;
2. constructing the eligible Entire home/apt cohort;
3. preprocessing bathrooms, CBD distance and amenities;
4. defining the training-sample-Q75 high-price target;
5. Pearson, Spearman, MI and NMI analysis;
6. KNN and Decision Tree tuning and evaluation;
7. bootstrap uncertainty and feature-set comparisons;
8. embedded and filter feature selection; and
9. exporting the hard-case listing used in the report.

It does not import external project modules, does not run another
notebook and does not require a pre-generated processed dataset.

Data source
-----------
The workflow uses only the original Melbourne Detailed Listings dataset from
Inside Airbnb, not the cleaned or modified Assignment 1 dataset.

Snapshot:

    Melbourne, Victoria, Australia
    16 June 2026
    Detailed listings.csv.gz

If data/listings.csv is absent, code.ipynb downloads the dated source and
checks its SHA256. If that URL later becomes unavailable, manually download
the same 16 June 2026 Melbourne Detailed Listings file, decompress it and
place it at data/listings.csv beside the notebook's working directory.

Environment
-----------
The submitted notebook was also run from start to finish on macOS arm64 with
Python 3.11.17 and reproduced the report's core tables and figures. The
environment below is the canonical Linux setup used for the reported values
and is recommended when grading because KNN has many exact-distance ties.

Recommended exact environment for the saved report values:

    Linux x86_64
    Python 3.11.16
    pandas==2.3.3
    numpy==2.3.5
    scipy==1.16.3
    scikit-learn==1.7.2
    matplotlib==3.10.6
    jupyter==1.1.1
    nbconvert==7.16.6
    ipykernel==6.31.0
    certifi==2026.5.20

Install the packages with:

    python -m pip install pandas==2.3.3 numpy==2.3.5 scipy==1.16.3 scikit-learn==1.7.2 matplotlib==3.10.6 jupyter==1.1.1 nbconvert==7.16.6 ipykernel==6.31.0 certifi==2026.5.20

How to run
----------
1. Put code.ipynb in a writable directory.
2. Start Jupyter in that directory.
3. Open code.ipynb.
4. Restart the kernel and select Run All.
5. Confirm that all 38 code cells finish without an error.

The notebook creates these folders under the working directory:

    data/
    output/tables/
    output/figures/

Report result to notebook output map
------------------------------------
Report item              Notebook section / generated output
-----------------------  ---------------------------------------------------
Tables 1 and 3           Part 1 sections 9-10;
                         preprocessing_candidates.csv,
                         preprocessing_selected_alternatives.csv,
                         preprocessing_impact.csv
Figure 1                 Part 1 section 13;
                         eligible_price_distribution.png
Table 4                  Part 2 sections 4-6;
                         correlation_results.csv
Table 2                  Part 3 sections 5-7;
                         hyperparameter_effects.csv and the CV tables
Tables 5a and 5b         Part 3 sections 4, 6 and 11;
                         model_summary.csv and confusion_*.csv
Figure 2                 Part 3 section 11;
                         model_macro_f1_comparison.png
Bootstrap intervals      Part 3 section 9;
                         model_uncertainty.csv,
                         model_incremental_bootstrap.csv,
                         model_auc_incremental_bootstrap.csv
Table 6                  Part 4 sections 3-5;
                         feature_selection_top3.csv and
                         feature_selection_rankings.csv
Figure 3                 Part 3 sections 10-11;
                         permutation_importance_decisiontree.png
Table 7                  Part 4 section 6;
                         feature_selection_hard_case.csv

Important interpretation notes
------------------------------
- Table 4 uses all eligible rows and five-bin discretisation for symmetric
  pairwise MI/NMI. Feature-selection MI is a separate training-only
  mutual_info_classif calculation on the original predictor values. This is
  why, for example, bedrooms MI is 0.1264 in Table 4 but 0.1426 in Table 6.
- The hard-case output is listing 33573259. Its 10 bedrooms exceed the
  training IQR upper fence of 6; only four training rows have at least 10
  bedrooms.
- KNN has frequent exact-distance boundary ties. Saved report values use the
  Linux environment above, stable ascending listing-ID order, brute-force
  neighbour search and one thread. Another operating system may differ in the
  last decimals, while the main feature-set conclusion remains unchanged.

The original Inside Airbnb file must not be replaced by the Assignment 1
cleaned dataset.
