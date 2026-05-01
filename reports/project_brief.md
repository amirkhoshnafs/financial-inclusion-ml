# Project brief

This project uses the World Bank Global Findex 2025 microdata to model account ownership as a practical first indicator of financial inclusion. The repo combines weighted descriptive analysis with a compact classification setup: a logistic regression baseline, a lightly tuned XGBoost model, threshold analysis for excluded-class targeting, SHAP interpretation, and country-level clustering.

The main analytical choice was to keep the predictors intentionally limited. I used age, gender, employment, urbanicity, internet use, education, income quintile, and region, while excluding variables that are too close to the target itself, such as financial institution account ownership, mobile money ownership, saving, borrowing, and digital payment behavior. That makes the resulting models less powerful than a leakage-heavy setup, but easier to defend.

The main result is that XGBoost improves ranking performance a bit over logistic regression, but threshold choice matters more than the raw AUC gap if the goal is to identify people who are likely to be excluded. The strongest descriptive and predictive gaps center on education, internet use, income, and country context. The policy write-up therefore treats digital access plus assisted account onboarding as a plausible intervention to test, not a proven causal answer.
