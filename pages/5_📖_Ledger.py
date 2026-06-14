import streamlit as st
import sqlite3

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif !important; }
.stApp { background: #0a0a12 !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1100px; }
label { color: #94a3b8 !important; font-size: 13px !important; font-weight: 500 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom:28px;">
  <div style="font-size:26px;font-weight:800;color:#f8fafc;">📖 Customer Ledger</div>
  <div style="font-size:13px;color:#475569;margin-top:2px;">Full credit and payment history per customer</div>
</div>
""", unsafe_allow_html=True)

conn = sqlite3.connect("credpulse.db")
customers = conn.execute("SELECT id, name FROM customers").fetchall()

if not customers:
    st.warning("No customers found.")
    st.stop()

selected_customer = st.selectbox("Select Customer", [c[1] for c in customers])
customer_id = next(c[0] for c in customers if c[1] == selected_customer)

total_credit   = conn.execute("SELECT COALESCE(SUM(amount),0) FROM credit_transactions WHERE customer_id=?", (customer_id,)).fetchone()[0]
total_payments = conn.execute("SELECT COALESCE(SUM(amount),0) FROM payments WHERE customer_id=?", (customer_id,)).fetchone()[0]
outstanding    = total_credit - total_payments
collection_pct = (total_payments / total_credit * 100) if total_credit > 0 else 0

st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
for col, label, value, color in [
    (c1, "💳 Total Credit",  f"₹{total_credit:,.0f}",   "#a855f7"),
    (c2, "✅ Total Paid",    f"₹{total_payments:,.0f}", "#34d399"),
    (c3, "⏳ Outstanding",   f"₹{outstanding:,.0f}",    "#fbbf24"),
    (c4, "📊 Collected",     f"{collection_pct:.1f}%",  "#60a5fa"),
]:
    with col:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
          border-top:3px solid {color};border-radius:14px;padding:18px 16px;text-align:center;">
          <div style="font-size:11px;color:#475569;text-transform:uppercase;
            letter-spacing:0.07em;margin-bottom:6px;">{label}</div>
          <div style="font-size:24px;font-weight:800;color:{color};">{value}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
bar_pct = min(collection_pct, 100)
st.markdown(f"""
<div style="background:rgba(255,255,255,0.05);border-radius:999px;height:8px;overflow:hidden;">
  <div style="width:{bar_pct}%;height:100%;
    background:linear-gradient(90deg,#7c3aed,#a855f7,#fbbf24);border-radius:999px;"></div>
</div>
<div style="font-size:12px;color:#475569;margin-top:6px;margin-bottom:24px;">
  {collection_pct:.1f}% collected
</div>
""", unsafe_allow_html=True)

# Credit history
credit_data = conn.execute(
    "SELECT transaction_date, amount, remarks FROM credit_transactions WHERE customer_id=? ORDER BY id DESC",
    (customer_id,)
).fetchall()

st.markdown(f"<div style='font-size:15px;font-weight:700;color:#a78bfa;margin-bottom:12px;'>💳 Credit History ({len(credit_data)} records)</div>", unsafe_allow_html=True)
if credit_data:
    st.markdown("""<div style="display:grid;grid-template-columns:1fr 1fr 2fr;padding:8px 12px;
      font-size:11px;font-weight:600;color:#475569;text-transform:uppercase;letter-spacing:0.07em;
      border-bottom:1px solid rgba(255,255,255,0.07);margin-bottom:4px;">
      <span>Date</span><span>Amount</span><span>Remarks</span></div>""", unsafe_allow_html=True)
    for i, (date, amt, rem) in enumerate(credit_data):
        bg = "rgba(255,255,255,0.02)" if i % 2 == 0 else "transparent"
        st.markdown(f"""<div style="display:grid;grid-template-columns:1fr 1fr 2fr;
          padding:11px 12px;font-size:13px;color:#cbd5e1;background:{bg};border-radius:8px;">
          <span style="color:#94a3b8;">{date}</span>
          <span style="color:#a78bfa;font-weight:600;">₹{amt:,.0f}</span>
          <span style="color:#64748b;">{rem or '—'}</span></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Payment history
payment_data = conn.execute(
    "SELECT payment_date, amount FROM payments WHERE customer_id=? ORDER BY id DESC",
    (customer_id,)
).fetchall()

st.markdown(f"<div style='font-size:15px;font-weight:700;color:#34d399;margin-bottom:12px;'>✅ Payment History ({len(payment_data)} records)</div>", unsafe_allow_html=True)
if payment_data:
    st.markdown("""<div style="display:grid;grid-template-columns:1fr 1fr;padding:8px 12px;
      font-size:11px;font-weight:600;color:#475569;text-transform:uppercase;letter-spacing:0.07em;
      border-bottom:1px solid rgba(255,255,255,0.07);margin-bottom:4px;">
      <span>Date</span><span>Amount</span></div>""", unsafe_allow_html=True)
    for i, (date, amt) in enumerate(payment_data):
        bg = "rgba(255,255,255,0.02)" if i % 2 == 0 else "transparent"
        st.markdown(f"""<div style="display:grid;grid-template-columns:1fr 1fr;
          padding:11px 12px;font-size:13px;color:#cbd5e1;background:{bg};border-radius:8px;">
          <span style="color:#94a3b8;">{date}</span>
          <span style="color:#34d399;font-weight:700;">+₹{amt:,.0f}</span></div>""", unsafe_allow_html=True)

conn.close()