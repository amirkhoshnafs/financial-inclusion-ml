# Policy recommendation

## Project question

Which groups are financially excluded, what predicts inclusion, and which policy intervention would likely help most?

## Executive summary

The strongest recommendation from this analysis is:

> Prioritize digital access and assisted account onboarding for adults with low education, low income, no internet use, and people living in low-inclusion countries.

This should not be interpreted as a causal claim. The project shows descriptive and predictive evidence that these groups are strongly associated with financial exclusion.

## Evidence base

This recommendation is based on the following project outputs:

- `reports/first_eda_summary.md`
- `reports/baseline_model_results.md`
- `reports/xgboost_model_results.md`
- `reports/model_comparison.md`
- `reports/threshold_analysis.md`
- `reports/shap_summary.md`
- `reports/country_clusters.md`

## Who appears most financially excluded?

The first EDA shows that account ownership is lower among several groups:

| Group comparison | Lower-inclusion group | Account ownership rate | Higher-inclusion group | Account ownership rate |
|---|---|---:|---|---:|
| Gender | women | 68.1% | men | 74.1% |
| Education | primary education or less | 51.9% | tertiary education or more | 93.4% |
| Income | poorest quintile | 61.1% | richest quintile | 80.6% |
| Internet use | does not use internet | 46.5% | uses internet | 80.0% |
| Urbanicity | rural | 66.3% | urban | 76.6% |

The strongest observed gaps are education and internet use.

## Where is exclusion most severe?

The lowest-account-ownership countries in the first EDA include:

| Economy | Account ownership rate |
|---|---:|
| Niger | 14.8% |
| Chad | 20.9% |
| Lebanon | 23.0% |
| Nicaragua | 23.5% |
| Madagascar | 24.5% |
| Pakistan | 27.3% |
| Mauritania | 27.3% |

The country clustering analysis groups economies into four broad profiles:

| Cluster profile | Average account rate | Interpretation |
|---|---:|---|
| Very low inclusion | 35.2% | broad financial exclusion with large gender gaps |
| Low/mid inclusion with large inequality gaps | 54.0% | inclusion exists but is uneven across groups |
| Mid/high inclusion | 76.1% | stronger inclusion but remaining subgroup gaps |
| Very high inclusion | 95.5% | near-universal account ownership and small gaps |

This means policy should not be one-size-fits-all. Low-inclusion countries need broad access expansion, while mid-inclusion countries may need more targeted gap-closing interventions.

## What predicts account ownership?

The XGBoost model performs better overall than logistic regression:

| Metric | Logistic regression | XGBoost |
|---|---:|---:|
| Test AUC | 0.822 | 0.831 |
| Accuracy | 73.6% | 79.2% |
| F1 | 0.802 | 0.865 |
| Excluded precision | 49.8% | 64.0% |
| Excluded recall | 77.7% | 47.1% |

The SHAP analysis suggests that the strongest predictive drivers are:

1. region context
2. internet use
3. employment status
4. education level
5. age
6. income quintile
7. gender
8. urbanicity

This supports a policy story focused on digital access, education/literacy, income vulnerability, and country context.

## Threshold choice for policy targeting

The XGBoost model should not be used only with the default 0.5 threshold.

Threshold analysis shows three useful policy options:

| Policy goal | Threshold | Excluded precision | Excluded recall | Use case |
|---|---:|---:|---:|---|
| Reach | 0.75 | 49.3% | 81.9% | find more excluded people, accept more false positives |
| Efficiency | 0.40 | 70.2% | 30.5% | target fewer people, avoid wasting resources |
| Balanced | 0.70 | 52.5% | 74.4% | compromise between reach and efficiency |

For a public inclusion campaign, the balanced or reach-oriented threshold is more appropriate than the default 0.5 threshold.

## Recommended intervention

### Primary recommendation

Use a combined intervention:

> Digital access plus assisted account onboarding.

This means helping excluded adults both access digital channels and complete the practical steps needed to open and use an account.

The intervention should focus first on:

- adults with primary education or less
- adults in the poorest income quintiles
- adults who do not use the internet
- rural residents
- women in countries with large gender gaps
- very low inclusion country clusters

### Why this recommendation fits the evidence

The recommendation fits the project evidence for four reasons:

1. Internet use is one of the strongest descriptive gaps and one of the strongest SHAP drivers.
2. Education is one of the largest observed account ownership gaps.
3. Country clusters show that very low inclusion economies need broad access expansion, not just marginal optimization.
4. Threshold analysis shows that policy targeting should prioritize the excluded class explicitly.

## Policy design by country cluster

| Country profile | Recommended focus | Rationale |
|---|---|---|
| Very low inclusion | basic access, assisted onboarding, trust-building, ID/documentation support | exclusion is broad and account ownership is low |
| Low/mid inclusion with large gaps | targeted support for low-income, low-education, rural, and women respondents | inclusion exists but is uneven |
| Mid/high inclusion | digital usage, product design, and remaining subgroup gaps | many people have accounts but gaps remain |
| Very high inclusion | resilience, consumer protection, and quality of use | account access is mostly solved |

## What not to overclaim

This project should not claim that digital access alone causes account ownership.

The analysis is based on observational survey data. It identifies strong associations and useful predictors, but it does not estimate causal treatment effects.

A stronger causal version would require policy variation, experiments, quasi-experimental designs, or longitudinal data.

## Final answer

The most financially excluded groups are adults with low education, low income, no internet use, rural residence, and adults living in low-inclusion countries.

The strongest predictors of inclusion are country/region context, internet use, employment, education, age, and income.

The most plausible policy intervention is a targeted digital access and assisted account onboarding strategy, adapted by country cluster and evaluated with explicit threshold tradeoffs.

## Next analytical improvements

- Analyze account barrier variables directly, such as distance, cost, documentation, and trust.
- Add subgroup-specific model evaluation.
- Add calibration analysis.
- Add SHAP local examples for representative excluded profiles.
- Build a Streamlit dashboard for exploration.