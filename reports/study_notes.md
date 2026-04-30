# Study notes

## Core project question

Which groups are financially excluded, what predicts financial inclusion, and which policy intervention would likely help most?

## Project mental model

This project treats financial inclusion as a progression:

```text
basic access
→ active use
→ resilience
→ development value
Basic access

Basic access means a person has an account at a financial institution, a mobile money provider, or another formal financial service provider.

In this project, account ownership is the main target because it is the clearest entry point into formal financial inclusion.

Active use

Having an account is not the same as using it.

Active use can include:

making or receiving digital payments
saving formally
borrowing formally
receiving wages or transfers through an account
using mobile money

These variables are important for understanding deeper inclusion, but many of them should not be used as predictors of account ownership because they may happen after a person already has an account.

Resilience

Financial resilience means whether a person can handle a shock, such as a major expense or income loss.

This matters because financial inclusion is not only about access. It is also about whether financial tools help people manage risk.

Digital access

Mobile phone ownership and internet access matter because many financial services now depend on digital channels.

A person may be formally excluded partly because they lack:

a phone
internet access
digital confidence
secure digital identity
trust in digital services
Demographic gaps

Financial exclusion is often unequal across groups.

The main demographic cuts in this project are:

gender
income group
education level
age group
rural or urban residence, if available
labor force status, if available
Development connection

Financial inclusion can matter for development because it can help people:

receive income safely
store money
make payments
save for goals
borrow for productive needs
manage financial shocks
participate in the digital economy
Main caution

This project is descriptive and predictive, not causal.

The model can show which features are associated with account ownership and which profiles are more likely to be excluded.

The model cannot prove that a policy intervention will cause inclusion to improve.


## Why this file matters

This is your “thinking foundation.” Later, when you write the README, model interpretation, and policy recommendation, you will reuse these ideas.

---

# 1.3 Write the concept glossary

Open `references/concept_glossary.md` and paste:

```md
# Concept glossary

## Financial inclusion

Financial inclusion means people can access and use useful financial services, including accounts, payments, savings, credit, and tools for managing financial risk.

## Account ownership

Account ownership means a person has access to an account at a financial institution or through a mobile money service provider.

This is the main target variable for the supervised learning part of the project.

## Financial exclusion

Financial exclusion means a person lacks access to formal or useful financial services.

In this project, a person without an account is treated as financially excluded for the main modeling task.

## Digital payments

Digital payments are payments made or received through digital channels.

They are useful for measuring active financial usage, but they may be downstream from account ownership.

## Mobile money

Mobile money allows people to store, send, and receive money using a mobile phone.

This can be especially important in countries where traditional bank access is limited.

## Formal saving

Formal saving means saving money through a formal financial institution or regulated financial provider.

It shows deeper use of financial services beyond simply owning an account.

## Formal borrowing

Formal borrowing means borrowing from a formal financial institution or regulated lender.

It is useful for understanding access to credit, but borrowing is not automatically good or bad without context.

## Financial resilience

Financial resilience means the ability to handle financial shocks, such as emergency expenses or income loss.

This connects financial inclusion to household stability and development.

## Gender gap

The gender gap measures differences in financial inclusion between men and women.

Example:

```text
gender_gap = account_ownership_men - account_ownership_women
Income gap

The income gap measures differences in financial inclusion between richer and poorer adults.

A common comparison is the wealthiest 60% versus the poorest 40%.

Education gap

The education gap measures differences in financial inclusion by education level.

This can capture differences in literacy, digital confidence, labor market access, and financial knowledge.

Age gap

The age gap measures differences in financial inclusion between younger and older adults.

Younger adults may have different digital access, income stability, employment patterns, and financial needs.

Policy intervention

A policy intervention is an action that could plausibly reduce financial exclusion.

Candidate intervention categories in this project:

mobile access
digital literacy
lower fees
ID or documentation access
trust-building
consumer protection
product design

## Why this file matters

This keeps the project language consistent. You are not just coding; you are building a policy-facing ML project.

---

# 1.4 Define the analytical questions

Open `references/analytical_questions.md` and paste:

```md
# Analytical questions

## Main project question

Which groups are financially excluded, what predicts financial inclusion, and which policy intervention would likely help most?

## Question 1: Country gaps

Which countries have the lowest account ownership rates?

Why it matters:

This identifies where financial exclusion is most severe at the country level.

Expected output:

- ranked table of countries
- bar chart
- optional map

## Question 2: Gender gap

Which countries have the largest gender gap in account ownership?

Why it matters:

Gender gaps show whether financial access is unequal even within the same national context.

Expected output:

- gender gap table
- top 10 largest gaps
- comparison chart

## Question 3: Income and education gaps

Are poorer and less educated adults less likely to own accounts?

Why it matters:

Income and education gaps connect financial inclusion to broader inequality.

Expected output:

- account ownership by income group
- account ownership by education group
- gap summary table

## Question 4: Digital access

Is mobile phone ownership or internet access associated with account ownership and digital payment use?

Why it matters:

Digital access is a plausible policy lever, especially where mobile financial services are important.

Expected output:

- account ownership by mobile phone ownership
- digital payment use by internet access
- scatter plot or grouped bar chart

## Question 5: Prediction

Which features best predict account ownership?

Why it matters:

Prediction helps identify which respondent characteristics are most associated with inclusion or exclusion.

Expected output:

- logistic regression baseline
- boosted tree model
- model comparison table
- feature importance or SHAP explanation

## Question 6: Country clusters

What country groups emerge based on financial inclusion profiles?

Why it matters:

Countries may share similar inclusion patterns even if they are in different regions.

Expected output:

- cluster labels
- cluster profile table
- cluster visualization

## Question 7: Policy recommendation

For the most excluded groups, which intervention appears most plausible?

Candidate interventions:

- mobile access
- digital literacy
- lower fees
- ID or documentation access
- trust-building
- consumer protection
- product design

Why it matters:

The project should end with a practical recommendation, not only analysis.

Expected output:

- policy scorecard
- recommendation table
- limitations note