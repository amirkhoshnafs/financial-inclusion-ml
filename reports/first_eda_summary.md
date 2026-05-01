# First EDA summary

This report summarizes first-pass account ownership patterns from the cleaned Global Findex 2025 microdata.

## Overall account ownership

- Rows: 144,090
- Weighted account ownership rate: 71.0%
- Unweighted account ownership rate: 73.8%
- Excluded rows: 37,778
- Included rows: 106,312

## Account ownership by gender

| gender   |     n |   weighted_n | has_account_rate   |
|:---------|------:|-------------:|:-------------------|
| women    | 75580 |        73278 | 68.1%              |
| men      | 68510 |        70812 | 74.1%              |


## Account ownership by education

| education_level   |     n |   weighted_n | has_account_rate   |
|:------------------|------:|-------------:|:-------------------|
| primary_or_less   | 38398 |        50373 | 51.9%              |
| <NA>              |   588 |          672 | 64.5%              |
| secondary         | 74624 |        70657 | 77.7%              |
| tertiary_or_more  | 30480 |        22387 | 93.4%              |


## Account ownership by income quintile

| income_quintile   |     n |   weighted_n | has_account_rate   |
|:------------------|------:|-------------:|:-------------------|
| 1                 | 23851 |        28525 | 61.1%              |
| <NA>              |  1020 |         1020 | 61.6%              |
| 2                 | 25615 |        28592 | 67.1%              |
| 3                 | 27916 |        28601 | 71.6%              |
| 4                 | 30139 |        28632 | 75.2%              |
| 5                 | 35549 |        28720 | 80.6%              |


## Account ownership by employment

| employment_status   |     n |   weighted_n | has_account_rate   |
|:--------------------|------:|-------------:|:-------------------|
| out_of_workforce    | 56205 |        57658 | 61.7%              |
| in_workforce        | 83865 |        82412 | 76.7%              |
| <NA>                |  4020 |         4020 | 89.4%              |


## Account ownership by urbanicity

| urbanicity   |     n |   weighted_n | has_account_rate   |
|:-------------|------:|-------------:|:-------------------|
| rural        | 79534 |        80362 | 66.3%              |
| urban        | 62030 |        61084 | 76.6%              |
| <NA>         |  2526 |         2644 | 87.4%              |


## Account ownership by internet use

| internet_status       |      n |   weighted_n | has_account_rate   |
|:----------------------|-------:|-------------:|:-------------------|
| does_not_use_internet |  35529 |        38367 | 46.5%              |
| uses_internet         | 108561 |       105723 | 80.0%              |


## Account ownership by age group

| age_group   |     n |   weighted_n | has_account_rate   |
|:------------|------:|-------------:|:-------------------|
| 15-24       | 25252 |        31090 | 57.0%              |
| 25-34       | 29544 |        29521 | 73.6%              |
| 45-54       | 21460 |        21234 | 75.0%              |
| 35-44       | 26813 |        25987 | 75.0%              |
| 55-64       | 18788 |        17043 | 75.4%              |
| 65+         | 22233 |        19214 | 76.5%              |


## Account ownership by region

| region                                             |     n |   weighted_n | has_account_rate   |
|:---------------------------------------------------|------:|-------------:|:-------------------|
| Middle East & North Africa (excluding high income) | 10046 |        10046 | 42.4%              |
| Sub-Saharan Africa (excluding high income)         | 35093 |        35093 | 55.6%              |
| Latin America & Caribbean (excluding high income)  | 15696 |        15696 | 59.3%              |
| South Asia                                         |  7000 |         7000 | 68.5%              |
| Europe & Central Asia (excluding high income)      | 18000 |        18000 | 72.2%              |
| East Asia & Pacific (excluding high income)        | 12088 |        12088 | 74.1%              |
| High income                                        | 46167 |        46167 | 92.1%              |


## Lowest account ownership countries

| economy     |    n |   weighted_n | has_account_rate   |
|:------------|-----:|-------------:|:-------------------|
| Niger       | 1000 |         1000 | 14.8%              |
| Chad        | 1000 |         1000 | 20.9%              |
| Lebanon     | 1010 |         1010 | 23.0%              |
| Nicaragua   | 1130 |         1130 | 23.5%              |
| Madagascar  | 1000 |         1000 | 24.5%              |
| Pakistan    | 1000 |         1000 | 27.3%              |
| Mauritania  | 1000 |         1000 | 27.3%              |
| Iraq        | 1000 |         1000 | 30.2%              |
| Libya       | 1000 |         1000 | 33.1%              |
| Algeria     | 1007 |         1007 | 35.3%              |
| Guinea      | 1000 |         1000 | 36.0%              |
| Lao PDR     | 1000 |         1000 | 37.7%              |
| Tunisia     | 1000 |         1000 | 37.8%              |
| Gambia, The | 1008 |         1008 | 38.2%              |
| Guatemala   | 1000 |         1000 | 38.3%              |


## Highest account ownership countries

| economy        |    n |   weighted_n | has_account_rate   |
|:---------------|-----:|-------------:|:-------------------|
| Iceland        |  500 |          500 | 99.9%              |
| Finland        | 1000 |         1000 | 99.8%              |
| Austria        | 1000 |         1000 | 99.5%              |
| United Kingdom | 1000 |         1000 | 99.3%              |
| France         | 1000 |         1000 | 99.2%              |
| Netherlands    | 1004 |         1004 | 99.2%              |
| Lithuania      | 1012 |         1012 | 99.0%              |
| Estonia        | 1006 |         1006 | 98.9%              |
| Slovenia       | 1001 |         1001 | 98.7%              |
| Denmark        | 1005 |         1005 | 98.7%              |
| Sweden         | 1004 |         1004 | 98.6%              |
| Norway         | 1007 |         1007 | 98.6%              |
| Japan          | 1008 |         1008 | 98.5%              |
| Switzerland    | 1000 |         1000 | 98.4%              |
| Canada         | 1024 |         1024 | 98.4%              |
