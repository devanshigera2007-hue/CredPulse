import streamlit as st
import sqlite3
import pandas as pd

st.title("📖 Customer Ledger")

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

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Credit", f"₹{total_credit:.0f}")

with col2:
    st.metric("Total Payments", f"₹{total_payments:.0f}")

with col3:
    st.metric("Outstanding", f"₹{outstanding:.0f}")

st.divider()

credit_data = conn.execute(
    """
    SELECT
    transaction_date,
    amount,
    remarks
    FROM credit_transactions
    WHERE customer_id = ?
    """,
    (customer_id,)
).fetchall()

credit_df = pd.DataFrame(
    credit_data,
    columns=[
        "Date",
        "Credit Amount",
        "Remarks"
    ]
)

st.subheader("Credit History")
st.dataframe(credit_df, use_container_width=True)

payment_data = conn.execute(
    """
    SELECT
    payment_date,
    amount
    FROM payments
    WHERE customer_id = ?
    """,
    (customer_id,)
).fetchall()

payment_df = pd.DataFrame(
    payment_data,
    columns=[
        "Date",
        "Payment Amount"
    ]
)

st.subheader("Payment History")
st.dataframe(payment_df, use_container_width=True)

conn.close()