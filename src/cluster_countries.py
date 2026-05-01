import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.config import FIGURES_DIR, PROCESSED_DIR, REPORTS_DIR, RANDOM_STATE

IN_PATH=PROCESSED_DIR / 'country_profiles.parquet'
OUT_PATH=PROCESSED_DIR / 'country_clusters.parquet'
REPORT_PATH=REPORTS_DIR / 'country_clusters.md'
FIGURE_PATH=FIGURES_DIR / 'country_clusters.png'

N_CLUSTERS=4

CLUSTER_FEATURES=[
    'account_rate',
    'internet_use_rate',
    'female_account_rate',
    'male_account_rate',
    'gender_gap_male_minus_female',
    'rural_account_rate',
    'urban_account_rate',
    'urban_rural_gap',
    'primary_account_rate',
    'tertiary_account_rate',
    'education_gap_tertiary_minus_primary',
    'poorest_account_rate',
    'richest_account_rate',
    'income_gap_richest_minus_poorest',
]


def load_profiles():
    return pd.read_parquet(IN_PATH)


def fit_clusters(df):
    x=df[CLUSTER_FEATURES].copy()

    preprocess=Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
    ])

    x_scaled=preprocess.fit_transform(x)

    kmeans=KMeans(
        n_clusters=N_CLUSTERS,
        random_state=RANDOM_STATE,
        n_init=20,
    )

    clusters=kmeans.fit_predict(x_scaled)

    pca=PCA(n_components=2, random_state=RANDOM_STATE)
    coords=pca.fit_transform(x_scaled)

    out=df.copy()
    out['cluster']=clusters
    out['pca_x']=coords[:,0]
    out['pca_y']=coords[:,1]

    return out, pca


def cluster_summary(df):
    summary=(
        df.groupby('cluster')
        .agg(
            economies=('economy','count'),
            avg_account_rate=('account_rate','mean'),
            avg_internet_use_rate=('internet_use_rate','mean'),
            avg_gender_gap=('gender_gap_male_minus_female','mean'),
            avg_urban_rural_gap=('urban_rural_gap','mean'),
            avg_education_gap=('education_gap_tertiary_minus_primary','mean'),
            avg_income_gap=('income_gap_richest_minus_poorest','mean'),
        )
        .reset_index()
        .sort_values('avg_account_rate')
    )

    return summary


def fmt_pct(x):
    if pd.isna(x):
        return ''
    return f'{100 * x:.1f}%'


def make_report(df, summary):
    lines=[
        '# Country cluster analysis',
        '',
        '## Purpose',
        '',
        'This report clusters economies by their financial inclusion profiles derived from the Global Findex 2025 microdata.',
        '',
        'The goal is to identify groups of countries with similar inclusion patterns, not to rank countries by a single metric.',
        '',
        '## Features used for clustering',
        '',
    ]

    for col in CLUSTER_FEATURES:
        lines.append(f'- `{col}`')

    lines.extend([
        '',
        '## Cluster summary',
        '',
        '| cluster | economies | avg account rate | avg internet use | avg gender gap | avg urban-rural gap | avg education gap | avg income gap |',
        '|---:|---:|---:|---:|---:|---:|---:|---:|',
    ])

    for row in summary.itertuples(index=False):
        lines.append(
            f'| {row.cluster} | '
            f'{row.economies} | '
            f'{fmt_pct(row.avg_account_rate)} | '
            f'{fmt_pct(row.avg_internet_use_rate)} | '
            f'{fmt_pct(row.avg_gender_gap)} | '
            f'{fmt_pct(row.avg_urban_rural_gap)} | '
            f'{fmt_pct(row.avg_education_gap)} | '
            f'{fmt_pct(row.avg_income_gap)} |'
        )

    lines.extend([
        '',
        '## Cluster members',
        '',
    ])

    for cluster in summary['cluster']:
        members=(
            df[df['cluster'].eq(cluster)]
            .sort_values('account_rate')
            [['economy','region','account_rate','internet_use_rate']]
        )

        lines.extend([
            f'### Cluster {cluster}',
            '',
            '| economy | region | account rate | internet use rate |',
            '|---|---|---:|---:|',
        ])

        for row in members.itertuples(index=False):
            lines.append(
                f'| {row.economy} | '
                f'{row.region} | '
                f'{fmt_pct(row.account_rate)} | '
                f'{fmt_pct(row.internet_use_rate)} |'
            )

        lines.append('')

    lines.extend([
        '## Interpretation notes',
        '',
        '- Clusters are descriptive groups, not causal categories.',
        '- Cluster labels are arbitrary numbers assigned by KMeans.',
        '- The clusters depend on the selected country-level features.',
        '- Missing country-level subgroup rates are median-imputed before clustering.',
        '',
        '## Generated figure',
        '',
        '- `figures/country_clusters.png`',
    ])

    REPORT_PATH.write_text('\n'.join(lines), encoding='utf-8')


def make_plot(df):
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax=plt.subplots(figsize=(8,6))

    for cluster, g in df.groupby('cluster'):
        ax.scatter(g['pca_x'], g['pca_y'], label=f'Cluster {cluster}', alpha=0.8)

    for row in df.sort_values('account_rate').head(10).itertuples(index=False):
        ax.text(row.pca_x, row.pca_y, row.economy, fontsize=8)

    ax.set_title('Country clusters by financial inclusion profile')
    ax.set_xlabel('PCA component 1')
    ax.set_ylabel('PCA component 2')
    ax.legend()

    fig.tight_layout()
    fig.savefig(FIGURE_PATH, dpi=160, bbox_inches='tight')
    plt.close(fig)


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    profiles=load_profiles()
    clustered, _=fit_clusters(profiles)
    summary=cluster_summary(clustered)

    clustered.to_parquet(OUT_PATH, index=False)
    make_report(clustered, summary)
    make_plot(clustered)

    print('saved clusters')
    print(OUT_PATH)

    print('\nsaved report')
    print(REPORT_PATH)

    print('\nsaved figure')
    print(FIGURE_PATH)

    print('\ncluster summary')
    print(summary.to_string(index=False))


if __name__ == '__main__':
    main()