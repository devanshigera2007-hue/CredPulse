import streamlit as st
import sqlite3

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif !important; }
.stApp { background: #0a0a12 !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1100px; }
.stNumberInput > div > div > input {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 10px !important;
  color: #f1f5f9 !important;
}
label { color: #94a3b8 !important; font-size: 13px !important; font-weight: 500 !important; }
.stButton > button {
  background: linear-gradient(135deg, #059669, #34d399) !important;
  color: #022c22 !important;
  border: none !important;
  border-radius: 10px !important;
  font-weight: 700 !important;
  width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom:28px;">
  <div style="font-size:26px;font-weight:800;color:#f8fafc;">💰 Payments</div>
  <div style="font-size:13px;color:#475569;margin-top:2px;">Record customer repayments</div>
</div>
""", unsafe_allow_html=True)

conn = sqlite3.connect("credpulse.db")
customers = conn.execute("SELECT id, name FROM customers").fetchall()

if not customers:
    st.warning("No customers found.")
    st.stop()

customer_names = [c[1] for c in customers]

st.markdown("""
<div style="background:rgba(5,150,105,0.07);border:1px solid rgba(5,150,105,0.2);
  border-radius:18px;padding:24px 24px 8px 24px;margin-bottom:28px;">
  <div style="font-size:14px;font-weight:700;color:#34d399;margin-bottom:16px;">➕ Record New Payment</div>
""", unsafe_allow_html=True)

selected_customer = st.selectbox("Customer", customer_names)
amount            = st.number_input("Payment Amount (₹)", min_value=0.0, step=100.0)
payment_date      = st.date_input("Payment Date")

if st.button("✅ Record Payment"):
    if amount > 0:
        customer_id = next(c[0] for c in customers if c[1] == selected_customer)
        conn.execute(
            "INSERT INTO payments(customer_id,amount,payment_date) VALUES(?,?,?)",
            (customer_id, amount, str(payment_date))
        )
        conn.commit()
        st.success(f"✅ ₹{amount:,.0f} payment recorded for {selected_customer}!")
        st.rerun()
    else:
        st.error("Please enter an amount greater than 0.")

st.markdown("</div>", unsafe_allow_html=True)

payments = conn.execute("""
    SELECT payments.id, customers.name, payments.amount, payments.payment_date
    FROM payments
    JOIN customers ON customers.id = payments.customer_id
    ORDER BY payments.id DESC
""").fetchall()
conn.close()

st.markdown(f"""
<div style="font-size:15px;font-weight:700;color:#cbd5e1;margin-bottom:12px;">
  📋 Payment History
  <span style="background:rgba(5,150,105,0.2);color:#34d399;
    padding:2px 10px;border-radius:999px;font-size:11px;margin-left:8px;">{len(payments)}</span>
</div>
""", unsafe_allow_html=True)

if payments:
    st.markdown("""
    <div style="display:grid;grid-template-columns:0.4fr 2fr 1fr 1fr;
      padding:8px 12px;font-size:11px;font-weight:600;color:#475569;
      text-transform:uppercase;letter-spacing:0.07em;
      border-bottom:1px solid rgba(255,255,255,0.07);margin-bottom:4px;">
      <span>ID</span><span>Customer</span><span>Amount</span><span>Date</span>
    </div>""", unsafe_allow_html=True)
    for i, (pid, name, amt, pdate) in enumerate(payments):
        bg = "rgba(255,255,255,0.02)" if i % 2 == 0 else "transparent"
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:0.4fr 2fr 1fr 1fr;
          padding:12px;font-size:13px;color:#cbd5e1;
          background:{bg};border-radius:8px;align-items:center;">
          <span style="color:#475569;">#{pid}</span>
          <span style="font-weight:600;color:#f1f5f9;display:flex;align-items:center;gap:8px;">
            <span style="display:inline-flex;width:26px;height:26px;border-radius:50%;
              background:linear-gradient(135deg,#059669,#34d399);
              align-items:center;justify-content:center;font-size:11px;font-weight:700;color:white;">
              {name[0].upper()}</span>{name}
          </span>
          <span style="color:#34d399;font-weight:700;">+₹{amt:,.0f}</span>
          <span style="color:#64748b;">{pdate}</span>
        </div>""", unsafe_allow_html=True)