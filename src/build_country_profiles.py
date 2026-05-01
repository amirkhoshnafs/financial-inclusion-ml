import pandas as pd

from src.config import INTERIM_DIR, PROCESSED_DIR

IN_PATH=INTERIM_DIR / 'microdata_core.parquet'
OUT_PATH=PROCESSED_DIR / 'country_profiles.parquet'


def weighted_mean(df, value_col, weight_col='survey_weight'):
    x=df[[value_col, weight_col]].dropna()
    if len(x) == 0:
        return pd.NA
    return (x[value_col] * x[weight_col]).sum() / x[weight_col].sum()


def weighted_count(df, weight_col='survey_weight'):
    return df[weight_col].dropna().sum()


def rate_where(df, mask, value_col='has_account'):
    x=df.loc[mask]
    if len(x) == 0:
        return pd.NA
    return weighted_mean(x, value_col)


def first_non_null(s):
    x=s.dropna()
    if len(x) == 0:
        return pd.NA
    return x.iloc[0]


def build_profile(g):
    female_rate=rate_where(g, g['is_female'].eq(1))
    male_rate=rate_where(g, g['is_female'].eq(0))

    rural_rate=rate_where(g, g['is_urban'].eq(0))
    urban_rate=rate_where(g, g['is_urban'].eq(1))

    primary_rate=rate_where(g, g['education_level'].eq('primary_or_less'))
    tertiary_rate=rate_where(g, g['education_level'].eq('tertiary_or_more'))

    poorest_rate=rate_where(g, g['income_quintile'].eq(1))
    richest_rate=rate_where(g, g['income_quintile'].eq(5))

    return pd.Series({
        'region':first_non_null(g['region']),
        'n':len(g),
        'weighted_n':weighted_count(g),
        'account_rate':weighted_mean(g, 'has_account'),
        'internet_use_rate':weighted_mean(g, 'uses_internet'),
        'female_account_rate':female_rate,
        'male_account_rate':male_rate,
        'gender_gap_male_minus_female':male_rate - female_rate,
        'rural_account_rate':rural_rate,
        'urban_account_rate':urban_rate,
        'urban_rural_gap':urban_rate - rural_rate,
        'primary_account_rate':primary_rate,
        'tertiary_account_rate':tertiary_rate,
        'education_gap_tertiary_minus_primary':tertiary_rate - primary_rate,
        'poorest_account_rate':poorest_rate,
        'richest_account_rate':richest_rate,
        'income_gap_richest_minus_poorest':richest_rate - poorest_rate,
    })


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    df=pd.read_parquet(IN_PATH)

    profiles=(
        df.groupby(['economy','economy_code'], dropna=False)
        .apply(build_profile, include_groups=False)
        .reset_index()
    )

    profiles.to_parquet(OUT_PATH, index=False)

    print('saved')
    print(OUT_PATH)

    print('\nshape')
    print(profiles.shape)

    print('\ncolumns')
    print('\n'.join(profiles.columns))

    print('\nmissing values')
    print(profiles.isna().sum().to_string())

    print('\nlowest account rates')
    print(
        profiles
        .sort_values('account_rate')
        [['economy','region','n','account_rate','internet_use_rate']]
        .head(15)
        .to_string(index=False)
    )


if __name__ == '__main__':
    main()