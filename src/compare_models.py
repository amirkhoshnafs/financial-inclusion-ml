from pathlib import Path

import pandas as pd

from src.config import REPORTS_DIR

BASELINE_REPORT=REPORTS_DIR / 'baseline_model_results.md'
XGBOOST_REPORT=REPORTS_DIR / 'xgboost_model_results.md'
OUT_PATH=REPORTS_DIR / 'model_comparison.md'


def parse_metric_value(value):
    value=value.strip()
    if value.endswith('%'):
        return float(value.rstrip('%')) / 100
    return float(value)


def read_metrics(path):
    lines=Path(path).read_text(encoding='utf-8').splitlines()

    rows=[]
    in_metrics=False
    for line in lines:
        if line.strip() == '## Metrics':
            in_metrics=True
            continue

        if in_metrics and line.startswith('## '):
            break

        if not in_metrics:
            continue

        if not line.startswith('|'):
            continue

        if 'metric' in line or '---' in line:
            continue

        parts=[p.strip() for p in line.strip('|').split('|')]
        if len(parts) != 2:
            continue

        metric, value=parts
        rows.append({
            'metric':metric,
            'value':parse_metric_value(value),
            'display_value':value,
        })

    return pd.DataFrame(rows)


def comparison_table():
    baseline=read_metrics(BASELINE_REPORT)
    xgboost=read_metrics(XGBOOST_REPORT)

    out=baseline.merge(
        xgboost,
        on='metric',
        suffixes=('_logistic','_xgboost'),
    )

    out['difference']=out['value_xgboost'] - out['value_logistic']

    return out


def fmt_value(metric, value):
    if metric in {
        'accuracy',
        'precision',
        'recall',
        'excluded precision',
        'excluded recall',
        'test positive rate',
        'predicted positive rate',
    }:
        return f'{100 * value:.1f}%'

    return f'{value:.3f}'


def make_markdown_table(df):
    lines=[
        '| metric | logistic regression | XGBoost | difference |',
        '|---|---:|---:|---:|',
    ]

    for _, row in df.iterrows():
        metric=row['metric']
        lines.append(
            f'| {metric} | '
            f'{fmt_value(metric, row["value_logistic"])} | '
            f'{fmt_value(metric, row["value_xgboost"])} | '
            f'{fmt_value(metric, row["difference"])} |'
        )

    return lines


def main():
    df=comparison_table()

    key_metrics=[
        'train AUC',
        'test AUC',
        'accuracy',
        'precision',
        'recall',
        'F1',
        'excluded precision',
        'excluded recall',
        'predicted positive rate',
    ]

    report_df=df[df['metric'].isin(key_metrics)].copy()
    report_df['metric']=pd.Categorical(
        report_df['metric'],
        categories=key_metrics,
        ordered=True,
    )
    report_df=report_df.sort_values('metric')

    metric_lookup={
        row['metric']:row
        for _, row in report_df.iterrows()
    }

    lines=[
        '# Model comparison',
        '',
        '## Purpose',
        '',
        'This report compares the logistic regression baseline against the XGBoost model for predicting account ownership.',
        '',
        'The comparison uses the committed model result reports:',
        '',
        '- `reports/baseline_model_results.md`',
        '- `reports/xgboost_model_results.md`',
        '',
        '## Metric comparison',
        '',
    ]

    lines.extend(make_markdown_table(report_df))

    lines.extend([
        '',
        '## Main interpretation',
        '',
    ])

    test_auc_diff=metric_lookup['test AUC']['difference']
    f1_diff=metric_lookup['F1']['difference']
    excluded_precision_diff=metric_lookup['excluded precision']['difference']
    excluded_recall_diff=metric_lookup['excluded recall']['difference']

    lines.extend([
        f'- XGBoost improves test AUC by {test_auc_diff:.3f}.',
        f'- XGBoost improves F1 by {f1_diff:.3f}.',
        f'- XGBoost improves excluded-class precision by {100 * excluded_precision_diff:.1f} percentage points.',
        f'- XGBoost lowers excluded-class recall by {100 * abs(excluded_recall_diff):.1f} percentage points.',
        '',
        'The gain in ranking performance is real, but it is not dramatic enough to make threshold choice irrelevant.',
        '',
        'At the default 0.5 threshold, XGBoost is more precise when it predicts exclusion, but it misses more actually excluded respondents than the logistic baseline.',
        '',
        '## Policy interpretation',
        '',
        'If the use case is outreach, excluded-class recall matters because missed cases are people the program never reaches.',
        '',
        'If the use case is a constrained program budget, excluded-class precision matters because false positives absorb staff time and funds.',
        '',
        'The better threshold depends on the policy goal:',
        '',
        '- maximize reach: favor higher excluded recall',
        '- maximize targeting efficiency: favor higher excluded precision',
        '- balanced targeting: evaluate multiple thresholds',
        '',
        '## Model choice',
        '',
        'Recommended project use:',
        '',
        '- use logistic regression as the transparent baseline',
        '- use XGBoost as the stronger predictive model',
        '- use XGBoost for SHAP explanations',
        '- do not treat the default 0.5 threshold as final for policy targeting',
        '',
        '## Current conclusion',
        '',
        'XGBoost is the better ranking model in this repo, but threshold choice matters more than the raw AUC gap for any targeting use case.',
    ])

    OUT_PATH.write_text('\n'.join(lines), encoding='utf-8')

    print('saved')
    print(OUT_PATH)


if __name__ == '__main__':
    main()
