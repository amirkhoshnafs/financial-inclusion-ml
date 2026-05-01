# Final project summary

## Project question

Which groups are more likely to be financially excluded, what predicts account ownership, and what intervention looks most plausible to test next?

## Dataset and target

This project uses the World Bank Global Findex 2025 microdata.

- 144,090 adult respondents
- 140 economies
- account ownership as the supervised target

`target = 1` means the respondent owns an account. `target = 0` means the respondent does not.

I use account ownership as a practical first definition of basic financial inclusion. It is narrower than full financial wellbeing, but clean enough for a focused predictive exercise.

## First-pass descriptive findings

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

The lowest account-ownership economies in the first EDA include Niger, Chad, Lebanon, Nicaragua, Madagascar, Pakistan, and Mauritania.

## Modeling readout

Two classifiers were trained on the same intentionally limited feature set:

1. logistic regression baseline
2. XGBoost benchmark

| Metric | Logistic regression | XGBoost |
|---|---:|---:|
| Test AUC | 0.822 | 0.831 |
| Accuracy | 73.6% | 79.2% |
| F1 | 0.802 | 0.865 |
| Excluded precision | 49.8% | 64.0% |
| Excluded recall | 77.7% | 47.1% |

XGBoost improves ranking performance a bit, but the more important takeaway is that model choice and threshold choice answer slightly different questions. At the default threshold, the tree model is more precise for finding excluded adults, while the logistic model recalls more of them.

## Threshold interpretation

The XGBoost threshold analysis highlights three useful operating points:

| Policy goal | Threshold | Excluded precision | Excluded recall |
|---|---:|---:|---:|
| Reach | 0.75 | 49.3% | 81.9% |
| Efficiency | 0.40 | 70.2% | 30.5% |
| Balanced | 0.70 | 52.5% | 74.4% |

Those thresholds are not universal best settings. They are examples of how the tradeoff changes depending on whether the program cares more about broad reach or tighter targeting.

## SHAP and country profiles

The strongest SHAP drivers in the XGBoost model are region context, internet use, employment status, education, age, income quintile, gender, and urbanicity.

The clustering step groups economies into four broad inclusion profiles:

| Cluster profile | Average account rate | Interpretation |
|---|---:|---|
| Very low inclusion | 35.2% | broad exclusion with large gaps |
| Low/mid inclusion with large inequality gaps | 54.0% | inclusion exists but is uneven |
| Mid/high inclusion | 76.1% | stronger inclusion with remaining subgroup gaps |
| Very high inclusion | 95.5% | near-universal account ownership |

I treat these clusters as descriptive profiles, not definitive categories.

## Final interpretation

The most consistently excluded profiles in this repo are adults with low education, low income, no internet use, rural residence, and adults living in lower-inclusion country contexts.

The policy recommendation is therefore modest: digital access plus assisted account onboarding looks like a plausible intervention to test first. The evidence is descriptive and predictive, not causal, so the recommendation should be read as a practical interpretation of the observed patterns rather than proof that the intervention would work.

## Important limitations

- This project is predictive and descriptive, not causal.
- Survey weights are used in the EDA and country profiling steps, but not in model fitting.
- Calibration is not yet evaluated.
- Validation is a standard train/test split rather than a grouped country-level split.
- Account ownership is only one measure of financial inclusion.
