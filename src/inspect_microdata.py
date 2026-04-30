import pandas as pd

from src.config import RAW_DIR

MICRODATA_PATH=RAW_DIR / 'global_findex_2025_microdata' / 'findex_microdata_2025_labelled_update112425.csv'

CORE_COLS=[
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
    'dig_account',
    'borrowed',
    'saved',
    'anydigpayment',
    'internet_use',
]

SEARCH_TERMS=[
    'account',
    'gender',
    'female',
    'age',
    'educ',
    'income',
    'phone',
    'mobile',
    'internet',
    'digital',
    'payment',
    'save',
    'borrow',
    'loan',
    'resilien',
    'emergency',
    'weight',
    'country',
    'economy',
]


def load_columns():
    return list(pd.read_csv(MICRODATA_PATH, nrows=0).columns)


def print_basic_info():
    cols=load_columns()
    rows=len(pd.read_csv(MICRODATA_PATH, usecols=['year']))

    print('microdata path')
    print(MICRODATA_PATH)

    print('\nshape')
    print(f'rows: {rows:,}')
    print(f'columns: {len(cols):,}')


def print_column_search():
    cols=load_columns()
    matches=[
        col for col in cols
        if any(term in col.lower() for term in SEARCH_TERMS)
    ]

    print('\nmatched columns')
    for col in matches:
        print(col)

    print(f'\nmatched: {len(matches)}')


def print_core_sample():
    df=pd.read_csv(MICRODATA_PATH, usecols=CORE_COLS, nrows=10)

    print('\ncore sample')
    print(df.to_string(index=False))


def print_value_counts():
    cols=[
        'female',
        'educ',
        'inc_q',
        'emp_in',
        'urbanicity',
        'account_fin',
        'account_mob',
        'account',
        'dig_account',
        'borrowed',
        'saved',
        'anydigpayment',
        'internet_use',
    ]
    df=pd.read_csv(MICRODATA_PATH, usecols=cols)

    print('\nvalue counts')
    for col in cols:
        print(f'\n{col}')
        print(df[col].value_counts(dropna=False).head(20).to_string())


def main():
    print_basic_info()
    print_column_search()
    print_core_sample()
    print_value_counts()


if __name__ == '__main__':
    main()