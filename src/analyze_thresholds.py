import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

from src.config import FIGURES_DIR, MODELS_DIR, PROCESSED_DIR, REPORTS_DIR, RANDOM_STATE

IN_PATH=PROCESSED_DIR / 'model_table.parquet'
MODEL_PATH=MODELS_DIR / 'xgboost_account_model.joblib'
REPORT_PATH=REPORTS_DIR / 'threshold_analysis.md'
FIGURE_PATH=FIGURES_DIR / 'xgboost_threshold_tradeoff.png'

TARGET_COL='target'

FEATURES=[
    'is_female',
    'age',
    'education_level',
    'income_quintile',
    'is_employed',
    'is_urban',
    'uses_internet',
    'region',
]


def load_data():
    return pd.read_parquet(IN_PATH)


def prepare_features(df):
    x=df[FEATURES].copy()

    numeric_features=['age', 'is_female', 'income_quintile', 'is_employed', 'is_urban', 'uses_internet']
    categorical_features=['education_level', 'region']

    x[numeric_features]=x[numeric_features].astype(float)
    x[categorical_features]=x[categorical_features].astype(object)
    x=x.mask(x.isna(), np.nan)

    return x.infer_objects(copy=False)


def split_data(df):
    x=prepare_features(df)
    y=df[TARGET_COL].astype(int)

    return train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y,
    )


def threshold_metrics(y_true, prob, threshold):
    pred=(prob >= threshold).astype(int)

    tn, fp, fn, tp=confusion_matrix(y_true, pred).ravel()

    account_precision=tp / (tp + fp) if (tp + fp) else 0
    account_recall=tp / (tp + fn) if (tp + fn) else 0
    excluded_precision=tn / (tn + fn) if (tn + fn) else 0
    excluded_recall=tn / (tn + fp) if (tn + fp) else 0

    return {
        'threshold':threshold,
        'account_precision':account_precision,
        'account_recall':account_recall,
        'excluded_precision':excluded_precision,
        'excluded_recall':excluded_recall,
        'predicted_account_rate':pred.mean(),
        'predicted_excluded_rate':1 - pred.mean(),
        'tn':int(tn),
        'fp':int(fp),
        'fn':int(fn),
        'tp':int(tp),
    }


def build_threshold_table(y_true, prob):
    thresholds=[round(x,2) for x in [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9]]
    rows=[threshold_metrics(y_true, prob, t) for t in thresholds]
    return pd.DataFrame(rows)


def choose_thresholds(table):
    reach_pool=table[table['excluded_recall'] >= 0.80]
    if len(reach_pool):
        reach=reach_pool.sort_values(
            ['excluded_precision','excluded_recall'],
            ascending=[False,False],
        ).iloc[0]
    else:
        reach=table.sort_values(
            ['excluded_recall','excluded_precision'],
            ascending=[False,False],
        ).iloc[0]

    efficiency_pool=table[table['excluded_precision'] >= 0.70]
    if len(efficiency_pool):
        efficiency=efficiency_pool.sort_values(
            ['excluded_recall','excluded_precision'],
            ascending=[False,False],
        ).iloc[0]
    else:
        efficiency=table.sort_values(
            ['excluded_precision','excluded_recall'],
            ascending=[False,False],
        ).iloc[0]

    balanced=table.assign(
        excluded_f1=lambda x: 2 * x['excluded_precision'] * x['excluded_recall'] / (
            x['excluded_precision'] + x['excluded_recall']
        )
    ).sort_values('excluded_f1', ascending=False).iloc[0]

    return reach, efficiency, balanced


def fmt_pct(x):
    return f'{100 * x:.1f}%'


def make_report(table):
    reach, efficiency, balanced=choose_thresholds(table)

    lines=[
        '# XGBoost threshold analysis',
        '',
        '## Purpose',
        '',
        'This report shows how changing the XGBoost classification threshold affects account-owner prediction and excluded-person targeting.',
        '',
        'The model predicts probability of account ownership:',
        '',
        '- higher probability = more likely to own an account',
        '- lower probability = more likely to be financially excluded',
        '',
        'The default threshold is 0.5:',
        '',
        '- probability >= 0.5 → predicted account owner',
        '- probability < 0.5 → predicted excluded',
        '',
        '## Threshold tradeoff table',
        '',
        '| threshold | account precision | account recall | excluded precision | excluded recall | predicted excluded rate |',
        '|---:|---:|---:|---:|---:|---:|',
    ]

    for _, row in table.iterrows():
        lines.append(
            f'| {row["threshold"]:.2f} | '
            f'{fmt_pct(row["account_precision"])} | '
            f'{fmt_pct(row["account_recall"])} | '
            f'{fmt_pct(row["excluded_precision"])} | '
            f'{fmt_pct(row["excluded_recall"])} | '
            f'{fmt_pct(row["predicted_excluded_rate"])} |'
        )

    lines.extend([
        '',
        '## Candidate thresholds',
        '',
        'Candidate thresholds are selected using simple practical constraints so the report does not recommend extreme endpoints.',
        '',
        '### Reach-oriented threshold',
        '',
        f'- threshold: {reach["threshold"]:.2f}',
        f'- excluded recall: {fmt_pct(reach["excluded_recall"])}',
        f'- excluded precision: {fmt_pct(reach["excluded_precision"])}',
        '',
        'Use this when the policy goal is to reach as many excluded people as possible.',
        '',
        '### Efficiency-oriented threshold',
        '',
        f'- threshold: {efficiency["threshold"]:.2f}',
        f'- excluded precision: {fmt_pct(efficiency["excluded_precision"])}',
        f'- excluded recall: {fmt_pct(efficiency["excluded_recall"])}',
        '',
        'Use this when the policy goal is to avoid targeting people who are already included.',
        '',
        '### Balanced threshold',
        '',
        f'- threshold: {balanced["threshold"]:.2f}',
        f'- excluded precision: {fmt_pct(balanced["excluded_precision"])}',
        f'- excluded recall: {fmt_pct(balanced["excluded_recall"])}',
        '',
        'Use this when the project needs a compromise between reach and targeting efficiency.',
        '',
        '## Interpretation',
        '',
        'Lower thresholds predict more people as account owners and fewer people as excluded.',
        '',
        'Higher thresholds predict fewer people as account owners and more people as excluded.',
        '',
        'Because the project focuses on financial exclusion, threshold choice should be tied to policy goals rather than selected only from default model settings.',
        '',
        '## Recommendation',
        '',
        'Use XGBoost probabilities for ranking risk of exclusion rather than relying only on the default 0.5 threshold.',
        '',
        'For the portfolio project, report the default threshold metrics but also show the threshold tradeoff table.',
    ])

    REPORT_PATH.write_text('\n'.join(lines), encoding='utf-8')


def make_plot(table):
    import matplotlib.pyplot as plt

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax=plt.subplots(figsize=(8,5))

    ax.plot(table['threshold'], table['excluded_precision'], marker='o', label='Excluded precision')
    ax.plot(table['threshold'], table['excluded_recall'], marker='o', label='Excluded recall')
    ax.plot(table['threshold'], table['predicted_excluded_rate'], marker='o', label='Predicted excluded rate')

    ax.set_title('XGBoost threshold tradeoff for financial exclusion')
    ax.set_xlabel('Account ownership probability threshold')
    ax.set_ylabel('Rate')
    ax.set_ylim(0,1)
    ax.legend()

    fig.tight_layout()
    fig.savefig(FIGURE_PATH, dpi=160, bbox_inches='tight')
    plt.close(fig)


def main():
    df=load_data()
    _, x_test, _, y_test=split_data(df)

    model=joblib.load(MODEL_PATH)
    prob=model.predict_proba(x_test)[:,1]

    table=build_threshold_table(y_test, prob)

    make_report(table)
    make_plot(table)

    print('saved report')
    print(REPORT_PATH)

    print('\nsaved figure')
    print(FIGURE_PATH)

    print('\nthreshold table')
    print(table.to_string(index=False))


if __name__ == '__main__':
    main()
