import streamlit as st
import sqlite3

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif !important; }
.stApp { background: #0a0a12 !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1100px; }
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 10px !important;
  color: #f1f5f9 !important;
}
label { color: #94a3b8 !important; font-size: 13px !important; font-weight: 500 !important; }
.stButton > button {
  background: linear-gradient(135deg, #d97706, #fbbf24) !important;
  color: #1a1a2e !important;
  border: none !important;
  border-radius: 10px !important;
  font-weight: 700 !important;
  width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom:28px;">
  <div style="font-size:26px;font-weight:800;color:#f8fafc;">💳 Credit Issuance</div>
  <div style="font-size:13px;color:#475569;margin-top:2px;">Record new credit transactions for your customers</div>
</div>
""", unsafe_allow_html=True)

conn = sqlite3.connect("credpulse.db")
customers = conn.execute("SELECT id, name FROM customers").fetchall()

if not customers:
    st.warning("Please add a customer first.")
    st.stop()

customer_names = [c[1] for c in customers]

st.markdown("""
<div style="background:rgba(217,119,6,0.07);border:1px solid rgba(217,119,6,0.2);
  border-radius:18px;padding:24px 24px 8px 24px;margin-bottom:28px;">
  <div style="font-size:14px;font-weight:700;color:#fbbf24;margin-bottom:16px;">➕ New Credit Transaction</div>
""", unsafe_allow_html=True)

selected_customer = st.selectbox("Select Customer", customer_names)
amount            = st.number_input("Credit Amount (₹)", min_value=0.0, step=100.0)
transaction_date  = st.date_input("Transaction Date")
due_date          = st.date_input("Due Date")
remarks           = st.text_area("Remarks (optional)", placeholder="e.g. Advance for festival stock")

if st.button("💳 Issue Credit"):
    if amount > 0:
        customer_id = next(c[0] for c in customers if c[1] == selected_customer)
        conn.execute(
            "INSERT INTO credit_transactions(customer_id,amount,transaction_date,due_date,remarks) VALUES(?,?,?,?,?)",
            (customer_id, amount, str(transaction_date), str(due_date), remarks)
        )
        conn.commit()
        st.success(f"✅ ₹{amount:,.0f} credit issued to {selected_customer}!")
        st.rerun()
    else:
        st.error("Please enter an amount greater than 0.")

st.markdown("</div>", unsafe_allow_html=True)

transactions = conn.execute("""
    SELECT credit_transactions.id, customers.name, credit_transactions.amount,
           credit_transactions.transaction_date, credit_transactions.due_date, credit_transactions.remarks
    FROM credit_transactions
    JOIN customers ON customers.id = credit_transactions.customer_id
    ORDER BY credit_transactions.id DESC
""").fetchall()
conn.close()

st.markdown(f"""
<div style="font-size:15px;font-weight:700;color:#cbd5e1;margin-bottom:12px;">
  📋 All Credit Transactions
  <span style="background:rgba(217,119,6,0.2);color:#fbbf24;
    padding:2px 10px;border-radius:999px;font-size:11px;margin-left:8px;">{len(transactions)}</span>
</div>
""", unsafe_allow_html=True)

if transactions:
    st.markdown("""
    <div style="display:grid;grid-template-columns:0.4fr 1.5fr 1fr 1fr 1fr 2fr;
      padding:8px 12px;font-size:11px;font-weight:600;color:#475569;
      text-transform:uppercase;letter-spacing:0.07em;
      border-bottom:1px solid rgba(255,255,255,0.07);margin-bottom:4px;">
      <span>ID</span><span>Customer</span><span>Amount</span>
      <span>Date</span><span>Due</span><span>Remarks</span>
    </div>""", unsafe_allow_html=True)
    for i, (tid, name, amt, tdate, ddate, rem) in enumerate(transactions):
        bg = "rgba(255,255,255,0.02)" if i % 2 == 0 else "transparent"
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:0.4fr 1.5fr 1fr 1fr 1fr 2fr;
          padding:11px 12px;font-size:13px;color:#cbd5e1;
          background:{bg};border-radius:8px;align-items:center;">
          <span style="color:#475569;">#{tid}</span>
          <span style="font-weight:600;color:#f1f5f9;">{name}</span>
          <span style="color:#fbbf24;font-weight:600;">₹{amt:,.0f}</span>
          <span style="color:#94a3b8;">{tdate}</span>
          <span style="color:#f87171;">{ddate}</span>
          <span style="color:#64748b;">{rem or '—'}</span>
        </div>""", unsafe_allow_html=True)