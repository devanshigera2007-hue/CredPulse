import streamlit as st
import sqlite3

st.title("💰 Payments")

conn = sqlite3.connect("credpulse.db")

customers = conn.execute(
    "SELECT id,name FROM customers"
).fetchall()

if not customers:
    st.warning("No customers found.")
    st.stop()

customer_names = [customer[1] for customer in customers]

selected_customer = st.selectbox(
    "Customer",
    customer_names
)

amount = st.number_input(
    "Payment Amount (₹)",
    min_value=0.0,
    step=100.0
)

payment_date = st.date_input(
    "Payment Date"
)

if st.button("Record Payment"):

    customer_id = next(
        customer[0]
        for customer in customers
        if customer[1] == selected_customer
    )

    conn.execute(
        """
        INSERT INTO payments
        (
            customer_id,
            amount,
            payment_date
        )
        VALUES (?,?,?)
        """,
        (
            customer_id,
            amount,
            str(payment_date)
        )
    )

    conn.commit()

    st.success("Payment Recorded Successfully")

payments = conn.execute("""
SELECT
payments.id,
customers.name,
payments.amount,
payments.payment_date
FROM payments
JOIN customers
ON customers.id = payments.customer_id
""").fetchall()

import pandas as pd

df = pd.DataFrame(
    payments,
    columns=[
        "Payment ID",
        "Customer",
        "Amount (₹)",
        "Payment Date"
    ]
)

st.divider()

st.subheader("Payment History")

st.dataframe(
    df,
    use_container_width=True
)

conn.close()