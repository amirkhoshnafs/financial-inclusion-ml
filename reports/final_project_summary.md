# Final project summary

## Project question

Which groups are financially excluded, what predicts inclusion, and which policy intervention would likely help most?

## Dataset

This project uses the World Bank Global Findex 2025 microdata.

The modeling table contains:

- 144,090 adult respondents
- 140 economies
- 13 model table columns
- account ownership as the target

## Main target

The supervised learning target is account ownership:

- `target = 1`: respondent owns an account
- `target = 0`: respondent does not own an account

Account ownership is used as the core measure of basic financial inclusion.

## First EDA findings

Weighted account ownership is 71.0%.

Account ownership is lower among:

| Group comparison | Lower-inclusion group | Rate | Higher-inclusion group | Rate |
|---|---|---:|---|---:|
| Gender | women | 68.1% | men | 74.1% |
| Education | primary education or less | 51.9% | tertiary education or more | 93.4% |
| Income | poorest quintile | 61.1% | richest quintile | 80.6% |
| Internet use | does not use internet | 46.5% | uses internet | 80.0% |
| Urbanicity | rural | 66.3% | urban | 76.6% |

The largest observed gaps are education and internet use.

## Lowest account ownership countries

The lowest-account-ownership economies in the first EDA are:

| Economy | Account ownership rate |
|---|---:|
| Niger | 14.8% |
| Chad | 20.9% |
| Lebanon | 23.0% |
| Nicaragua | 23.5% |
| Madagascar | 24.5% |
| Pakistan | 27.3% |
| Mauritania | 27.3% |

## Model comparison

Two classifiers were trained:

1. logistic regression baseline
2. XGBoost advanced model

| Metric | Logistic regression | XGBoost |
|---|---:|---:|
| Test AUC | 0.822 | 0.831 |
| Accuracy | 73.6% | 79.2% |
| F1 | 0.802 | 0.865 |
| Excluded precision | 49.8% | 64.0% |
| Excluded recall | 77.7% | 47.1% |

XGBoost performs better overall, but logistic regression has higher excluded recall at the default threshold.

## Threshold analysis

XGBoost threshold analysis shows different policy options:

| Policy goal | Threshold | Excluded precision | Excluded recall |
|---|---:|---:|---:|
| Reach | 0.75 | 49.3% | 81.9% |
| Efficiency | 0.40 | 70.2% | 30.5% |
| Balanced | 0.70 | 52.5% | 74.4% |

The model should not be used only with the default 0.5 threshold for policy targeting.

## SHAP findings

The strongest XGBoost model drivers are:

1. region context
2. internet use
3. employment status
4. education level
5. age
6. income quintile
7. gender
8. urbanicity

These are predictive associations, not causal effects.

## Country clustering

The country clustering analysis identified four broad country profiles:

| Cluster profile | Average account rate | Interpretation |
|---|---:|---|
| Very low inclusion | 35.2% | broad financial exclusion with large gender gaps |
| Low/mid inclusion with large inequality gaps | 54.0% | inclusion exists but is uneven |
| Mid/high inclusion | 76.1% | stronger inclusion but remaining subgroup gaps |
| Very high inclusion | 95.5% | near-universal account ownership and small gaps |

## Final recommendation

The recommended policy direction is:

> Digital access plus assisted account onboarding.

This intervention should prioritize:

- adults with primary education or less
- adults in the poorest income quintiles
- adults who do not use the internet
- rural residents
- women in countries with large gender gaps
- very low inclusion country clusters

## Limitations

This project is descriptive and predictive, not causal.

The results show associations and useful prediction patterns. They do not prove that a policy intervention would cause account ownership to increase.

A causal version would require experiments, policy variation, quasi-experimental designs, or longitudinal data.