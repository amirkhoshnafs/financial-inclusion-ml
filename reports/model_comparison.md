# Model comparison

## Purpose

This report compares the logistic regression baseline against the XGBoost model for predicting account ownership.

The comparison uses the committed model result reports:

- `reports/baseline_model_results.md`
- `reports/xgboost_model_results.md`

## Metric comparison

| metric | logistic regression | XGBoost | difference |
|---|---:|---:|---:|
| train AUC | 0.822 | 0.833 | 0.011 |
| test AUC | 0.822 | 0.831 | 0.009 |
| accuracy | 73.6% | 79.2% | 5.6% |
| precision | 90.1% | 82.8% | -7.3% |
| recall | 72.2% | 90.6% | 18.4% |
| F1 | 0.802 | 0.865 | 0.063 |
| excluded precision | 49.8% | 64.0% | 14.2% |
| excluded recall | 77.7% | 47.1% | -30.6% |
| predicted positive rate | 59.1% | 80.7% | 21.6% |

## Main interpretation

- XGBoost improves test AUC by 0.009.
- XGBoost improves F1 by 0.063.
- XGBoost improves excluded-class precision by 14.2 percentage points.
- XGBoost lowers excluded-class recall by 30.6 percentage points.

The gain in ranking performance is real, but it is not dramatic enough to make threshold choice irrelevant.

At the default 0.5 threshold, XGBoost is more precise when it predicts exclusion, but it misses more actually excluded respondents than the logistic baseline.

## Policy interpretation

If the use case is outreach, excluded-class recall matters because missed cases are people the program never reaches.

If the use case is a constrained program budget, excluded-class precision matters because false positives absorb staff time and funds.

The better threshold depends on the policy goal:

- maximize reach: favor higher excluded recall
- maximize targeting efficiency: favor higher excluded precision
- balanced targeting: evaluate multiple thresholds

## Model choice

Recommended project use:

- use logistic regression as the transparent baseline
- use XGBoost as the stronger predictive model
- use XGBoost for SHAP explanations
- do not treat the default 0.5 threshold as final for policy targeting

## Current conclusion

XGBoost is the better ranking model in this repo, but threshold choice matters more than the raw AUC gap for any targeting use case.