import streamlit as st
import sqlite3
import database

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif !important; }
.stApp { background: #0a0a12 !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1100px; }
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 10px !important;
  color: #f1f5f9 !important;
}
label { color: #94a3b8 !important; font-size: 13px !important; font-weight: 500 !important; }
.stButton > button {
  background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
  color: white !important;
  border: none !important;
  border-radius: 10px !important;
  font-weight: 600 !important;
  width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom:28px;">
  <div style="font-size:26px;font-weight:800;color:#f8fafc;">Customer Management</div>
  <div style="font-size:13px;color:#475569;margin-top:2px;">Add and manage your credit customers</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:rgba(124,58,237,0.08);border:1px solid rgba(124,58,237,0.2);
  border-radius:18px;padding:24px 24px 8px 24px;margin-bottom:28px;">
  <div style="font-size:14px;font-weight:700;color:#a78bfa;margin-bottom:16px;">➕ Add New Customer</div>
""", unsafe_allow_html=True)

name         = st.text_input("Customer Name", placeholder="e.g. Ramesh Kumar")
phone        = st.text_input("Phone Number", placeholder="e.g. 9876543210")
credit_limit = st.number_input("Credit Limit (₹)", min_value=0.0, step=500.0)

if st.button("Add Customer"):
    if name.strip():
        conn = sqlite3.connect("credpulse.db")
        conn.execute("INSERT INTO customers(name,phone,credit_limit) VALUES(?,?,?)", (name, phone, credit_limit))
        conn.commit()
        conn.close()
        st.success(f"✅ {name} added successfully!")
        st.rerun()
    else:
        st.error("Please enter a customer name.")

st.markdown("</div>", unsafe_allow_html=True)

conn = sqlite3.connect("credpulse.db")
customers = conn.execute("SELECT id, name, phone, credit_limit FROM customers").fetchall()
conn.close()

st.markdown(f"""
<div style="font-size:15px;font-weight:700;color:#cbd5e1;margin-bottom:12px;">
  👥 All Customers
  <span style="background:rgba(124,58,237,0.2);color:#a78bfa;
    padding:2px 10px;border-radius:999px;font-size:11px;margin-left:6px;">{len(customers)}</span>
</div>
""", unsafe_allow_html=True)

if customers:
    st.markdown("""
    <div style="display:grid;grid-template-columns:0.5fr 2fr 1.5fr 1fr;
      padding:8px 16px;font-size:11px;font-weight:600;color:#475569;
      text-transform:uppercase;letter-spacing:0.07em;
      border-bottom:1px solid rgba(255,255,255,0.07);margin-bottom:4px;">
      <span>#</span><span>Name</span><span>Phone</span><span>Credit Limit</span>
    </div>""", unsafe_allow_html=True)

    colors = ["#7c3aed","#a855f7","#d97706","#fbbf24","#059669","#34d399","#2563eb","#60a5fa"]
    for i, (cid, cname, phone, limit) in enumerate(customers):
        bg = "rgba(255,255,255,0.02)" if i % 2 == 0 else "transparent"
        color = colors[i % len(colors)]
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:0.5fr 2fr 1.5fr 1fr;
          padding:12px 16px;font-size:13px;color:#cbd5e1;
          background:{bg};border-radius:8px;align-items:center;">
          <span style="color:#475569;">{cid}</span>
          <span style="font-weight:600;color:#f1f5f9;display:flex;align-items:center;gap:10px;">
            <span style="display:inline-flex;width:30px;height:30px;border-radius:50%;
              background:linear-gradient(135deg,{color},{color}88);
              align-items:center;justify-content:center;font-size:12px;font-weight:700;color:white;">
              {cname[0].upper()}</span>{cname}
          </span>
          <span style="color:#94a3b8;">{phone or '—'}</span>
          <span style="color:#fbbf24;font-weight:600;">₹{limit:,.0f}</span>
        </div>""", unsafe_allow_html=True)