import joblib
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import shap

from sklearn.model_selection import train_test_split
from xgboost import DMatrix

from src.config import (
    FIGURES_DIR,
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
REPORT_PATH=REPORTS_DIR / 'shap_summary.md'

FEATURE_IMPORTANCE_PATH=FIGURES_DIR / 'shap_feature_importance.png'
BEESWARM_PATH=FIGURES_DIR / 'shap_beeswarm.png'

TARGET_COL='target'

FEATURES = MODEL_FEATURES

SAMPLE_SIZE=3000


def load_data():
    return pd.read_parquet(IN_PATH)


def prepare_features(df):
    x=df[FEATURES].copy()

    x[MODEL_NUMERIC_FEATURES] = x[MODEL_NUMERIC_FEATURES].astype(float)
    x[MODEL_BINARY_FEATURES] = x[MODEL_BINARY_FEATURES].astype(float)
    x[MODEL_CATEGORICAL_FEATURES] = x[MODEL_CATEGORICAL_FEATURES].astype(object)
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


def clean_feature_name(name):
    name=name.replace('numeric__','')
    name=name.replace('binary__','')
    name=name.replace('categorical__','')
    return name


def get_transformed_sample(model, x_test):
    sample=x_test.sample(
        n=min(SAMPLE_SIZE, len(x_test)),
        random_state=RANDOM_STATE,
    )

    preprocess=model.named_steps['preprocess']
    x_trans=preprocess.transform(sample)

    if hasattr(x_trans, 'toarray'):
        x_trans=x_trans.toarray()

    feature_names=[
        clean_feature_name(name)
        for name in preprocess.get_feature_names_out()
    ]

    return sample, x_trans, feature_names


def compute_shap(model, x_trans, feature_names):
    xgb_model=model.named_steps['model']
    booster=xgb_model.get_booster()
    dmatrix=DMatrix(x_trans, feature_names=feature_names)
    shap_values=booster.predict(dmatrix, pred_contribs=True)

    return np.asarray(shap_values)[:, :-1]


def make_importance_table(shap_values, feature_names):
    importance=pd.DataFrame({
        'feature':feature_names,
        'mean_abs_shap':np.abs(shap_values).mean(axis=0),
    })

    return importance.sort_values('mean_abs_shap', ascending=False)


def save_feature_importance_plot(importance):
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    plot_df=importance.head(15).sort_values('mean_abs_shap')

    fig, ax=plt.subplots(figsize=(8,6))
    ax.barh(plot_df['feature'], plot_df['mean_abs_shap'])
    ax.set_title('XGBoost SHAP feature importance')
    ax.set_xlabel('Mean absolute SHAP value')
    ax.set_ylabel('')
    fig.tight_layout()
    fig.savefig(FEATURE_IMPORTANCE_PATH, dpi=160, bbox_inches='tight')
    plt.close(fig)


def save_beeswarm_plot(shap_values, x_trans, feature_names):
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    shap.summary_plot(
        shap_values,
        features=x_trans,
        feature_names=feature_names,
        show=False,
        max_display=15,
    )

    fig=plt.gcf()
    fig.tight_layout()
    fig.savefig(BEESWARM_PATH, dpi=160, bbox_inches='tight')
    plt.close(fig)


def make_report(importance):
    top=importance.head(15)

    lines=[
        '# SHAP summary',
        '',
        '## Purpose',
        '',
        'This report explains the XGBoost account ownership model using SHAP values.',
        '',
        'The model predicts probability of account ownership:',
        '',
        '- higher prediction = more likely to own an account',
        '- lower prediction = more likely to be financially excluded',
        '',
        '## Method',
        '',
        f'- model: `models/xgboost_account_model.joblib`',
        f'- sample size for SHAP: {SAMPLE_SIZE:,} test rows or fewer',
        '- explanation type: Tree SHAP on the fitted XGBoost model',
        '- feature space: preprocessed model features after imputation and one-hot encoding',
        '',
        '## Top global drivers',
        '',
        '| rank | feature | mean absolute SHAP value |',
        '|---:|---|---:|',
    ]

    for i, row in enumerate(top.itertuples(index=False), start=1):
        lines.append(
            f'| {i} | `{row.feature}` | {row.mean_abs_shap:.4f} |'
        )

    lines.extend([
        '',
        '## Interpretation',
        '',
        'The largest SHAP values identify the features that move the model predictions the most on average.',
        '',
        'Because the model uses one-hot encoded categorical variables, one underlying concept can show up as several rows in the table.',
        '',
        'The SHAP results should be interpreted as predictive associations, not causal effects.',
        '',
        '## Policy caution',
        '',
        'A feature with high SHAP importance is useful for understanding model behavior, but it does not show that changing that feature would cause account ownership to rise.',
        '',
        'For example, if internet use is important, that tells us digital access is tightly associated with inclusion in the model. It does not prove that providing internet access alone would raise account ownership.',
        '',
        '## Generated figures',
        '',
        '- `figures/shap_feature_importance.png`',
        '- `figures/shap_beeswarm.png`',
    ])

    REPORT_PATH.write_text('\n'.join(lines), encoding='utf-8')


def main():
    df=load_data()
    _, x_test, _, _=split_data(df)

    model=joblib.load(MODEL_PATH)

    _, x_trans, feature_names=get_transformed_sample(model, x_test)
    shap_values=compute_shap(model, x_trans, feature_names)

    importance=make_importance_table(shap_values, feature_names)

    save_feature_importance_plot(importance)
    save_beeswarm_plot(shap_values, x_trans, feature_names)
    make_report(importance)

    print('saved report')
    print(REPORT_PATH)

    print('\nsaved figures')
    print(FEATURE_IMPORTANCE_PATH)
    print(BEESWARM_PATH)

    print('\ntop features')
    print(importance.head(15).to_string(index=False))


if __name__ == '__main__':
    main()
