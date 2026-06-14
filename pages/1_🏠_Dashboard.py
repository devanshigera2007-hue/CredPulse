import streamlit as st
import sqlite3
from datetime import datetime

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif !important; }
.stApp { background: #0a0a12 !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1100px; }
</style>
""", unsafe_allow_html=True)

conn = sqlite3.connect("credpulse.db")
total_customers = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
total_credit    = conn.execute("SELECT COALESCE(SUM(amount),0) FROM credit_transactions").fetchone()[0]
total_payments  = conn.execute("SELECT COALESCE(SUM(amount),0) FROM payments").fetchone()[0]
outstanding     = total_credit - total_payments
collection_rate = round((total_payments / total_credit) * 100, 1) if total_credit > 0 else 0
transactions    = conn.execute("""
    SELECT customers.name, credit_transactions.amount, credit_transactions.transaction_date
    FROM credit_transactions
    JOIN customers ON customers.id = credit_transactions.customer_id
    ORDER BY credit_transactions.id DESC LIMIT 8
""").fetchall()
conn.close()

today = datetime.now().strftime("%d %b %Y")

st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:28px;">
  <div>
    <div style="font-size:26px;font-weight:800;color:#f8fafc;letter-spacing:-0.5px;">Dashboard</div>
    <div style="font-size:13px;color:#475569;margin-top:2px;">CredPulse · {today}</div>
  </div>
  <div style="background:linear-gradient(135deg,#7c3aed,#a855f7);
    padding:8px 18px;border-radius:999px;font-size:12px;font-weight:600;color:white;">⚡ LIVE</div>
</div>
""", unsafe_allow_html=True)

kpis = [
    ("💳", "Total Credit Issued",  f"₹{total_credit:,.0f}",  "#7c3aed", "#a855f7", "Lifetime across all customers"),
    ("⏳", "Outstanding Balance",  f"₹{outstanding:,.0f}",   "#d97706", "#fbbf24", "Yet to be collected"),
    ("✅", "Collection Rate",      f"{collection_rate}%",     "#059669", "#34d399", f"₹{total_payments:,.0f} recovered"),
    ("👥", "Total Customers",      f"{total_customers}",      "#2563eb", "#60a5fa", "Active credit accounts"),
]
cols = st.columns(4)
for col, (icon, label, value, c1, c2, sub) in zip(cols, kpis):
    with col:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
          border-radius:18px;padding:22px 20px 18px 20px;position:relative;overflow:hidden;">
          <div style="position:absolute;top:0;left:0;right:0;height:3px;
            background:linear-gradient(90deg,{c1},{c2});border-radius:18px 18px 0 0;"></div>
          <div style="font-size:22px;margin-bottom:10px;">{icon}</div>
          <div style="font-size:11px;font-weight:600;color:#64748b;
            text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">{label}</div>
          <div style="font-size:28px;font-weight:800;color:{c2};
            letter-spacing:-1px;line-height:1;margin-bottom:6px;">{value}</div>
          <div style="font-size:11px;color:#475569;">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

b1, b2 = st.columns(2)
with b1:
    health = "🟢 Healthy Portfolio" if collection_rate >= 50 else "🔴 Portfolio at Risk"
    health_sub = "Most customers are repaying on time." if collection_rate >= 50 else "Collection rate needs attention."
    bg = "linear-gradient(135deg,#064e3b,#059669)" if collection_rate >= 50 else "linear-gradient(135deg,#7f1d1d,#dc2626)"
    st.markdown(f"""
    <div style="background:{bg};padding:20px 22px;border-radius:16px;">
      <div style="font-size:15px;font-weight:700;color:white;margin-bottom:4px;">{health}</div>
      <div style="font-size:13px;color:rgba(255,255,255,0.7);">{health_sub}</div>
    </div>""", unsafe_allow_html=True)
with b2:
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1e1b4b,#4338ca);padding:20px 22px;border-radius:16px;">
      <div style="font-size:15px;font-weight:700;color:white;margin-bottom:4px;">📊 Credit Activity</div>
      <div style="font-size:13px;color:rgba(255,255,255,0.7);">
        ₹{outstanding:,.0f} outstanding across {total_customers} customers.
      </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style="font-size:15px;font-weight:700;color:#cbd5e1;margin-bottom:12px;">📋 Recent Credit Transactions</div>
""", unsafe_allow_html=True)

if transactions:
    st.markdown("""
    <div style="display:grid;grid-template-columns:2fr 1fr 1fr;
      padding:8px 12px;font-size:11px;font-weight:600;color:#475569;
      text-transform:uppercase;letter-spacing:0.07em;
      border-bottom:1px solid rgba(255,255,255,0.07);margin-bottom:4px;">
      <span>Customer</span><span>Amount</span><span>Date</span>
    </div>""", unsafe_allow_html=True)
    for i, (name, amount, date) in enumerate(transactions):
        bg = "rgba(255,255,255,0.02)" if i % 2 == 0 else "transparent"
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:2fr 1fr 1fr;
          padding:12px;font-size:13px;color:#cbd5e1;
          background:{bg};border-radius:8px;align-items:center;">
          <span style="font-weight:600;color:#f1f5f9;display:flex;align-items:center;gap:10px;">
            <span style="display:inline-flex;width:28px;height:28px;border-radius:50%;
              background:linear-gradient(135deg,#7c3aed,#a855f7);
              align-items:center;justify-content:center;font-size:11px;font-weight:700;color:white;">
              {name[0].upper()}</span>{name}
          </span>
          <span style="color:#fbbf24;font-weight:600;">₹{amount:,.0f}</span>
          <span style="color:#64748b;">{date}</span>
        </div>""", unsafe_allow_html=True)