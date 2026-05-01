import pandas as pd

from src.config import FIGURES_DIR, INTERIM_DIR
from src.eda import add_age_group, add_readable_flags, grouped_weighted_rate
from src.plots import save_rate_bar

IN_PATH=INTERIM_DIR / 'microdata_core.parquet'


def prep_table(df, group_col, min_n=100, drop_missing=True):
    table=grouped_weighted_rate(df, group_col, min_n=min_n)
    if drop_missing:
        table=table[table[group_col].notna()]
        table=table[table[group_col].astype(str).ne('<NA>')]
    return table


def main():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    df=pd.read_parquet(IN_PATH)
    df=add_readable_flags(add_age_group(df))

    gender=prep_table(df, 'gender').sort_values('has_account_rate')
    education=prep_table(df, 'education_level').sort_values('has_account_rate')
    income=prep_table(df, 'income_quintile').sort_values('income_quintile')
    internet=prep_table(df, 'internet_status').sort_values('has_account_rate')
    region=prep_table(df, 'region').sort_values('has_account_rate')
    countries=prep_table(df, 'economy', min_n=300).head(15).sort_values('has_account_rate', ascending=False)

    save_rate_bar(
        gender,
        'gender',
        'has_account_rate',
        FIGURES_DIR / 'account_by_gender.png',
        'Account ownership by gender',
    )

    save_rate_bar(
        education,
        'education_level',
        'has_account_rate',
        FIGURES_DIR / 'account_by_education.png',
        'Account ownership by education',
    )

    save_rate_bar(
        income,
        'income_quintile',
        'has_account_rate',
        FIGURES_DIR / 'account_by_income.png',
        'Account ownership by income quintile',
        horizontal=False,
    )

    save_rate_bar(
        internet,
        'internet_status',
        'has_account_rate',
        FIGURES_DIR / 'account_by_internet.png',
        'Account ownership by internet use',
    )

    save_rate_bar(
        region,
        'region',
        'has_account_rate',
        FIGURES_DIR / 'account_by_region.png',
        'Account ownership by World Bank region',
    )

    save_rate_bar(
        countries,
        'economy',
        'has_account_rate',
        FIGURES_DIR / 'lowest_account_countries.png',
        'Lowest account ownership countries',
    )

    print('saved figures')
    for path in sorted(FIGURES_DIR.glob('account_by_*.png')):
        print(path)

    print(FIGURES_DIR / 'lowest_account_countries.png')


if __name__ == '__main__':
    main()