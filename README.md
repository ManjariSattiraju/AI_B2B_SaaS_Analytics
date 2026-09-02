# AI-Enhanced B2B SaaS Customer & Revenue Intelligence

An end-to-end analytics project analyzing customer churn, subscription behavior, product usage, and support activity for a fictional B2B SaaS company, RavenStack.

The project combines **Python/Pandas analytics, Streamlit visualization, and a grounded AI Analyst** to turn customer data into actionable business insights.

## 🚀 Project Overview

B2B SaaS companies need to understand not only **who is churning**, but also **why customers are leaving and which customer behaviors may be associated with churn**.

This project analyzes five interconnected datasets to answer questions around:

- Customer churn
- Industry-level churn patterns
- Subscription behavior
- Upgrades and downgrades
- Product and feature usage
- Support tickets and escalations
- Customer satisfaction
- Churn reasons
- AI-assisted business interpretation

The analytical findings are calculated using Python and Pandas first. The AI layer is then used to interpret these validated findings conversationally rather than independently performing the analysis.

---

## 🎯 Business Questions

The analysis focuses on questions such as:

1. Which industries have the highest churn?
2. Is churn concentrated in a particular subscription plan?
3. Are subscription upgrades or downgrades associated with churn?
4. Does product usage differ between churned and non-churned customers?
5. Is support activity associated with customer churn?
6. What are the major reasons customers leave?
7. Are there industry-specific churn patterns?
8. Can an AI assistant explain the analytical findings in a business-friendly way?

---

## 🗂️ Dataset

The project uses a synthetic RavenStack dataset containing:

| Dataset | Records | Description |
|---|---:|---|
| `ravenstack_accounts.csv` | 500 | Customer account information |
| `ravenstack_subscriptions.csv` | 5,000 | Subscription and plan information |
| `ravenstack_feature_usage.csv` | 25,000 | Product and feature usage |
| `ravenstack_support_tickets.csv` | 2,000 | Customer support interactions |
| `ravenstack_churn_events.csv` | 600 | Customer churn events |

---

## 🔍 Key Findings

### Industry Churn

Overall churn across the analyzed accounts was approximately **22%**.

| Industry | Churn Rate |
|---|---:|
| DevTools | **30.97%** |
| FinTech | 22.32% |
| HealthTech | 21.88% |
| EdTech | 16.46% |
| Cybersecurity | 16.00% |

DevTools showed the highest churn rate, approximately **9 percentage points above the overall churn rate**.

---

### Subscription Plan Churn

Churn was remarkably similar across plans:

- Basic: **22.02%**
- Enterprise: **22.08%**
- Pro: **21.91%**

This suggests that, within this dataset, **subscription plan alone does not appear to be a strong differentiator of churn**.

---

### Product Usage

Average product usage was slightly higher among churned subscriptions:

| Metric | Non-Churned | Churned |
|---|---:|---:|
| Total Usage | 495.13 | 522.04 |
| Total Duration (seconds) | 150,350.88 | 158,347.54 |
| Total Errors | 28.23 | 28.15 |

The differences are relatively small, so product usage does **not appear to be a strong standalone differentiator of churn** in this analysis.

---

### Support Activity

Support activity was analyzed at the account level using ticket volume, resolution time, response time, satisfaction, and escalations.

The analysis found broadly similar ticket volumes and satisfaction between churned and non-churned accounts.

Escalation rates showed a potentially interesting difference and may warrant further investigation, but the analysis does not establish causation.

---

### Churn Reasons

The churn event data includes several reason categories:

- Features
- Support
- Budget
- Competitor
- Pricing
- Unknown

The importance of these reasons varies across industries.

For example, **DevTools** showed relatively high counts for budget and support-related churn, while **EdTech** had a larger share of feature-related churn.

---

## 🤖 AI Analyst

The project includes an AI Analyst built into the Streamlit application.

Instead of allowing the AI to independently analyze the raw dataset, the project follows a more controlled approach:

```text
Raw Data
   ↓
Python / Pandas Analysis
   ↓
Validated Business Findings
   ↓
AI Analyst
   ↓
Natural-Language Explanation





