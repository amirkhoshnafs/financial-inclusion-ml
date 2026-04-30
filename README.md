# financial-inclusion-ml

Which groups are financially excluded, what predicts financial inclusion, and which policy intervention would likely help most?

## Project overview

This project uses the World Bank Global Findex database to analyze financial inclusion across countries and demographic groups. The goal is to identify excluded groups, build interpretable machine learning models that predict account ownership, cluster countries by inclusion profile, and translate the findings into practical policy recommendations.

The project combines:

- economics and financial inclusion concepts
- exploratory data analysis
- demographic gap analysis
- classification modeling
- country clustering
- SHAP explainability
- Streamlit dashboarding
- policy interpretation

## Why financial inclusion matters

Financial inclusion means that people can access and use useful financial services such as accounts, payments, savings, borrowing, and tools for managing financial shocks.

This matters because financial access can help people receive income, store money safely, make payments, build resilience, and participate in the digital economy. Exclusion is often uneven across gender, income, education, age, geography, mobile access, and internet access.

## Core project question

> Which groups are financially excluded, what predicts inclusion, and which policy intervention would likely help most?

## Planned methods

1. Document Global Findex data sources.
2. Clean country-level and microdata files.
3. Analyze account ownership and digital financial inclusion gaps.
4. Build a baseline logistic regression model.
5. Build one stronger tree-based model.
6. Explain model drivers using SHAP.
7. Cluster countries by financial inclusion profile.
8. Build a lightweight Streamlit dashboard.
9. Write a final policy recommendation.

## Repository structure

```text
financial-inclusion-ml/
├── app/              # Streamlit dashboard
├── data/             # raw, interim, and processed data
├── figures/          # exported charts
├── models/           # saved model artifacts
├── notebooks/        # analysis notebooks
├── references/       # data dictionary and source notes
├── reports/          # project brief, model report, final writeup
├── src/              # reusable Python code
├── README.md
└── requirements.txt