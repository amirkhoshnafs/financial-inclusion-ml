# XGBoost threshold analysis

## Purpose

This report shows how changing the XGBoost classification threshold affects account-owner prediction and excluded-person targeting.

The model predicts probability of account ownership:

- higher probability = more likely to own an account
- lower probability = more likely to be financially excluded

The default threshold is 0.5:

- probability >= 0.5 → predicted account owner
- probability < 0.5 → predicted excluded

## Threshold tradeoff table

| threshold | account precision | account recall | excluded precision | excluded recall | predicted excluded rate |
|---:|---:|---:|---:|---:|---:|
| 0.10 | 73.9% | 100.0% | 86.7% | 0.5% | 0.2% |
| 0.15 | 74.2% | 99.9% | 84.3% | 2.1% | 0.7% |
| 0.20 | 74.6% | 99.7% | 83.3% | 4.4% | 1.4% |
| 0.25 | 75.6% | 99.2% | 81.7% | 9.8% | 3.1% |
| 0.30 | 76.7% | 98.4% | 77.8% | 15.8% | 5.3% |
| 0.35 | 78.0% | 97.2% | 74.1% | 22.8% | 8.1% |
| 0.40 | 79.4% | 95.4% | 70.2% | 30.5% | 11.4% |
| 0.45 | 81.1% | 93.3% | 67.2% | 38.9% | 15.2% |
| 0.50 | 82.8% | 90.6% | 64.0% | 47.1% | 19.3% |
| 0.55 | 84.3% | 87.7% | 60.8% | 53.9% | 23.2% |
| 0.60 | 85.8% | 84.7% | 58.3% | 60.4% | 27.2% |
| 0.65 | 87.2% | 81.3% | 55.8% | 66.5% | 31.2% |
| 0.70 | 89.3% | 76.1% | 52.5% | 74.4% | 37.1% |
| 0.75 | 91.6% | 70.0% | 49.3% | 81.9% | 43.6% |
| 0.80 | 92.8% | 63.9% | 45.9% | 86.0% | 49.2% |
| 0.85 | 94.1% | 57.2% | 42.8% | 90.0% | 55.2% |
| 0.90 | 95.9% | 45.4% | 38.1% | 94.5% | 65.1% |

## Candidate thresholds

These candidate thresholds are not universal best settings. They are just useful operating points for different program tradeoffs.

### Reach-oriented threshold

- threshold: 0.75
- excluded recall: 81.9%
- excluded precision: 49.3%

Use this when the priority is broad outreach and the program can tolerate more false positives.

### Efficiency-oriented threshold

- threshold: 0.40
- excluded precision: 70.2%
- excluded recall: 30.5%

Use this when the priority is targeting efficiency and the program can only follow up on a smaller group.

### Balanced threshold

- threshold: 0.70
- excluded precision: 52.5%
- excluded recall: 74.4%

Use this when the project needs a middle ground between reach and targeting efficiency.

## Interpretation

Lower thresholds predict more people as account owners and fewer people as excluded.

Higher thresholds predict fewer people as account owners and more people as excluded.

Because the project focuses on financial exclusion, threshold choice should be tied to the intervention design rather than left at the library default.

## Recommendation

Use the XGBoost scores mainly for ranking exclusion risk, then pick a threshold that matches budget and outreach constraints.

For the portfolio project, report the default threshold metrics but also show the threshold tradeoff table.