import pandas as pd

from src.config import INTERIM_DIR, MODEL_FEATURES, PROCESSED_DIR

IN_PATH = INTERIM_DIR / "microdata_core.parquet"
OUT_PATH = PROCESSED_DIR / "model_table.parquet"

ID_COLS = [
    "respondent_id",
    "economy",
    "economy_code",
    "survey_weight",
]

FEATURE_COLS = MODEL_FEATURES.copy()

TARGET_COL='has_account'

LEAKAGE_COLS=[
    'has_financial_institution_account',
    'has_mobile_money_account',
]


def load_core():
    return pd.read_parquet(IN_PATH)


def build_model_table(df):
    cols=ID_COLS + FEATURE_COLS + [TARGET_COL]
    out=df[cols].copy()

    out=out.rename(columns={
        TARGET_COL:'target',
    })

    return out


def validate(df):
    checks={
        'rows':len(df),
        'columns':len(df.columns),
        'missing_target':int(df['target'].isna().sum()),
        'target_values':sorted(df['target'].dropna().unique().tolist()),
        'duplicate_respondent_ids':int(df['respondent_id'].duplicated().sum()),
    }

    if checks['missing_target'] != 0:
        raise ValueError(f'missing target values: {checks["missing_target"]}')

    if checks['target_values'] != [0,1]:
        raise ValueError(f'unexpected target values: {checks["target_values"]}')

    leakage_found=[col for col in LEAKAGE_COLS if col in df.columns]
    if leakage_found:
        raise ValueError(f'leakage columns found: {leakage_found}')

    return checks


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    core=load_core()
    model_df=build_model_table(core)
    checks=validate(model_df)

    model_df.to_parquet(OUT_PATH, index=False)

    print('saved')
    print(OUT_PATH)

    print('\nchecks')
    for key, value in checks.items():
        print(f'{key}: {value}')

    print('\ncolumns')
    print('\n'.join(model_df.columns))

    print('\nmissing values')
    print(model_df.isna().sum().to_string())

    print('\ntarget distribution')
    print(model_df['target'].value_counts(dropna=False).to_string())


if __name__ == '__main__':
    main()
