# NDIC + IADI Analytics Project

**Author:** Promise O. Amhanesi

## Research Question
How does NDIC's fund adequacy, coverage ratio, and premium system compare against IADI Core Principles and peer member DICs (2010–2024)?

## Key Finding
Nigeria's NDIC maintains a fund adequacy ratio 8× above the IADI 14-country peer average, but exchange rate depreciation and GDP contraction are the primary macro drivers of fund stress — identified via XGBoost and SHAP explainability on 2010–2024 data.

## Tools
| Tool | Purpose |
|------|---------|
| Python (pandas, scikit-learn, XGBoost, SHAP, Plotly) | Cleaning, feature engineering, modeling, visualisation |
| SQL (SQLite + SQLAlchemy) | Data ingestion, normalisation, joins |
| Microsoft Excel | Sanity checks, ratio validation, pivot tables |
| GitHub | Version control, public portfolio |
| Streamlit | Interactive dashboard |

## IADI Framework
This project benchmarks Nigeria's NDIC against the [IADI Core Principles for Effective Deposit Insurance Systems](https://www.iadi.org/en/core-principles-and-guidance/core-principles/).

** Launch dashboard**
```bash
streamlit run dashboard/app.py
```

## Live Demo
See `docs/demo_link.txt` for the Streamlit dashboard URL and YouTube walkthrough link.

## Data Sources
| File | Source | URL |
|------|--------|-----|
| ndic_annual_202507.csv | NDIC Annual Reports | https://ndic.gov.ng/publications |
| iadi_survey_202507.csv | IADI Annual Survey | https://www.iadi.org/en/about-iadi/annual-survey |
| world_bank_macro_202507.csv | World Bank GFDD | https://databank.worldbank.org |

## Deliverables
| # | Deliverable | Location |
|---|-------------|----------|
| 1 | Excel sanity check | excel/01_sanity_check.xlsx |
| 2 | Ratio validation workbook | excel/02_ratio_analysis.xlsx |
| 3 | EDA workbook + key findings | excel/03_eda_analysis.xlsx |
| 4 | Model validation + IADI scorecard | excel/04_model_validation.xlsx |
| 5 | Full report (10–12 pages) | docs/report.pdf |
| 6 | Slide deck (10 slides) | docs/slides.pdf |
| 7 | Public GitHub release v1.0 | This repo |

## Project Structure
data/raw/       → downloaded source files
data/clean/     → cleaned CSVs used by notebooks
sql/            → ingest and transform scripts
notebooks/      → Python Jupyter notebooks
excel/          → Excel workbooks
results/figs/   → charts and outputs
docs/           → report.pdf, slides.pdf, demo link
dashboard/      → Streamlit app (optional)

## Status
✅ Complete
