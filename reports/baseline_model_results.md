# Baseline logistic regression results

## Model purpose

This model is the first baseline classifier for predicting account ownership.

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

## Leakage controls

The baseline model excludes account components and downstream financial behavior variables such as mobile money ownership, formal saving, borrowing, and digital payment use.

## Metrics

| metric | value |
|---|---:|
| train AUC | 0.822 |
| test AUC | 0.822 |
| accuracy | 73.6% |
| precision | 90.1% |
| recall | 72.2% |
| F1 | 0.802 |
| excluded precision | 49.8% |
| excluded recall | 77.7% |
| test positive rate | 73.8% |
| predicted positive rate | 59.1% |

## Confusion matrix

| | predicted 0 | predicted 1 |
|---|---:|---:|
| actual 0 | 5,872 | 1,684 |
| actual 1 | 5,910 | 15,352 |

## Interpretation notes

This is the reference model for the project, not a claim that a linear specification is the best possible one.

Because the model uses `class_weight="balanced"`, it puts more weight on the excluded class than a plain accuracy-first fit would.

Because the project is interested in exclusion as well as inclusion, I report the excluded-class precision and recall separately.

The useful role of this baseline is to show how far a simple, interpretable model gets before moving to a tree-based model.

## Limitations

- This model is predictive, not causal.
- The feature set is intentionally narrow to reduce leakage and keep the baseline interpretable.
- Survey weights are retained in the data but not yet used in model fitting.
- The default 0.5 threshold may not be the best policy threshold.
