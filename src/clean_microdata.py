import pandas as pd

from src.config import INTERIM_DIR, RAW_MICRODATA_PATH

MICRODATA_PATH = RAW_MICRODATA_PATH
OUT_PATH = INTERIM_DIR / "microdata_core.parquet"

RAW_COLS=[
    'year',
    'economy',
    'economycode',
    'regionwb',
    'wpid_random',
    'wgt',
    'female',
    'age',
    'educ',
    'inc_q',
    'emp_in',
    'urbanicity',
    'account_fin',
    'account_mob',
    'account',
    'internet_use',
]

EDUCATION_MAP={
    1:'primary_or_less',
    2:'secondary',
    3:'tertiary_or_more',
}


def to_binary(s, true_value):
    out=s.map(lambda x: pd.NA if pd.isna(x) else int(x == true_value))
    return out.astype('Int64')


def load_raw():
    return pd.read_csv(MICRODATA_PATH, usecols=RAW_COLS)


def clean(df):
    out=pd.DataFrame({
        'year':df['year'].astype('Int64'),
        'economy':df['economy'].astype('string'),
        'economy_code':df['economycode'].astype('string'),
        'region':df['regionwb'].astype('string'),
        'respondent_id':df['wpid_random'].astype('Int64'),
        'survey_weight':df['wgt'].astype(float),
        'is_female':to_binary(df['female'], 1),
        'age':df['age'].astype('Int64'),
        'education_level':df['educ'].map(EDUCATION_MAP).astype('string'),
        'income_quintile':df['inc_q'].astype('Int64'),
        'is_employed':to_binary(df['emp_in'], 1),
        'is_urban':to_binary(df['urbanicity'], 2),
        'has_financial_institution_account':df['account_fin'].astype('Int64'),
        'has_mobile_money_account':df['account_mob'].astype('Int64'),
        'has_account':df['account'].astype('Int64'),
        'uses_internet':df['internet_use'].astype('Int64'),
    })
    return out


def validate(df):
    checks={
        'rows':len(df),
        'columns':len(df.columns),
        'missing_target':int(df['has_account'].isna().sum()),
        'target_values':sorted(df['has_account'].dropna().unique().tolist()),
        'duplicate_respondent_ids':int(df['respondent_id'].duplicated().sum()),
    }

    if checks['missing_target'] != 0:
        raise ValueError(f'missing target values: {checks["missing_target"]}')

    if checks['target_values'] != [0,1]:
        raise ValueError(f'unexpected target values: {checks["target_values"]}')

    return checks


def main():
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)

    raw=load_raw()
    clean_df=clean(raw)
    checks=validate(clean_df)

    clean_df.to_parquet(OUT_PATH, index=False)

    print('saved')
    print(OUT_PATH)

    print('\nchecks')
    for key, value in checks.items():
        print(f'{key}: {value}')

    print('\nmissing values')
    print(clean_df.isna().sum().to_string())

    print('\ntarget distribution')
    print(clean_df['has_account'].value_counts(dropna=False).to_string())


if __name__ == '__main__':
    main()
