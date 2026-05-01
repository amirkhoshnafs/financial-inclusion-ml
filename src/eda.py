import pandas as pd


def weighted_mean(
    df,
    value_col,
    weight_col='survey_weight',
):
    x=df[[value_col, weight_col]].dropna()
    if len(x) == 0:
        return pd.NA
    return (x[value_col] * x[weight_col]).sum() / x[weight_col].sum()


def weighted_count(
    df,
    weight_col='survey_weight',
):
    return df[weight_col].dropna().sum()


def grouped_weighted_rate(
    df,
    group_cols,
    value_col='has_account',
    weight_col='survey_weight',
    min_n=100,
):
    if isinstance(group_cols, str):
        group_cols=[group_cols]

    rows=[]
    for keys, g in df.groupby(group_cols, dropna=False, observed=False):
        if not isinstance(keys, tuple):
            keys=(keys,)

        n=len(g)
        if n < min_n:
            continue

        row={col:key for col, key in zip(group_cols, keys)}
        row['n']=n
        row['weighted_n']=weighted_count(g, weight_col)
        row[f'{value_col}_rate']=weighted_mean(g, value_col, weight_col)
        rows.append(row)

    out=pd.DataFrame(rows)
    if len(out) == 0:
        return out

    return out.sort_values(f'{value_col}_rate')


def add_age_group(df):
    out=df.copy()
    bins=[14,24,34,44,54,64,200]
    labels=['15-24','25-34','35-44','45-54','55-64','65+']
    out['age_group']=pd.cut(out['age'], bins=bins, labels=labels)
    return out


def add_readable_flags(df):
    out=df.copy()

    out['gender']=out['is_female'].map({
        1:'women',
        0:'men',
    }).astype('string')

    out['employment_status']=out['is_employed'].map({
        1:'in_workforce',
        0:'out_of_workforce',
    }).astype('string')

    out['urbanicity']=out['is_urban'].map({
        1:'urban',
        0:'rural',
    }).astype('string')

    out['internet_status']=out['uses_internet'].map({
        1:'uses_internet',
        0:'does_not_use_internet',
    }).astype('string')

    return out


def account_summary(df):
    return pd.Series({
        'rows':len(df),
        'weighted_account_rate':weighted_mean(df, 'has_account'),
        'unweighted_account_rate':df['has_account'].mean(),
        'excluded_rows':int((df['has_account'] == 0).sum()),
        'included_rows':int((df['has_account'] == 1).sum()),
    })


def gap_between_groups(
    table,
    group_col,
    rate_col='has_account_rate',
    high_group=None,
    low_group=None,
):
    x=table[[group_col, rate_col]].dropna()

    if high_group is not None and low_group is not None:
        high=x.loc[x[group_col].eq(high_group), rate_col]
        low=x.loc[x[group_col].eq(low_group), rate_col]
        if len(high) == 0 or len(low) == 0:
            return pd.NA
        return float(high.iloc[0] - low.iloc[0])

    return float(x[rate_col].max() - x[rate_col].min())