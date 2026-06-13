import streamlit as st
import sqlite3

st.title("💳 Credit Transactions")

conn = sqlite3.connect("credpulse.db")

customers = conn.execute(
    "SELECT id,name FROM customers"
).fetchall()

if not customers:
    st.warning("Please add a customer first.")
    st.stop()

customer_names = [customer[1] for customer in customers]

selected_customer = st.selectbox(
    "Select Customer",
    customer_names
)

amount = st.number_input(
    "Credit Amount (₹)",
    min_value=0.0,
    step=100.0
)

transaction_date = st.date_input(
    "Transaction Date"
)

due_date = st.date_input(
    "Due Date"
)

remarks = st.text_area(
    "Remarks"
)

if st.button("Add Credit Transaction"):

    customer_id = next(
        customer[0]
        for customer in customers
        if customer[1] == selected_customer
    )

    conn.execute(
        """
        INSERT INTO credit_transactions
        (
            customer_id,
            amount,
            transaction_date,
            due_date,
            remarks
        )
        VALUES (?,?,?,?,?)
        """,
        (
            customer_id,
            amount,
            str(transaction_date),
            str(due_date),
            remarks
        )
    )

    conn.commit()

    st.success("Credit Transaction Added Successfully")

st.divider()

transactions = conn.execute("""
SELECT
credit_transactions.id,
customers.name,
credit_transactions.amount,
credit_transactions.transaction_date,
credit_transactions.due_date,
credit_transactions.remarks
FROM credit_transactions
JOIN customers
ON customers.id = credit_transactions.customer_id
""").fetchall()

st.subheader("All Credit Transactions")

import pandas as pd

df = pd.DataFrame(
    transactions,
    columns=[
        "Transaction ID",
        "Customer",
        "Amount (₹)",
        "Transaction Date",
        "Due Date",
        "Remarks"
    ]
)

st.dataframe(
    df,
    use_container_width=True
)

conn.close()