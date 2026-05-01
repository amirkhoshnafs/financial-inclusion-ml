# XGBoost model results

## Model purpose

This model is the first tree-based classifier for predicting account ownership.

Target:

- `target = 1`: respondent owns an account
- `target = 0`: respondent does not own an account

## Features

Numeric features:

- `age`

Binary features:

- `is_female`
- `is_employed`
- `is_urban`
- `uses_internet`

Categorical features:

- `education_level`
- `income_quintile`
- `region`

## Model settings

- model: `XGBClassifier`
- n_estimators: 300
- max_depth: 3
- learning_rate: 0.05
- subsample: 0.8
- colsample_bytree: 0.8
- tree_method: hist

These settings are intentionally conservative. The goal is a modest tree-based benchmark, not an aggressively tuned leaderboard model.

## Leakage controls

The model excludes account components and downstream financial behavior variables such as mobile money ownership, formal saving, borrowing, and digital payment use.

## Metrics

| metric | value |
|---|---:|
| train AUC | 0.833 |
| test AUC | 0.831 |
| accuracy | 79.2% |
| precision | 82.8% |
| recall | 90.6% |
| F1 | 0.865 |
| excluded precision | 64.0% |
| excluded recall | 47.1% |
| test positive rate | 73.8% |
| predicted positive rate | 80.7% |

## Confusion matrix

| | predicted 0 | predicted 1 |
|---|---:|---:|
| actual 0 | 3,560 | 3,996 |
| actual 1 | 2,005 | 19,257 |

## Interpretation notes

This model should be read against the logistic regression baseline rather than in isolation.

Because the project cares about targeting excluded adults, excluded-class precision and recall are reported separately.

A higher AUC than the logistic baseline suggests that some nonlinear patterns or interactions are helping, even with the same compact feature set.

## Limitations

- This model is predictive, not causal.
- It uses the same deliberately limited feature set as the logistic baseline.
- Survey weights are retained in the data but not yet used in model fitting.
- The default 0.5 threshold may not be the best policy threshold.
- The model is only lightly tuned, so the reported lift should be treated as a modest benchmark rather than a final ceiling.
