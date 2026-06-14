import streamlit as st
import sqlite3

st.title("🎯 Credit Decision Engine")
st.caption("Customer trust scoring and lending recommendations")

# ==========================
# DATABASE
# ==========================

conn = sqlite3.connect("credpulse.db")

customers = conn.execute(
    "SELECT id, name FROM customers"
).fetchall()

if not customers:
    st.warning("No customers found.")
    st.stop()

selected_customer = st.selectbox(
    "Select Customer",
    [c[1] for c in customers]
)

customer_id = next(
    c[0]
    for c in customers
    if c[1] == selected_customer
)

# ==========================
# CUSTOMER DATA
# ==========================

total_credit = conn.execute(
    """
    SELECT COALESCE(SUM(amount),0)
    FROM credit_transactions
    WHERE customer_id=?
    """,
    (customer_id,)
).fetchone()[0]

total_payments = conn.execute(
    """
    SELECT COALESCE(SUM(amount),0)
    FROM payments
    WHERE customer_id=?
    """,
    (customer_id,)
).fetchone()[0]

tx_count = conn.execute(
    """
    SELECT COUNT(*)
    FROM credit_transactions
    WHERE customer_id=?
    """,
    (customer_id,)
).fetchone()[0]

conn.close()

outstanding = total_credit - total_payments

# ==========================
# CREDIT SCORE MODEL
# ==========================

score = 50

# Outstanding balance

if outstanding <= 500:
    score += 25
elif outstanding <= 2000:
    score += 15
elif outstanding <= 5000:
    score += 5
else:
    score -= 20

# Repayment behaviour

if total_credit > 0:

    repayment_ratio = (
        total_payments / total_credit
    )

    if repayment_ratio >= 0.80:
        score += 20

    elif repayment_ratio >= 0.50:
        score += 10

    elif repayment_ratio > 0:
        score += 5

    else:
        score -= 10

# Transaction history

if tx_count >= 10:
    score += 15

elif tx_count >= 5:
    score += 10

elif tx_count >= 2:
    score += 5

score = max(
    0,
    min(100, round(score))
)

# ==========================
# RISK LEVEL
# ==========================

if score >= 80:

    risk = "🟢 LOW RISK"

    recommendation = (
        "Safe to extend additional credit"
    )

elif score >= 50:

    risk = "🟡 MEDIUM RISK"

    recommendation = (
        "Extend credit with caution"
    )

else:

    risk = "🔴 HIGH RISK"

    recommendation = (
        "Do not extend further credit"
    )

# ==========================
# DISPLAY
# ==========================

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Trust Score",
        f"{score}/100"
    )

with col2:
    st.metric(
        "Outstanding",
        f"₹{outstanding:,.0f}"
    )

with col3:
    st.metric(
        "Payments",
        f"₹{total_payments:,.0f}"
    )

with col4:
    st.metric(
        "Transactions",
        tx_count
    )

st.divider()

st.subheader("Risk Assessment")
st.write(risk)

st.subheader("Recommendation")
st.info(recommendation)

st.divider()

st.subheader("Credit Summary")

st.write(f"**Customer:** {selected_customer}")
st.write(f"**Total Credit Issued:** ₹{total_credit:,.0f}")
st.write(f"**Total Payments:** ₹{total_payments:,.0f}")
st.write(f"**Outstanding Balance:** ₹{outstanding:,.0f}")
st.write(f"**Number of Transactions:** {tx_count}")

st.divider()

st.subheader("Score Explanation")

st.write("""
- Base Score = 50
- Lower outstanding balance increases score
- Better repayment history increases score
- More transaction history increases score
- Final score is capped between 0 and 100
""")