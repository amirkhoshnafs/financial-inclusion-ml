# Country cluster analysis

## Purpose

This report clusters economies by their financial inclusion profiles derived from the Global Findex 2025 microdata.

The goal is to identify groups of countries with similar inclusion patterns, not to rank countries by a single metric.

## Features used for clustering

- `account_rate`
- `internet_use_rate`
- `female_account_rate`
- `male_account_rate`
- `gender_gap_male_minus_female`
- `rural_account_rate`
- `urban_account_rate`
- `urban_rural_gap`
- `primary_account_rate`
- `tertiary_account_rate`
- `education_gap_tertiary_minus_primary`
- `poorest_account_rate`
- `richest_account_rate`
- `income_gap_richest_minus_poorest`

## Cluster summary

| cluster | economies | avg account rate | avg internet use | avg gender gap | avg urban-rural gap | avg education gap | avg income gap |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 23 | 35.2% | 58.1% | 14.7% | 8.3% | 47.8% | 20.4% |
| 3 | 31 | 54.0% | 55.8% | 9.1% | 15.8% | 51.8% | 37.4% |
| 0 | 42 | 76.1% | 78.3% | 4.0% | 5.5% | 34.7% | 20.4% |
| 1 | 44 | 95.5% | 89.9% | 1.4% | 0.4% | 8.4% | 5.8% |

## Cluster members

### Cluster 2

| economy | region | account rate | internet use rate |
|---|---|---:|---:|
| Niger | Sub-Saharan Africa (excluding high income) | 14.8% | 15.6% |
| Chad | Sub-Saharan Africa (excluding high income) | 20.9% | 11.4% |
| Lebanon | Middle East & North Africa (excluding high income) | 23.0% | 94.2% |
| Nicaragua | Latin America & Caribbean (excluding high income) | 23.5% | 74.7% |
| Madagascar | Sub-Saharan Africa (excluding high income) | 24.5% | 11.1% |
| Pakistan | South Asia | 27.3% | 35.7% |
| Mauritania | Sub-Saharan Africa (excluding high income) | 27.3% | 59.8% |
| Iraq | Middle East & North Africa (excluding high income) | 30.2% | 76.2% |
| Libya | Middle East & North Africa (excluding high income) | 33.1% | 80.5% |
| Algeria | Middle East & North Africa (excluding high income) | 35.3% | 82.9% |
| Guinea | Sub-Saharan Africa (excluding high income) | 36.0% | 31.0% |
| Tunisia | Middle East & North Africa (excluding high income) | 37.8% | 68.0% |
| Gambia, The | Sub-Saharan Africa (excluding high income) | 38.2% | 64.8% |
| Guatemala | Latin America & Caribbean (excluding high income) | 38.3% | 71.1% |
| Congo, Dem. Rep. | Sub-Saharan Africa (excluding high income) | 39.2% | 32.1% |
| West Bank and Gaza | Middle East & North Africa (excluding high income) | 39.6% | 94.1% |
| Honduras | Latin America & Caribbean (excluding high income) | 42.4% | 75.3% |
| Egypt, Arab Rep. | Middle East & North Africa (excluding high income) | 43.1% | 54.9% |
| Bangladesh | South Asia | 43.3% | 43.6% |
| Morocco | Middle East & North Africa (excluding high income) | 44.4% | 64.8% |
| Comoros | Sub-Saharan Africa (excluding high income) | 45.5% | 43.4% |
| Jordan | Middle East & North Africa (excluding high income) | 46.5% | 89.3% |
| Tajikistan | Europe & Central Asia (excluding high income) | 54.5% | 62.5% |

### Cluster 3

| economy | region | account rate | internet use rate |
|---|---|---:|---:|
| Lao PDR | East Asia & Pacific (excluding high income) | 37.7% | 70.2% |
| Sierra Leone | Sub-Saharan Africa (excluding high income) | 38.6% | 32.8% |
| Cambodia | East Asia & Pacific (excluding high income) | 39.0% | 81.0% |
| El Salvador | Latin America & Caribbean (excluding high income) | 43.4% | 80.8% |
| Albania | Europe & Central Asia (excluding high income) | 46.1% | 82.8% |
| Ethiopia | Sub-Saharan Africa (excluding high income) | 48.8% | 13.8% |
| Zimbabwe | Sub-Saharan Africa (excluding high income) | 49.5% | 31.6% |
| Philippines | East Asia & Pacific (excluding high income) | 50.2% | 70.7% |
| Malawi | Sub-Saharan Africa (excluding high income) | 50.4% | 20.5% |
| Burkina Faso | Sub-Saharan Africa (excluding high income) | 51.4% | 31.3% |
| Benin | Sub-Saharan Africa (excluding high income) | 51.8% | 34.3% |
| Liberia | Sub-Saharan Africa (excluding high income) | 52.2% | 32.9% |
| Mexico | Latin America & Caribbean (excluding high income) | 53.0% | 77.5% |
| Mozambique | Sub-Saharan Africa (excluding high income) | 54.4% | 27.1% |
| Mali | Sub-Saharan Africa (excluding high income) | 54.7% | 46.0% |
| Moldova | Europe & Central Asia (excluding high income) | 55.5% | 78.7% |
| Congo, Rep. | Sub-Saharan Africa (excluding high income) | 55.6% | 33.9% |
| Azerbaijan | Europe & Central Asia (excluding high income) | 56.3% | 86.4% |
| Indonesia | East Asia & Pacific (excluding high income) | 56.3% | 70.5% |
| Bolivia | Latin America & Caribbean (excluding high income) | 56.8% | 79.1% |
| Colombia | Latin America & Caribbean (excluding high income) | 57.1% | 80.7% |
| Togo | Sub-Saharan Africa (excluding high income) | 57.4% | 43.7% |
| Cote d'Ivoire | Sub-Saharan Africa (excluding high income) | 57.6% | 47.2% |
| Peru | Latin America & Caribbean (excluding high income) | 59.3% | 78.1% |
| Tanzania | Sub-Saharan Africa (excluding high income) | 59.8% | 20.4% |
| Cameroon | Sub-Saharan Africa (excluding high income) | 60.9% | 46.2% |
| Paraguay | Latin America & Caribbean (excluding high income) | 60.9% | 83.8% |
| Botswana | Sub-Saharan Africa (excluding high income) | 61.4% | 47.3% |
| Nigeria | Sub-Saharan Africa (excluding high income) | 63.3% | 37.7% |
| Panama | High income | 64.1% | 75.1% |
| Viet Nam | East Asia & Pacific (excluding high income) | 70.6% | 87.9% |

### Cluster 0

| economy | region | account rate | internet use rate |
|---|---|---:|---:|
| Uzbekistan | Europe & Central Asia (excluding high income) | 59.7% | 73.7% |
| Nepal | South Asia | 60.0% | 50.1% |
| Lesotho | Sub-Saharan Africa (excluding high income) | 61.6% | 45.9% |
| Kosovo | Europe & Central Asia (excluding high income) | 64.2% | 95.8% |
| Ecuador | Latin America & Caribbean (excluding high income) | 64.5% | 82.8% |
| Dominican Republic | Latin America & Caribbean (excluding high income) | 64.8% | 89.3% |
| Eswatini | Sub-Saharan Africa (excluding high income) | 65.1% | 51.6% |
| Belize | Latin America & Caribbean (excluding high income) | 68.0% | 86.0% |
| Gabon | Sub-Saharan Africa (excluding high income) | 68.2% | 68.7% |
| Oman | High income | 69.5% | 92.5% |
| Romania | High income | 71.3% | 76.9% |
| Costa Rica | Latin America & Caribbean (excluding high income) | 71.4% | 87.4% |
| Armenia | Europe & Central Asia (excluding high income) | 71.4% | 87.5% |
| Kyrgyz Republic | Europe & Central Asia (excluding high income) | 72.3% | 92.0% |
| Zambia | Sub-Saharan Africa (excluding high income) | 72.7% | 38.9% |
| Uganda | Sub-Saharan Africa (excluding high income) | 72.8% | 38.2% |
| Namibia | Sub-Saharan Africa (excluding high income) | 72.9% | 56.4% |
| Uruguay | High income | 73.7% | 91.3% |
| Kuwait | High income | 74.5% | 96.0% |
| Trinidad and Tobago | High income | 74.6% | 86.0% |
| Montenegro | Europe & Central Asia (excluding high income) | 75.4% | 83.8% |
| Senegal | Sub-Saharan Africa (excluding high income) | 76.5% | 70.1% |
| Bosnia and Herzegovina | Europe & Central Asia (excluding high income) | 77.5% | 84.8% |
| Georgia | Europe & Central Asia (excluding high income) | 78.8% | 81.9% |
| Saudi Arabia | High income | 78.8% | 99.1% |
| Russian Federation | Europe & Central Asia (excluding high income) | 79.3% | 92.9% |
| South Africa | Sub-Saharan Africa (excluding high income) | 81.1% | 68.3% |
| Ghana | Sub-Saharan Africa (excluding high income) | 81.2% | 54.8% |
| Turkiye | Europe & Central Asia (excluding high income) | 81.6% | 87.5% |
| Sri Lanka | South Asia | 81.7% | 43.0% |
| Argentina | Latin America & Caribbean (excluding high income) | 81.7% | 88.1% |
| Bahrain | High income | 82.3% | 97.5% |
| Serbia | Europe & Central Asia (excluding high income) | 83.3% | 79.2% |
| North Macedonia | Europe & Central Asia (excluding high income) | 84.3% | 83.2% |
| Bulgaria | Europe & Central Asia (excluding high income) | 84.7% | 79.4% |
| Chile | High income | 85.1% | 86.7% |
| Poland | High income | 86.1% | 80.9% |
| Brazil | Latin America & Caribbean (excluding high income) | 86.4% | 87.5% |
| Hungary | High income | 87.0% | 90.8% |
| Kazakhstan | Europe & Central Asia (excluding high income) | 87.0% | 88.4% |
| Israel | High income | 89.3% | 86.1% |
| Slovak Republic | High income | 92.2% | 87.8% |

### Cluster 1

| economy | region | account rate | internet use rate |
|---|---|---:|---:|
| Italy | High income | 86.0% | 89.4% |
| Venezuela, RB | Latin America & Caribbean (excluding high income) | 87.3% | 89.4% |
| Ukraine | Europe & Central Asia (excluding high income) | 87.6% | 94.9% |
| Greece | High income | 88.6% | 91.2% |
| Malaysia | East Asia & Pacific (excluding high income) | 88.7% | 86.9% |
| India | South Asia | 89.0% | 45.7% |
| China | East Asia & Pacific (excluding high income) | 89.4% | 86.2% |
| Mauritius | Sub-Saharan Africa (excluding high income) | 89.6% | 77.2% |
| Kenya | Sub-Saharan Africa (excluding high income) | 90.1% | 60.5% |
| Iran, Islamic Rep. | Middle East & North Africa (excluding high income) | 91.1% | 77.5% |
| Portugal | High income | 91.4% | 86.3% |
| Thailand | East Asia & Pacific (excluding high income) | 91.8% | 85.8% |
| Czechia | High income | 92.3% | 92.9% |
| Croatia | High income | 92.6% | 87.4% |
| Latvia | High income | 95.0% | 93.7% |
| Taiwan, China | High income | 95.6% | 90.2% |
| Cyprus | High income | 96.1% | 90.3% |
| Malta | High income | 96.6% | 92.7% |
| Korea, Rep. | High income | 96.9% | 86.6% |
| United States | High income | 97.0% | 97.8% |
| Hong Kong SAR, China | High income | 97.3% | 88.5% |
| New Zealand | High income | 97.9% | 95.5% |
| Singapore | High income | 98.0% | 92.9% |
| Australia | High income | 98.0% | 92.3% |
| Belgium | High income | 98.2% | 95.0% |
| Mongolia | East Asia & Pacific (excluding high income) | 98.3% | 86.9% |
| Ireland | High income | 98.3% | 94.8% |
| Germany | High income | 98.3% | 95.1% |
| Spain | High income | 98.4% | 96.5% |
| Canada | High income | 98.4% | 95.1% |
| Switzerland | High income | 98.4% | 94.4% |
| Japan | High income | 98.5% | 83.3% |
| Norway | High income | 98.6% | 98.2% |
| Sweden | High income | 98.6% | 98.3% |
| Denmark | High income | 98.7% | 98.2% |
| Slovenia | High income | 98.7% | 87.6% |
| Estonia | High income | 98.9% | 97.2% |
| Lithuania | High income | 99.0% | 89.0% |
| Netherlands | High income | 99.2% | 95.9% |
| France | High income | 99.2% | 96.4% |
| United Kingdom | High income | 99.3% | 96.2% |
| Austria | High income | 99.5% | 93.8% |
| Finland | High income | 99.8% | 93.9% |
| Iceland | High income | 99.9% | 98.8% |

## Interpretation notes

- Clusters are descriptive groups, not causal categories.
- Cluster labels are arbitrary numbers assigned by KMeans.
- The clusters depend on the selected country-level features.
- Missing country-level subgroup rates are median-imputed before clustering.

## Generated figure

- `figures/country_clusters.png`