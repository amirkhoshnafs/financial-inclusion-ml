import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config import (
    MODELS_DIR,
    MODEL_BINARY_FEATURES,
    MODEL_CATEGORICAL_FEATURES,
    MODEL_FEATURES,
    MODEL_NUMERIC_FEATURES,
    PROCESSED_DIR,
    REPORTS_DIR,
    RANDOM_STATE,
)

IN_PATH=PROCESSED_DIR / 'model_table.parquet'
MODEL_PATH=MODELS_DIR / 'baseline_logistic_regression.joblib'
REPORT_PATH=REPORTS_DIR / 'baseline_model_results.md'

TARGET_COL='target'

NUMERIC_FEATURES = MODEL_NUMERIC_FEATURES
BINARY_FEATURES = MODEL_BINARY_FEATURES
CATEGORICAL_FEATURES = MODEL_CATEGORICAL_FEATURES
FEATURES = MODEL_FEATURES

METADATA_COLS=[
    'respondent_id',
    'economy',
    'economy_code',
    'survey_weight',
]


def load_data():
    return pd.read_parquet(IN_PATH)


def prepare_features(df):
    x=df[FEATURES].copy()

    x[NUMERIC_FEATURES]=x[NUMERIC_FEATURES].astype(float)
    x[BINARY_FEATURES]=x[BINARY_FEATURES].astype(float)
    x[CATEGORICAL_FEATURES]=x[CATEGORICAL_FEATURES].astype(object)

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


def build_pipeline():
    numeric_pipe=Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
    ])

    binary_pipe=Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
    ])

    categorical_pipe=Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore')),
    ])

    preprocess=ColumnTransformer([
        ('numeric', numeric_pipe, NUMERIC_FEATURES),
        ('binary', binary_pipe, BINARY_FEATURES),
        ('categorical', categorical_pipe, CATEGORICAL_FEATURES),
    ])

    model=LogisticRegression(
        max_iter=1000,
        class_weight='balanced',
        random_state=RANDOM_STATE,
    )

    return Pipeline([
        ('preprocess', preprocess),
        ('model', model),
    ])


def evaluate(model, x_train, x_test, y_train, y_test):
    train_prob=model.predict_proba(x_train)[:,1]
    test_prob=model.predict_proba(x_test)[:,1]
    test_pred=(test_prob >= 0.5).astype(int)

    tn, fp, fn, tp=confusion_matrix(y_test, test_pred).ravel()
    excluded_precision=tn / (tn + fn)
    excluded_recall=tn / (tn + fp)

    metrics={
        'train_auc':roc_auc_score(y_train, train_prob),
        'test_auc':roc_auc_score(y_test, test_prob),
        'accuracy':accuracy_score(y_test, test_pred),
        'precision':precision_score(y_test, test_pred),
        'recall':recall_score(y_test, test_pred),
        'f1':f1_score(y_test, test_pred),
        'excluded_precision':excluded_precision,
        'excluded_recall':excluded_recall,
        'true_negatives':int(tn),
        'false_positives':int(fp),
        'false_negatives':int(fn),
        'true_positives':int(tp),
        'test_rows':len(y_test),
        'positive_rate_test':float(y_test.mean()),
        'predicted_positive_rate':float(test_pred.mean()),
    }

    return metrics


def format_pct(x):
    return f'{100 * x:.1f}%'


def make_report(metrics):
    lines=[
        '# Baseline logistic regression results',
        '',
        '## Model purpose',
        '',
        'This model is the first baseline classifier for predicting account ownership.',
        '',
        'Target:',
        '',
        '- `target = 1`: respondent owns an account',
        '- `target = 0`: respondent does not own an account',
        '',
        '## Features',
        '',
        'Numeric features:',
        '',
    ]

    for col in NUMERIC_FEATURES:
        lines.append(f'- `{col}`')

    lines.extend([
        '',
        'Binary features:',
        '',
    ])

    for col in BINARY_FEATURES:
        lines.append(f'- `{col}`')

    lines.extend([
        '',
        'Categorical features:',
        '',
    ])

    for col in CATEGORICAL_FEATURES:
        lines.append(f'- `{col}`')

    lines.extend([
        '',
        '## Leakage controls',
        '',
        'The baseline model excludes account components and downstream financial behavior variables such as mobile money ownership, formal saving, borrowing, and digital payment use.',
        '',
        '## Metrics',
        '',
        '| metric | value |',
        '|---|---:|',
        f'| train AUC | {metrics["train_auc"]:.3f} |',
        f'| test AUC | {metrics["test_auc"]:.3f} |',
        f'| accuracy | {format_pct(metrics["accuracy"])} |',
        f'| precision | {format_pct(metrics["precision"])} |',
        f'| recall | {format_pct(metrics["recall"])} |',
        f'| F1 | {metrics["f1"]:.3f} |',
        f'| excluded precision | {format_pct(metrics["excluded_precision"])} |',
        f'| excluded recall | {format_pct(metrics["excluded_recall"])} |',
        f'| test positive rate | {format_pct(metrics["positive_rate_test"])} |',
        f'| predicted positive rate | {format_pct(metrics["predicted_positive_rate"])} |',
        '',
        '## Confusion matrix',
        '',
        '| | predicted 0 | predicted 1 |',
        '|---|---:|---:|',
        f'| actual 0 | {metrics["true_negatives"]:,} | {metrics["false_positives"]:,} |',
        f'| actual 1 | {metrics["false_negatives"]:,} | {metrics["true_positives"]:,} |',
        '',
        '## Interpretation notes',
        '',
        'This is the reference model for the project, not a claim that a linear specification is the best possible one.',
        '',
        'Because the model uses `class_weight=\"balanced\"`, it puts more weight on the excluded class than a plain accuracy-first fit would.',
        '',
        'Because the project is interested in exclusion as well as inclusion, I report the excluded-class precision and recall separately.',
        '',
        'The useful role of this baseline is to show how far a simple, interpretable model gets before moving to a tree-based model.',
        '',
        '## Limitations',
        '',
        '- This model is predictive, not causal.',
        '- The feature set is intentionally narrow to reduce leakage and keep the baseline interpretable.',
        '- Survey weights are retained in the data but not yet used in model fitting.',
        '- The default 0.5 threshold may not be the best policy threshold.',
    ])

    REPORT_PATH.write_text('\n'.join(lines), encoding='utf-8')


def main():
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    df=load_data()
    x_train, x_test, y_train, y_test=split_data(df)

    model=build_pipeline()
    model.fit(x_train, y_train)

    metrics=evaluate(model, x_train, x_test, y_train, y_test)

    joblib.dump(model, MODEL_PATH)
    make_report(metrics)

    print('saved model')
    print(MODEL_PATH)

    print('\nsaved report')
    print(REPORT_PATH)

    print('\nmetrics')
    for key, value in metrics.items():
        print(f'{key}: {value}')


if __name__ == '__main__':
    main()
