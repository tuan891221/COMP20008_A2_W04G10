# COMP20008 Assignment 2 — W04G10

Group project for **COMP20008 Elements of Data Processing, Semester 2, 2026**.

## Research Question

> Among Melbourne entire homes and apartments with valid nightly prices, do location and amenities improve high-price prediction beyond property size alone, and which attributes are most useful?

**Target definition:** high price means an advertised nightly price above the **training sample's 75th percentile**.

## Group Members and Responsibilities

| Area | Primary | Support |
|---|---|---|
| Preprocessing | Tuan Wei | Tianyi Qin |
| Correlation analysis | Tianyi Qin | Tuan Wei |
| Supervised learning & evaluation | Zhilin Zhang | Tuan Wei |
| Feature selection | Zhilin Zhang | Tianyi Qin |
| Report writing/editing | Tianyi Qin | Zhilin Zhang |
| Code & README | Tuan Wei | Zhilin Zhang |
| Slides | Tianyi Qin | Tuan Wei |

This is a **3-person group**, so PCA and clustering are not required.

## Repository Structure

```text
.
├── data/
│   └── README.md
├── notebooks/
│   ├── 01_preprocessing.ipynb
│   ├── 02_correlation.ipynb
│   ├── 03_modelling.ipynb
│   └── 04_feature_selection.ipynb
├── output/
│   ├── figures/
│   └── tables/
├── submission/
│   └── README.txt
├── PROJECT_CHECKLIST.md
├── requirements.txt
└── README.md
```

## Dataset amendment

The teaching team clarified that **A2 must use only the original dataset downloaded directly from the Inside Airbnb website**. The cleaned/modified dataset supplied for Assignment 1 must **not** be used for A2.

The team's A1 preprocessing logic can be reused where relevant, but it must be rerun on the original Inside Airbnb data. In particular, A1-derived cleaned price, amenity count, and numeric bathroom logic are kept in `src/a1_reuse.py`.

See `A2_DATA_AMENDMENT.md` and `data/README.md` before adding data.

## Workflow

1. Download the original Melbourne `listings.csv` directly from Inside Airbnb and place it in `data/`. Do **not** use the cleaned/modified A1 dataset.
2. Run `01_preprocessing.ipynb` and agree on the final three preprocessing tasks.
3. Export one stable processed dataset/schema for all later notebooks.
4. Run `02_correlation.ipynb`.
5. Run `03_modelling.ipynb` for KNN and Decision Tree.
6. Run `04_feature_selection.ipynb`.
7. Merge the final reproducible workflow into the required submission notebook only after all results are stable.

## Assignment-aligned analysis rules

- Preprocessing: name **6 candidates**, choose **3**, justify with dataset-specific numbers, and report measurable before/after impact.
- Correlation: compute **Pearson, Spearman, Mutual Information, and Normalised Mutual Information** for each pair in the designed set, noting when a method is inappropriate.
- Modelling: **KNN and Decision Tree are mandatory**; tune them, report every tried hyperparameter score, compare to a baseline, report per-class metrics, and quantify uncertainty for at least one metric.
- Feature selection: use **one embedded** and **one filter** method, report top 3 from each, and identify a concrete hard-case listing.
- The RQ requires comparing **property size only** against **property size + location + amenities**.
- Keep all repeated numbers consistent across notebooks/report/slides.

## Target-threshold caution

The group contract says the threshold is the **training sample's 75th percentile**. That creates a tension with a strictly stratified outer train/test split because the final label does not exist until the training threshold is known. The modelling notebook therefore includes a leakage-safe implementation and a note to confirm the preferred outer-split interpretation with the tutor before the final submission.

## Environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

## Suggested notebook ownership

- Tuan Wei: `01_preprocessing.ipynb`
- Tianyi Qin: `02_correlation.ipynb`
- Zhilin Zhang: `03_modelling.ipynb`, `04_feature_selection.ipynb`

Avoid editing the same `.ipynb` simultaneously.

## Academic-integrity note

The subject specification allows only minimal GenAI use and explicitly prohibits GenAI-generated report paragraphs/sections. This repository therefore contains coding scaffolds, checks, and reproducible analysis structure, not generated report prose.
