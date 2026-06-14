```python
import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("credpulse.db")

# =========================
# DATA
# =========================

total_customers = conn.execute(
    "SELECT COUNT(*) FROM customers"
).fetchone()[0]

total_credit = conn.execute(
    """
    SELECT COALESCE(SUM(amount),0)
    FROM credit_transactions
    """
).fetchone()[0]

total_payments = conn.execute(
    """
    SELECT COALESCE(SUM(amount),0)
    FROM payments
    """
).fetchone()[0]

outstanding = total_credit - total_payments

if total_credit > 0:
    collection_rate = round(
        (total_payments / total_credit) * 100,
        1
    )
else:
    collection_rate = 0

# =========================
# CUSTOM STYLING
# =========================

st.markdown("""
<style>

.metric-card{
background:white;
padding:25px;
border-radius:20px;
text-align:center;
box-shadow:0px 4px 15px rgba(0,0,0,0.08);
border:2px solid #FACC15;
}

.metric-value{
font-size:38px;
font-weight:bold;
color:#7C3AED;
}

.metric-label{
font-size:16px;
color:#666;
}

.hero-card{
background:linear-gradient(
135deg,
#7C3AED,
#A855F7
);
padding:40px;
border-radius:30px;
margin-bottom:30px;
box-shadow:0px 10px 30px rgba(124,58,237,0.35);
}

.hero-title{
color:white;
font-size:56px;
font-weight:bold;
}

.hero-subtitle{
color:white;
font-size:20px;
}

.info-card{
padding:25px;
border-radius:20px;
color:white;
margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HERO
# =========================

st.markdown("""
<div class="hero-card">

<div class="hero-title">
💳 CredPulse
</div>

<div class="hero-subtitle">
AI-Powered Credit Intelligence Platform
</div>

</div>
""", unsafe_allow_html=True)

st.markdown("## Welcome Back 👋")

st.caption(
    "Monitor customer credit exposure, repayments and business performance in real time."
)

# =========================
# KPI CARDS
# =========================

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">
        ₹{outstanding:,.0f}
        </div>
        <div class="metric-label">
        Outstanding Credit
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">
        {total_customers}
        </div>
        <div class="metric-label">
        Customers
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">
        ₹{total_credit:,.0f}
        </div>
        <div class="metric-label">
        Credit Issued
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">
        {collection_rate}%
        </div>
        <div class="metric-label">
        Collection Rate
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# =========================
# STATUS CARDS
# =========================

col1,col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card"
    style="background:linear-gradient(135deg,#22C55E,#16A34A);">

    <h3>✅ Healthy Portfolio</h3>

    <p>
    Most customers are repaying on time.
    </p>

    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card"
    style="background:linear-gradient(135deg,#3B82F6,#2563EB);">

    <h3>📈 Business Insight</h3>

    <p>
    Collections are improving this month.
    </p>

    </div>
    """, unsafe_allow_html=True)

# =========================
# TRANSACTIONS
# =========================

st.markdown("## 📋 Recent Credit Transactions")

transactions = conn.execute(
"""
SELECT
customers.name,
credit_transactions.amount,
credit_transactions.transaction_date
FROM credit_transactions
JOIN customers
ON customers.id = credit_transactions.customer_id
ORDER BY credit_transactions.id DESC
LIMIT 10
"""
).fetchall()

df = pd.DataFrame(
    transactions,
    columns=[
        "Customer",
        "Amount (₹)",
        "Date"
    ]
)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

conn.close()
```
