import streamlit as st
import sqlite3
import database

st.title("👤 Customer Management")

name = st.text_input("Customer Name")
phone = st.text_input("Phone Number")
credit_limit = st.number_input("Credit Limit", min_value=0.0)

if st.button("Add Customer"):

    conn = sqlite3.connect("credpulse.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO customers(name,phone,credit_limit) VALUES(?,?,?)",
        (name, phone, credit_limit)
    )

    conn.commit()
    conn.close()

    st.success("Customer Added Successfully")

st.divider()

conn = sqlite3.connect("credpulse.db")

customers = conn.execute(
    "SELECT * FROM customers"
).fetchall()

conn.close()

st.subheader("All Customers")

st.dataframe(customers)
cursor.execute("""
CREATE TABLE IF NOT EXISTS credit_transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    amount REAL,
    transaction_date TEXT,
    due_date TEXT,
    remarks TEXT
)
""")