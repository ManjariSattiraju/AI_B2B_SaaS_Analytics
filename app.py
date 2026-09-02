import streamlit as st
import pandas as pd
from openai import OpenAI


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="RavenStack Churn Analysis",
    page_icon="📊",
    layout="wide"
)


# =====================================================
# OPENAI CLIENT
# =====================================================

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


# =====================================================
# LOAD DATA
# =====================================================

accounts = pd.read_csv("ravenstack_accounts.csv")
subscriptions = pd.read_csv("ravenstack_subscriptions.csv")
churn_events = pd.read_csv("ravenstack_churn_events.csv")
support_tickets = pd.read_csv("ravenstack_support_tickets.csv")
feature_usage = pd.read_csv("ravenstack_feature_usage.csv")


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

st.sidebar.title("RavenStack Analytics")

page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Customer Explorer"]
)


# =====================================================
# OVERVIEW
# =====================================================

if page == "Overview":

    st.title("RavenStack SaaS Churn Analysis")

    st.write(
        "Explore customer churn patterns, industry-level trends, "
        "churn reasons, and individual account behavior."
    )


    # -------------------------------------------------
    # KPI SECTION
    # -------------------------------------------------

    churn_rate = accounts["churn_flag"].mean() * 100
    total_accounts = len(accounts)
    total_churned = accounts["churn_flag"].sum()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Accounts",
        total_accounts
    )

    col2.metric(
        "Churned Accounts",
        total_churned
    )

    col3.metric(
        "Overall Churn Rate",
        f"{churn_rate:.1f}%"
    )

    st.info(
        "Overall churn is 22%. DevTools has the highest churn rate "
        "among all industries."
    )


    # -------------------------------------------------
    # INDUSTRY CHURN
    # -------------------------------------------------

    st.subheader("Churn Rate by Industry")

    industry_churn = (
        accounts
        .groupby("industry")["churn_flag"]
        .mean()
        .mul(100)
        .reset_index(name="churn_rate")
    )

    industry_churn["vs_overall"] = (
        industry_churn["churn_rate"] - churn_rate
    )

    industry_churn = industry_churn.sort_values(
        "churn_rate",
        ascending=False
    )

    st.bar_chart(
        industry_churn.set_index("industry")["churn_rate"]
    )

    st.caption(
        f"Overall churn rate across all accounts: "
        f"{churn_rate:.1f}%"
    )

    st.dataframe(
        industry_churn,
        hide_index=True,
        column_config={
            "industry": "Industry",
            "churn_rate": st.column_config.NumberColumn(
                "Churn Rate (%)",
                format="%.1f%%"
            ),
            "vs_overall": st.column_config.NumberColumn(
                "Vs Overall (pp)",
                format="%.1f"
            )
        }
    )


    # -------------------------------------------------
    # INDUSTRY SELECTOR
    # -------------------------------------------------

    st.subheader("Explore an Industry")

    selected_industry = st.selectbox(
        "Select an industry",
        ["All"] + sorted(
            accounts["industry"].unique().tolist()
        )
    )

    if selected_industry == "All":

        filtered_accounts = accounts

    else:

        filtered_accounts = accounts[
            accounts["industry"] == selected_industry
        ]

    filtered_churn_rate = (
        filtered_accounts["churn_flag"].mean() * 100
    )

    st.metric(
        "Selected Industry Churn Rate",
        f"{filtered_churn_rate:.1f}%"
    )


    # -------------------------------------------------
    # CHURN REASONS
    # -------------------------------------------------

    st.subheader("Churn Reasons")

    if selected_industry == "All":

        filtered_churn_events = churn_events

    else:

        filtered_churn_events = churn_events.merge(
            accounts[["account_id", "industry"]],
            on="account_id",
            how="left"
        )

        filtered_churn_events = filtered_churn_events[
            filtered_churn_events["industry"]
            == selected_industry
        ]

    churn_reasons = (
        filtered_churn_events["reason_code"]
        .value_counts()
    )

    st.bar_chart(churn_reasons)


    # -------------------------------------------------
    # ANALYSIS CONTEXT FOR AI
    # -------------------------------------------------

    analysis_context = f"""
RavenStack SaaS Churn Analysis

Overall churn rate: {churn_rate:.1f}%

Total accounts: {total_accounts}

Total churned accounts: {total_churned}

Industry churn rates:

{industry_churn.to_string(index=False)}

Key findings from the analysis:

1. DevTools has the highest churn rate at approximately
{industry_churn.iloc[0]["churn_rate"]:.1f}%.

2. The overall churn rate is 22%.

3. Basic product engagement metrics showed little difference
between churned and non-churned accounts.

Average resolution time:
Non-churned = 36.45 hours
Churned = 35.49 hours

Average first response time:
Non-churned = 89.58 minutes
Churned = 84.93 minutes

Average satisfaction:
Non-churned = 3.95
Churned = 4.00

Average escalation count:
Non-churned = 0.185
Churned = 0.222

Average subscription duration:
Non-churned = 79.40 days
Churned = 94.09 days

Average product usage:
Non-churned = 495.13
Churned = 522.04

Average usage duration:
Non-churned = 150350.88 seconds
Churned = 158347.54 seconds

Average errors:
Non-churned = 28.23
Churned = 28.15

Beta feature adoption:
Accounts with beta usage had a churn rate of approximately
22.15%, compared with 12.50% for accounts without beta usage.

Feature breadth also showed almost no difference:
Non-churned = 4.74 unique features
Churned = 4.77 unique features

DevTools churn reasons:
Budget = 27
Support = 27
Features = 26
Competitor = 25
Pricing = 22
Unknown = 15

DevTools churn events preceded by an upgrade:
16.90%

DevTools churn events preceded by a downgrade:
11.27%

DevTools churn events that were reactivations:
9.15%

Important interpretation rule:
These findings describe associations and patterns in the dataset.
They do not establish causation.
Do not invent additional findings.
"""


    # -------------------------------------------------
    # AI ANALYST
    # -------------------------------------------------

    st.subheader("🤖 AI Analyst")

    st.write(
        "Ask a question about the RavenStack churn analysis."
    )

    user_question = st.text_input(
        "Your question",
        placeholder="Example: Why is DevTools churn concerning?"
    )

    if st.button("Ask AI"):

        if not user_question.strip():

            st.warning(
                "Please enter a question first."
            )

        else:

            with st.spinner(
                "Analyzing RavenStack data..."
            ):

                response = client.responses.create(
                    model="gpt-5.4-mini",
                    instructions="""
You are a business data analyst for RavenStack.

Answer the user's question using ONLY the provided
RavenStack analysis context.

Rules:

- Do not invent statistics or findings.
- Do not claim causation when the analysis only shows
  an association.
- Clearly distinguish observations from interpretations.
- If the available context is insufficient, say so.
- Keep answers concise and business-focused.
- Use specific numbers from the context when relevant.
""",
                    input=f"""
ANALYSIS CONTEXT:

{analysis_context}

USER QUESTION:

{user_question}
""",
                    max_output_tokens=500
                )

            st.markdown("### AI Analysis")

            st.write(
                response.output_text
            )


# =====================================================
# CUSTOMER EXPLORER
# =====================================================

else:

    st.title("Customer Explorer")

    selected_account = st.selectbox(
        "Select an account",
        sorted(accounts["account_id"].unique())
    )

    customer = accounts[
        accounts["account_id"] == selected_account
    ].iloc[0]


    # -------------------------------------------------
    # ACCOUNT
    # -------------------------------------------------

    st.subheader("Account")

    if customer["churn_flag"]:

        st.warning(
            "This account churned."
        )

    else:

        st.success(
            "This account did not churn."
        )

    col1, col2, col3 = st.columns(3)

    col1.write("**Industry**")
    col1.write(customer["industry"])

    col2.write("**Account ID**")
    col2.write(customer["account_id"])

    col3.write("**Churn Status**")
    col3.write(
        "Churned"
        if customer["churn_flag"]
        else "Active"
    )


    # -------------------------------------------------
    # SUBSCRIPTION PROFILE
    # -------------------------------------------------

    st.subheader("Subscription Profile")

    account_subscriptions = subscriptions[
        subscriptions["account_id"] == selected_account
    ]

    col1, col2 = st.columns(2)

    col1.metric(
        "Number of Subscriptions",
        len(account_subscriptions)
    )

    col2.metric(
        "Upgrades",
        account_subscriptions["upgrade_flag"].sum()
    )


    # -------------------------------------------------
    # SUPPORT PROFILE
    # -------------------------------------------------

    st.subheader("Support Profile")

    account_tickets = support_tickets[
        support_tickets["account_id"] == selected_account
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Support Tickets",
        len(account_tickets)
    )

    col2.metric(
        "Escalations",
        account_tickets["escalation_flag"].sum()
    )

    col3.metric(
        "Avg Satisfaction",
        f"{account_tickets['satisfaction_score'].mean():.1f}"
    )


    # -------------------------------------------------
    # PRODUCT USAGE
    # -------------------------------------------------

    st.subheader("Product Usage")

    account_subscription_ids = (
        account_subscriptions["subscription_id"]
    )

    account_usage = feature_usage[
        feature_usage["subscription_id"].isin(
            account_subscription_ids
        )
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Usage Events",
        int(account_usage["usage_count"].sum())
    )

    col2.metric(
        "Total Duration (sec)",
        int(
            account_usage[
                "usage_duration_secs"
            ].sum()
        )
    )

    col3.metric(
        "Total Errors",
        int(
            account_usage[
                "error_count"
            ].sum()
        )
    )


    # -------------------------------------------------
    # CHURN INFORMATION
    # -------------------------------------------------

    st.subheader("Churn Information")

    account_churn_events = churn_events[
        churn_events["account_id"] == selected_account
    ]

    if len(account_churn_events) > 0:

        st.write(
            "Recorded churn reason:",
            account_churn_events[
                "reason_code"
            ].iloc[0]
        )

    else:

        st.write(
            "No churn event recorded for this account."
        )