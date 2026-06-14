import streamlit as st
import sqlite3
import pandas as pd

st.markdown("""
<div style="
background:
linear-gradient(
135deg,
#7C3AED,
#A855F7
);

padding:35px;

border-radius:25px;

margin-bottom:25px;
">

<h1 style="color:white;">
💳 CredPulse
</h1>

<p style="
color:white;
font-size:18px;
">
Smarter Credit Decisions for Local Retailers
</p>

</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.success("""
    ✅ Healthy Portfolio
    
    Most customers are repaying on time.
    """)

with col2:
    st.info("""
    📈 Credit Activity
    
    Collections are increasing this month.
    """)

st.title("📊 Dashboard")
st.markdown("""
### Welcome Back 👋

Monitor customer credit exposure, repayment activity,
and business health from a single dashboard.
""")

conn = sqlite3.connect("credpulse.db")

# Total Customers
total_customers = conn.execute(
    "SELECT COUNT(*) FROM customers"
).fetchone()[0]

# Total Credit Given
total_credit = conn.execute(
    """
    SELECT COALESCE(SUM(amount),0)
    FROM credit_transactions
    """
).fetchone()[0]

# Total Payments Received
total_payments = conn.execute(
    """
    SELECT COALESCE(SUM(amount),0)
    FROM payments
    """
).fetchone()[0]

# Outstanding Amount
outstanding = total_credit - total_payments

# Collection Rate
if total_credit > 0:
    collection_rate = round(
        (total_payments / total_credit) * 100,
        1
    )
else:
    collection_rate = 0

# KPI Cards

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Outstanding Credit",
        f"₹{outstanding:.0f}"
    )

with col2:
    st.metric(
        "Customers",
        total_customers
    )

with col3:
    st.metric(
        "Total Credit",
        f"₹{total_credit:.0f}"
    )

with col4:
    st.metric(
        "Collection Rate",
        f"{collection_rate}%"
    )

st.divider()

# Recent Credit Transactions

st.subheader("Recent Credit Transactions")

transactions = conn.execute("""
SELECT
customers.name,
credit_transactions.amount,
credit_transactions.transaction_date
FROM credit_transactions
JOIN customers
ON customers.id = credit_transactions.customer_id
ORDER BY credit_transactions.id DESC
LIMIT 10
""").fetchall()

df = pd.DataFrame(
    transactions,
    columns=[
        "Customer",
        "Amount",
        "Date"
    ]
)

st.dataframe(
    df,
    use_container_width=True
)

conn.close()