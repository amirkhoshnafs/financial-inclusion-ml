# Dataset decision

## Preferred dataset plan

Use Global Findex 2025 as the primary dataset version.

## Current data status

The project currently has:

- Global Findex 2025 microdata CSV
- Global Findex 2025 codebook
- Global Findex 2025 questionnaire
- Global Findex 2025 connectivity questionnaire
- Global Findex 2025 report
- Global Findex 2025 glossary
- Global Findex 2025 survey methodology
- Global Findex 2025 variable naming script

The project still needs:

- Global Findex 2025 country-level indicators
- Global Findex 2025 indicator mapping workbook, if available

## Primary use of microdata

Microdata will be used for:

- respondent-level prediction of account ownership
- feature engineering
- subgroup model evaluation
- SHAP explanations
- example respondent profiles

## Primary use of country-level indicators

Country-level indicators will be used for:

- global overview
- country comparison
- demographic gap analysis at country level
- country clustering
- dashboard country explorer

## Why microdata matters

The main machine learning task is respondent-level:

> What predicts account ownership?

Microdata is the right source for this because each row represents an individual respondent.

## Why country-level data still matters

Country-level indicators are useful for comparison, clustering, and dashboard summaries.

However, country-level data is aggregated. It should not be the main source for individual-level classification.

## Current modeling decision

Use the 2025 microdata as the main modeling dataset.

## Current project risk

Country-level clustering and dashboard country comparison will require a country-level indicator file.

If the 2025 country-level file is not available soon, create country-level summaries directly from the microdata as a fallback.

## Fallback plan

If the official country-level indicator file is not downloaded, use the microdata to create country-level aggregates such as:

- account ownership rate
- mobile phone ownership rate
- internet use rate
- digital payment use rate
- formal saving rate
- formal borrowing rate
- financial resilience rate
- gender gap in account ownership
- income gap in account ownership
- education gap in account ownership

## Important limitation

This project is descriptive and predictive, not causal.

The model can identify associations and useful predictors, but it cannot prove that a policy intervention will cause financial inclusion to improve.
