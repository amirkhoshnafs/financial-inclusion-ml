# SHAP summary

## Purpose

This report explains the XGBoost account ownership model using SHAP values.

The model predicts probability of account ownership:

- higher prediction = more likely to own an account
- lower prediction = more likely to be financially excluded

## Method

- model: `models/xgboost_account_model.joblib`
- sample size for SHAP: 3,000 test rows or fewer
- explanation type: Tree SHAP on the fitted XGBoost model
- feature space: preprocessed model features after imputation and one-hot encoding

## Top global drivers

| rank | feature | mean absolute SHAP value |
|---:|---|---:|
| 1 | `region_High income` | 0.5127 |
| 2 | `uses_internet` | 0.4606 |
| 3 | `is_employed` | 0.2982 |
| 4 | `education_level_primary_or_less` | 0.2828 |
| 5 | `education_level_tertiary_or_more` | 0.2666 |
| 6 | `age` | 0.2657 |
| 7 | `region_Middle East & North Africa (excluding high income)` | 0.1717 |
| 8 | `region_Latin America & Caribbean (excluding high income)` | 0.1497 |
| 9 | `income_quintile_5.0` | 0.1005 |
| 10 | `income_quintile_1.0` | 0.0747 |
| 11 | `is_female` | 0.0640 |
| 12 | `is_urban` | 0.0608 |
| 13 | `region_South Asia` | 0.0557 |
| 14 | `region_Sub-Saharan Africa (excluding high income)` | 0.0462 |
| 15 | `income_quintile_4.0` | 0.0326 |

## Interpretation

The largest SHAP values identify the features that move the model predictions the most on average.

Because the model uses one-hot encoded categorical variables, one underlying concept can show up as several rows in the table.

The SHAP results should be interpreted as predictive associations, not causal effects.

## Policy caution

A feature with high SHAP importance is useful for understanding model behavior, but it does not show that changing that feature would cause account ownership to rise.

For example, if internet use is important, that tells us digital access is tightly associated with inclusion in the model. It does not prove that providing internet access alone would raise account ownership.

## Generated figures

- `figures/shap_feature_importance.png`
- `figures/shap_beeswarm.png`
