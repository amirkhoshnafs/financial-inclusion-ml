# Study notes

These are working notes for how I framed the project, not a formal results report.

## Core framing

The repo treats financial inclusion as a progression:

```text
basic access -> active use -> resilience
```

For this version of the project, I stop at the first step and model account ownership. That is not the whole concept of inclusion, but it is the cleanest entry point for a predictive exercise.

## Why the predictors are narrow

I kept the feature set small on purpose:

- age
- gender
- employment
- urbanicity
- internet use
- education
- income quintile
- region

This choice trades some predictive power for cleaner interpretation. Variables such as mobile money ownership, financial institution account ownership, saving, borrowing, and digital payment use are informative, but they are too close to the target for this specific setup.

## How to read the models

- Logistic regression is the transparency baseline.
- XGBoost is the stronger ranking model, but only by a modest AUC margin.
- Threshold choice matters more than the headline AUC difference if the practical goal is excluded-class targeting.

## How to read the policy section

The policy write-up is an interpretation layer, not a treatment-effects claim.

What the repo does support:

- identifying groups with lower observed account ownership
- showing which compact background features help rank exclusion risk
- showing how targeting tradeoffs shift with the threshold
- describing broad country profiles

What the repo does not support:

- claiming that one intervention will definitely increase account ownership
- claiming that SHAP importance is causal importance
- treating country clusters as fixed typologies

## Known limitations to keep visible

- Survey weights are used descriptively but not in model fitting.
- Calibration is not yet checked.
- Validation is not grouped by country.
- Account ownership is only one dimension of financial inclusion.

## Useful next steps

- evaluate calibration
- test grouped country validation
- examine barrier variables more directly
- compare with a survey-weighted modeling approach
