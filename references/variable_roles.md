# Variable roles

This file defines how variables should be used in the project.

The exact raw variable names will be filled in after data acquisition.

## Target variable

### account_ownership

Role:

```text
target

Meaning:

Whether a respondent owns an account at a financial institution or with a mobile money service provider.

Used in:

classification model
exclusion definition
demographic gap analysis
Core predictor variables

These variables may be used to predict account ownership if available.

gender

Role:

predictor

Why:

Financial inclusion often differs by gender.

age_group

Role:

predictor

Why:

Financial inclusion may differ between younger and older adults.

education_level

Role:

predictor

Why:

Education may relate to financial literacy, employment, digital confidence, and account access.

income_group

Role:

predictor

Why:

Income affects ability and need to access formal financial services.

mobile_phone_ownership

Role:

predictor

Why:

Mobile access may enable mobile money and digital financial services.

internet_access_or_use

Role:

predictor

Why:

Internet access may support digital payments and account usage.

labor_force_status

Role:

predictor_optional

Why:

Employment may affect account ownership through wages, income stability, and formal payment channels.

rural_urban

Role:

predictor_optional

Why:

Financial access may differ between rural and urban areas.

country

Role:

predictor_or_group

Why:

Country context strongly affects financial inclusion.

Caution:

If country is included directly in the model, the model may learn country-level differences instead of individual-level patterns. We may compare models with and without country.

Descriptive outcome variables

These variables are important for analysis but should usually not predict account ownership.

digital_payment_use

Role:

descriptive_outcome

Why:

Digital payments show active financial use.

Leakage risk:

High. Digital payment use may depend on having an account.

saved_formally

Role:

descriptive_outcome

Why:

Formal saving shows deeper financial inclusion.

Leakage risk:

High. Formal saving may require an account.

borrowed_formally

Role:

descriptive_outcome

Why:

Formal borrowing shows access to credit.

Leakage risk:

Medium to high. It may depend on formal financial access.

financial_resilience

Role:

descriptive_outcome

Why:

Financial resilience connects inclusion to ability to handle shocks.

Leakage risk:

Medium. It may be partly affected by financial inclusion.

Barrier variables

These should be used for policy interpretation, not for predicting account ownership.

Examples:

too expensive
too far away
lack of documentation
lack of trust
religious reasons
someone else in family has account
no need for account
lack of money

Role:

policy_barrier

Why:

These variables often apply only to people without accounts, so using them in the prediction model would leak target information.

Leakage checklist

Do not use a feature in the account ownership model if:

it directly requires having an account
it happens after account ownership
it is only asked to people without accounts
it mechanically reveals the target
it is a financial behavior outcome rather than a background characteristic

## Why this file matters

This is one of the most important project-quality files.

It shows that you understand **target leakage**, which is a big applied ML skill.

---

# 1.6 Add official source notes

Now update `references/project_decisions.md` by adding this section at the bottom:

```md
## Official source notes

The Global Findex is the main data source for this project.

Useful official source pages:

```text
https://www.worldbank.org/en/publication/globalfindex
https://www.worldbank.org/en/publication/globalfindex/report
https://www.worldbank.org/en/publication/globalfindex/download-data
https://www.worldbank.org/en/topic/financialinclusion/overview

Key source facts to verify during data acquisition:

Which edition is used: 2025 or 2021.
Whether microdata access is available.
Whether country-level indicators are downloaded as CSV, XLSX, or DTA.
Whether variable names match the questionnaire and codebook.
Whether survey weights are available and documented.

The official Findex page describes the database as a demand-side survey on how adults access and use financial services, and the 2025 release adds a Digital Connectivity Tracker measuring access to and use of mobile technology.  The World Bank’s financial inclusion overview also frames inclusive finance as connected to growth and resilience, while noting that digital financial services can reduce costs and expand access but also create consumer and cyber risks.

---

# 1.7 Mentor explanation: the project logic

Here is the logic we will follow for the whole project:

```text
Who lacks access?
→ demographic gap analysis

What predicts access?
→ classification model

Why might they lack access?
→ barrier variables and subgroup analysis

Which countries look similar?
→ country clustering

Which intervention is plausible?
→ policy scorecard

How do we communicate it?
→ dashboard and README