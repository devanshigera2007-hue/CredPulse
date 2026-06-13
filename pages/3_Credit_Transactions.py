import streamlit as st
import sqlite3

st.title("💳 Credit Transactions")

conn = sqlite3.connect("credpulse.db")

customers = conn.execute(
    "SELECT id,name FROM customers"
).fetchall()

customer_dict = {
    customer[1]: customer[0]
    for customer in customers
}

selected_customer = st.selectbox(
    "Customer",
    list(customer_dict.keys())
)

amount = st.number_input(
    "Credit Amount",
    min_value=0.0
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

    conn.execute(
        """
        INSERT INTO credit_transactions
        (customer_id,amount,transaction_date,due_date,remarks)
        VALUES (?,?,?,?,?)
        """,
        (
            customer_dict[selected_customer],
            amount,
            str(transaction_date),
            str(due_date),
            remarks
        )
    )

    conn.commit()

    st.success("Transaction Added")

conn.close()