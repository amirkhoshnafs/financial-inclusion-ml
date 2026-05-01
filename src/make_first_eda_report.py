import pandas as pd

from src.config import INTERIM_DIR, REPORTS_DIR
from src.eda import (
    account_summary,
    add_age_group,
    add_readable_flags,
    grouped_weighted_rate,
)

IN_PATH=INTERIM_DIR / 'microdata_core.parquet'
OUT_PATH=REPORTS_DIR / 'first_eda_summary.md'


def fmt_pct(x):
    if pd.isna(x):
        return ''
    return f'{100 * x:.1f}%'


def format_table(df):
    out=df.copy()
    for col in out.columns:
        if col.endswith('_rate'):
            out[col]=out[col].map(fmt_pct)
        if col == 'weighted_n':
            out[col]=out[col].round(0).astype('Int64')
    return out.to_markdown(index=False)


def write_section(lines, title, table):
    lines.append(f'\n## {title}\n')
    lines.append(format_table(table))
    lines.append('')


def main():
    df=pd.read_parquet(IN_PATH)
    df=add_age_group(df)
    df=add_readable_flags(df)

    summary=account_summary(df)

    lines=[
        '# First EDA summary',
        '',
        'This report summarizes first-pass account ownership patterns from the cleaned Global Findex 2025 microdata.',
        '',
        '## Overall account ownership',
        '',
        f'- Rows: {summary["rows"]:,.0f}',
        f'- Weighted account ownership rate: {fmt_pct(summary["weighted_account_rate"])}',
        f'- Unweighted account ownership rate: {fmt_pct(summary["unweighted_account_rate"])}',
        f'- Excluded rows: {summary["excluded_rows"]:,.0f}',
        f'- Included rows: {summary["included_rows"]:,.0f}',
    ]

    write_section(lines, 'Account ownership by gender', grouped_weighted_rate(df, 'gender'))
    write_section(lines, 'Account ownership by education', grouped_weighted_rate(df, 'education_level'))
    write_section(lines, 'Account ownership by income quintile', grouped_weighted_rate(df, 'income_quintile'))
    write_section(lines, 'Account ownership by employment', grouped_weighted_rate(df, 'employment_status'))
    write_section(lines, 'Account ownership by urbanicity', grouped_weighted_rate(df, 'urbanicity'))
    write_section(lines, 'Account ownership by internet use', grouped_weighted_rate(df, 'internet_status'))
    write_section(lines, 'Account ownership by age group', grouped_weighted_rate(df, 'age_group'))
    write_section(lines, 'Account ownership by region', grouped_weighted_rate(df, 'region'))

    country=grouped_weighted_rate(df, 'economy', min_n=300)
    country_low=country.head(15)
    country_high=country.tail(15).sort_values('has_account_rate', ascending=False)

    write_section(lines, 'Lowest account ownership countries', country_low)
    write_section(lines, 'Highest account ownership countries', country_high)

    OUT_PATH.write_text('\n'.join(lines), encoding='utf-8')

    print('saved')
    print(OUT_PATH)


if __name__ == '__main__':
    main()