# Microdata column notes

## File inspected

```text
data/raw/global_findex_2025_microdata/findex_microdata_2025_labelled_update112425.csv

The file has:

144,090 respondent rows
199 columns

The row count was verified by reading the year column and by shell line count.

Core identifier and context columns
Column	Meaning	Project use
year	survey year	metadata
economy	country/economy name	grouping and dashboard
economycode	country/economy code	grouping and joins
regionwb	World Bank region	grouping
pop_adult	adult population	country weighting / context
wpid_random	respondent identifier	row id
wgt	survey weight	weighted EDA
Main target
Column	Meaning	Project role
account	owns an account	target

Observed values:

1 = owns account
0 = does not own account

Observed distribution:

1    106,312
0     37,778
Candidate predictors
Column	Meaning	Project role
female	respondent gender	predictor
age	respondent age	predictor
educ	education level	predictor
inc_q	within-country income quintile	predictor
emp_in	employment status	predictor
urbanicity	urban/rural status	predictor
internet_use	internet use	predictor
economy	country/economy	grouping or optional predictor
regionwb	World Bank region	grouping or optional predictor
Access variables
Column	Meaning	Project role
account_fin	financial institution account	descriptive / component of account
account_mob	mobile money account	descriptive / component of account
account	any account	main target
dig_account	digital account use or digital account measure	descriptive outcome, verify before use
Descriptive financial behavior variables

These are important for analysis but should not be used as predictors in the main account ownership model.

Column	Meaning	Project role
borrowed	borrowing activity	descriptive outcome
saved	saving activity	descriptive outcome
receive_wages	receives wages	descriptive outcome / possible leakage
receive_transfers	receives transfers	descriptive outcome / possible leakage
receive_pensions	receives pensions	descriptive outcome / possible leakage
receive_agriculture	receives agricultural payments	descriptive outcome / possible leakage
merchantpay_dig	digital merchant payment	descriptive outcome / leakage
pay_utilities	utility payment	descriptive outcome / leakage
domestic_remittances	domestic remittances	descriptive outcome
anydigpayment	any digital payment	descriptive outcome / leakage
Connectivity variables
Column	Meaning	Project role
internet_use	internet use	predictor
con1 to con32	digital connectivity module	inspect with questionnaire/codebook
Unknown question-code variables

Most columns are named as question IDs:

fin2 to fin51
fh1 to fh2a
con1 to con32

These need to be mapped using:

references/raw_docs/global_findex_2025_codebook.pdf
references/raw_docs/global_findex_2025_questionnaire.pdf
references/raw_docs/global_findex_2025_connectivity_questionnaire.pdf
references/raw_docs/global_findex_2025_variable_naming_script.r
Missing value caution

Some important behavior variables have 41,136 missing values:

dig_account
borrowed
saved
anydigpayment

These missing values should not be automatically treated as zero.

They may represent module skip patterns, non-applicable questions, or country/module differences.
## Confirmed value labels

| Column | Confirmed labels |
|---|---|
| `female` | 1 = women, 2 = men |
| `educ` | 1 = primary school or less, 2 = secondary school, 3 = tertiary education or more |
| `inc_q` | within-economy household income quintile, 1 to 5 |
| `emp_in` | 1 = in workforce, 2 = out of workforce |
| `urbanicity` | 1 = rural, 2 = urban |
| `account` | 1 = has account, 0 = does not have account |
| `internet_use` | constructed from `con24` and `con25`; exact construction still needs detail |

## Cleaning implications

- Create `is_female` from `female == 1`.
- Create `is_urban` from `urbanicity == 2`.
- Keep `educ` as an ordered categorical variable.
- Keep `inc_q` as an ordered categorical variable.
- Create `is_employed` from `emp_in == 1`.
- Use `account` directly as `has_account`.
- Use `internet_use` as a first-pass predictor, but document its construction.
