import streamlit as st
import sqlite3

st.title("🎯 Decision Center")

conn = sqlite3.connect("credpulse.db")

customers = conn.execute(
    "SELECT id,name FROM customers"
).fetchall()

if not customers:
    st.warning("No customers found.")
    st.stop()

customer_names = [customer[1] for customer in customers]

selected_customer = st.selectbox(
    "Select Customer",
    customer_names
)

customer_id = next(
    customer[0]
    for customer in customers
    if customer[1] == selected_customer
)

# Total Credit

total_credit = conn.execute(
    """
    SELECT COALESCE(SUM(amount),0)
    FROM credit_transactions
    WHERE customer_id = ?
    """,
    (customer_id,)
).fetchone()[0]

# Total Payments

total_payments = conn.execute(
    """
    SELECT COALESCE(SUM(amount),0)
    FROM payments
    WHERE customer_id = ?
    """,
    (customer_id,)
).fetchone()[0]

outstanding = total_credit - total_payments

# TRUST SCORE

trust_score = 100

if outstanding > 5000:
    trust_score -= 40
elif outstanding > 2000:
    trust_score -= 20
elif outstanding > 1000:
    trust_score -= 10

if total_payments > 0:
    trust_score += 5

trust_score = max(0, min(100, trust_score))

# RISK CATEGORY

if trust_score >= 80:
    risk = "LOW"
    recommendation = "✅ Safe to extend additional credit"

elif trust_score >= 50:
    risk = "MEDIUM"
    recommendation = "⚠️ Extend credit with caution"

else:
    risk = "HIGH"
    recommendation = "❌ Do not extend further credit"

# DISPLAY

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Outstanding Amount",
        f"₹{outstanding:.0f}"
    )

with col2:
    st.metric(
        "Trust Score",
        f"{trust_score}"
    )

with col3:
    st.metric(
        "Risk Level",
        risk
    )

st.divider()

st.subheader("Recommendation")

st.success(recommendation)

conn.close()