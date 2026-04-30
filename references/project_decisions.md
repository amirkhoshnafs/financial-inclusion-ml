# Project decisions

## Decision 1: Main dataset

Use Global Findex 2025 microdata as the primary dataset for respondent-level modeling.

Use country-level indicators or microdata-derived country summaries for comparison and clustering.

## Decision 2: Main target

Use account ownership as the primary prediction target.

## Decision 3: Avoid target leakage

Do not use downstream financial behavior variables as predictors of account ownership.

Examples to exclude from the main account ownership model:

- digital payment use
- formal saving
- formal borrowing
- receiving wages into an account
- paying bills from an account

## Decision 4: Use one advanced model

Use one boosted tree model, preferably LightGBM.

## Decision 5: Interpret carefully

SHAP explanations will be used to interpret model predictions, not to prove causal policy impact.

## Official source notes

Useful source pages:

- https://www.worldbank.org/en/publication/globalfindex
- https://www.worldbank.org/en/publication/globalfindex/report
- https://www.worldbank.org/en/publication/globalfindex/download-data
- https://microdata.worldbank.org/catalog/global-findex
- https://microdata.worldbank.org/catalog/7860
