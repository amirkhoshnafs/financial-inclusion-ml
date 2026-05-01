import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
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
from xgboost import XGBClassifier

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
MODEL_PATH=MODELS_DIR / 'xgboost_account_model.joblib'
REPORT_PATH=REPORTS_DIR / 'xgboost_model_results.md'

TARGET_COL='target'

NUMERIC_FEATURES = MODEL_NUMERIC_FEATURES
BINARY_FEATURES = MODEL_BINARY_FEATURES
CATEGORICAL_FEATURES = MODEL_CATEGORICAL_FEATURES
FEATURES = MODEL_FEATURES


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

    model=XGBClassifier(
        n_estimators=300,
        max_depth=3,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        objective='binary:logistic',
        eval_metric='logloss',
        tree_method='hist',
        random_state=RANDOM_STATE,
        n_jobs=-1,
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
        '# XGBoost model results',
        '',
        '## Model purpose',
        '',
        'This model is the first tree-based classifier for predicting account ownership.',
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
        '## Model settings',
        '',
        '- model: `XGBClassifier`',
        '- n_estimators: 300',
        '- max_depth: 3',
        '- learning_rate: 0.05',
        '- subsample: 0.8',
        '- colsample_bytree: 0.8',
        '- tree_method: hist',
        '',
        'These settings are intentionally conservative. The goal here is a modest tree-based benchmark, not an aggressively tuned leaderboard model.',
        '',
        '## Leakage controls',
        '',
        'The model excludes account components and downstream financial behavior variables such as mobile money ownership, formal saving, borrowing, and digital payment use.',
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
        'This model should be read against the logistic regression baseline rather than in isolation.',
        '',
        'Because the project cares about targeting excluded adults, excluded-class precision and recall are reported separately.',
        '',
        'A higher AUC than the logistic baseline suggests that some nonlinear patterns or interactions are helping, even with the same compact feature set.',
        '',
        '## Limitations',
        '',
        '- This model is predictive, not causal.',
        '- It uses the same deliberately limited feature set as the logistic baseline.',
        '- Survey weights are retained in the data but not yet used in model fitting.',
        '- The default 0.5 threshold may not be the best policy threshold.',
        '- The model is only lightly tuned, so the reported lift should be treated as a modest benchmark rather than a final ceiling.',
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
