# Financial Inclusion ML

This repository uses the World Bank Global Findex 2025 microdata to study account ownership as a practical first measure of financial inclusion. The project combines weighted descriptive analysis, a simple classification baseline, a small XGBoost benchmark, threshold analysis, SHAP-based interpretation, country profiling, clustering, and a cautious policy write-up.

I kept the modeling feature set intentionally limited: age, gender, employment, urbanicity, internet use, education, income quintile, and region. That keeps the prediction task interpretable and avoids obvious leakage from variables that are really components or downstream consequences of already having an account.

## Project Question

> Which groups are more likely to be financially excluded, what predicts account ownership, and what intervention looks most plausible to test next?

This is a predictive and descriptive project, not a causal one. The goal is to identify useful patterns and targeting tradeoffs, not to claim that one variable directly causes inclusion.

## Dataset

- Source: World Bank Global Findex 2025 microdata
- Rows: 144,090 adult respondents
- Coverage: 140 economies
- Main target: account ownership

Expected raw file path:

```text
data/raw/global_findex_2025_microdata/findex_microdata_2025_labelled_update112425.csv
```

### Data Availability

- The raw Global Findex CSV is not tracked by git and should stay out of a public GitHub push.
- In this local working copy, the raw CSV, raw reference PDFs, processed parquet files, and trained models are present for verification. They are gitignored.
- A small set of figures is committed so the README and reports remain readable on GitHub.
- The main recreatable local outputs are `data/interim/microdata_core.parquet`, `data/processed/*.parquet`, `models/*.joblib`, and most report/figure artifacts.

If you are recreating the project locally, put the downloaded raw CSV in `data/raw/global_findex_2025_microdata/` and keep the rest of the large raw/reference files out of version control as well.

## Why Account Ownership

Account ownership is a narrow target, but it is a defensible starting point. It captures basic access to the formal financial system and is much easier to model cleanly than deeper behaviors like saving, borrowing, or digital payments, many of which are partly downstream of already having an account.

That is also why the model excludes variables such as financial institution account ownership, mobile money ownership, saving, borrowing, and digital payment behavior. Those variables are analytically interesting, but they would blur the line between predictors and outcomes in this specific task.

## What the Repo Covers

1. Raw data inspection and cleaning
2. Weighted first-pass EDA
3. Model table construction
4. Logistic regression baseline
5. XGBoost benchmark
6. Threshold tradeoff analysis
7. SHAP explanations for the XGBoost model
8. Country profile construction and clustering
9. A final policy interpretation with explicit caveats

## Main Findings

Weighted account ownership in the cleaned microdata is 71.0%.

Account ownership is lower among:

| Group comparison | Lower-inclusion group | Rate | Higher-inclusion group | Rate |
|---|---|---:|---|---:|
| Gender | women | 68.1% | men | 74.1% |
| Education | primary education or less | 51.9% | tertiary education or more | 93.4% |
| Income | poorest quintile | 61.1% | richest quintile | 80.6% |
| Internet use | does not use internet | 46.5% | uses internet | 80.0% |
| Urbanicity | rural | 66.3% | urban | 76.6% |

Education and internet use show the largest gaps in this first pass.

## Model Summary

Two models are compared on the same compact feature set:

| Metric | Logistic regression | XGBoost |
|---|---:|---:|
| Test AUC | 0.822 | 0.831 |
| Accuracy | 73.6% | 79.2% |
| F1 | 0.802 | 0.865 |
| Excluded precision | 49.8% | 64.0% |
| Excluded recall | 77.7% | 47.1% |

XGBoost gives a small ranking lift, but the bigger practical point is threshold choice. At the default `0.5` threshold, the tree model is more precise for finding excluded adults, while the logistic model recalls more of them.

For the XGBoost model, three threshold settings are useful illustrations:

| Policy goal | Threshold | Excluded precision | Excluded recall |
|---|---:|---:|---:|
| Reach | 0.75 | 49.3% | 81.9% |
| Efficiency | 0.40 | 70.2% | 30.5% |
| Balanced | 0.70 | 52.5% | 74.4% |

Those are not universal best thresholds. They are just different operating points for different program constraints.

## Country-Level Readout

The clustering step groups economies into four broad inclusion profiles, from very low inclusion to near-universal account ownership. I treat those clusters as descriptive profiles rather than definitive categories; they depend on the features included in the country profile table and on the choice of four clusters.

## Repository Structure

```text
data/
  raw/                 # local raw downloads, gitignored
  interim/             # local cleaned intermediate data, gitignored
  processed/           # local model-ready outputs, gitignored

figures/               # selected committed figures for GitHub rendering
models/                # local trained models, gitignored
notebooks/             # exploratory notebooks
references/            # project notes and source documentation
reports/               # Markdown reports and summaries
src/                   # runnable modules
```

## Reproduce

Install dependencies:

```bash
pip install -r requirements.txt
```

Place the raw CSV at:

```text
data/raw/global_findex_2025_microdata/findex_microdata_2025_labelled_update112425.csv
```

Run the project step by step:

```bash
python -m src.clean_microdata
python -m src.build_model_table
python -m src.make_model_table_report
python -m src.make_first_eda_report
python -m src.make_first_eda_figures
python -m src.train_baseline_model
python -m src.train_xgboost_model
python -m src.compare_models
python -m src.analyze_thresholds
python -m src.explain_xgboost_shap
python -m src.build_country_profiles
python -m src.cluster_countries
python -m src.make_policy_recommendation
```

The heavier steps are `train_xgboost_model` and `explain_xgboost_shap`. Several of these commands overwrite local generated artifacts in `data/`, `models/`, `reports/`, and `figures/`.

## Main Reports

- [`reports/final_project_summary.md`](reports/final_project_summary.md)
- [`reports/project_brief.md`](reports/project_brief.md)
- [`reports/model_comparison.md`](reports/model_comparison.md)
- [`reports/threshold_analysis.md`](reports/threshold_analysis.md)
- [`reports/policy_recommendation.md`](reports/policy_recommendation.md)
- [`reports/country_clusters.md`](reports/country_clusters.md)

## Limitations

- The project is predictive and descriptive, not causal.
- Survey weights are used in the EDA and country profiles, but not in model fitting.
- Calibration is not yet evaluated, so predicted scores should be read mainly as ranking signals.
- Validation uses a standard train/test split rather than grouped country-level splits.
- Account ownership is only one slice of financial inclusion; it does not capture quality of use or resilience on its own.
- Threshold choice is a program tradeoff, not a single correct setting.

## What I Would Improve Next

- Evaluate calibration and score reliability directly.
- Test country-grouped validation to check cross-economy generalization.
- Add subgroup performance slices for the excluded class.
- Use barrier variables more directly in a follow-up descriptive analysis.
- Compare against a survey-weighted modeling approach if the use case requires population-level targeting claims.
