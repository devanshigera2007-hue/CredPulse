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
  <div style="font-size:26px;font-weight:800;color:#f8fafc;">🎯 Credit Decision Engine</div>
  <div style="font-size:13px;color:#475569;margin-top:2px;">AI-powered trust scoring and lending recommendations</div>
</div>
""", unsafe_allow_html=True)

conn = sqlite3.connect("credpulse.db")
customers = conn.execute("SELECT id, name FROM customers").fetchall()

if not customers:
    st.warning("No customers found.")
    st.stop()

selected_customer = st.selectbox("Select Customer to Analyse", [c[1] for c in customers])
customer_id = next(c[0] for c in customers if c[1] == selected_customer)

total_credit   = conn.execute("SELECT COALESCE(SUM(amount),0) FROM credit_transactions WHERE customer_id=?", (customer_id,)).fetchone()[0]
total_payments = conn.execute("SELECT COALESCE(SUM(amount),0) FROM payments WHERE customer_id=?", (customer_id,)).fetchone()[0]
tx_count       = conn.execute("SELECT COUNT(*) FROM credit_transactions WHERE customer_id=?", (customer_id,)).fetchone()[0]
conn.close()

outstanding = total_credit - total_payments

trust_score = 100
if outstanding > 5000:   trust_score -= 40
elif outstanding > 2000: trust_score -= 20
elif outstanding > 1000: trust_score -= 10
if total_payments > 0:   trust_score += 5
trust_score = max(0, min(100, trust_score))

if trust_score >= 80:
    risk, risk_color, risk_bg, risk_border = "LOW", "#34d399", "rgba(52,211,153,0.1)", "rgba(52,211,153,0.25)"
    risk_label, recommendation = "🟢 Low Risk", "Safe to extend additional credit"
    rec_detail = "This customer has maintained a healthy repayment profile. Outstanding balance is manageable. Additional credit may be extended confidently."
    gauge_color = "#34d399"
elif trust_score >= 50:
    risk, risk_color, risk_bg, risk_border = "MEDIUM", "#fbbf24", "rgba(251,191,36,0.1)", "rgba(251,191,36,0.25)"
    risk_label, recommendation = "🟡 Medium Risk", "Extend credit with caution"
    rec_detail = "This customer has moderate outstanding dues. Consider setting a tighter credit limit and monitoring repayments closely."
    gauge_color = "#fbbf24"
else:
    risk, risk_color, risk_bg, risk_border = "HIGH", "#f87171", "rgba(248,113,113,0.1)", "rgba(248,113,113,0.25)"
    risk_label, recommendation = "🔴 High Risk", "Do not extend further credit"
    rec_detail = "This customer has elevated credit risk due to high outstanding balance. Further credit extension is not recommended until existing dues are cleared."
    gauge_color = "#f87171"

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(f"""
<div style="background:linear-gradient(135deg,#0f0f1f,#1a0a2e);
  border:1px solid rgba(124,58,237,0.3);border-radius:20px;padding:32px;
  margin-bottom:24px;display:flex;align-items:center;gap:32px;">
  <div style="flex-shrink:0;text-align:center;">
    <div style="width:110px;height:110px;border-radius:50%;
      background:conic-gradient({gauge_color} {trust_score * 3.6}deg, rgba(255,255,255,0.06) 0deg);
      display:flex;align-items:center;justify-content:center;">
      <div style="width:82px;height:82px;border-radius:50%;background:#0a0a12;
        display:flex;flex-direction:column;align-items:center;justify-content:center;">
        <div style="font-size:26px;font-weight:800;color:{gauge_color};line-height:1;">{trust_score}</div>
        <div style="font-size:10px;color:#475569;">/ 100</div>
      </div>
    </div>
    <div style="font-size:11px;color:#475569;margin-top:8px;text-transform:uppercase;letter-spacing:0.08em;">Trust Score</div>
  </div>
  <div style="flex:1;">
    <div style="font-size:11px;color:#7c3aed;font-weight:600;
      text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;">Customer Analysis</div>
    <div style="font-size:20px;font-weight:800;color:#f8fafc;margin-bottom:8px;">{selected_customer}</div>
    <div style="display:inline-block;background:{risk_bg};border:1px solid {risk_border};
      color:{risk_color};padding:4px 14px;border-radius:999px;
      font-size:12px;font-weight:700;margin-bottom:14px;">{risk_label}</div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:8px;">
      <div style="background:rgba(255,255,255,0.04);border-radius:10px;padding:12px;">
        <div style="font-size:10px;color:#475569;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:4px;">Outstanding</div>
        <div style="font-size:17px;font-weight:700;color:#fbbf24;">₹{outstanding:,.0f}</div>
      </div>
      <div style="background:rgba(255,255,255,0.04);border-radius:10px;padding:12px;">
        <div style="font-size:10px;color:#475569;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:4px;">Total Paid</div>
        <div style="font-size:17px;font-weight:700;color:#34d399;">₹{total_payments:,.0f}</div>
      </div>
      <div style="background:rgba(255,255,255,0.04);border-radius:10px;padding:12px;">
        <div style="font-size:10px;color:#475569;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:4px;">Transactions</div>
        <div style="font-size:17px;font-weight:700;color:#a78bfa;">{tx_count}</div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="background:{risk_bg};border:1px solid {risk_border};border-left:4px solid {risk_color};
  border-radius:16px;padding:24px;margin-bottom:24px;">
  <div style="font-size:11px;font-weight:600;color:{risk_color};
    text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">📋 Recommendation</div>
  <div style="font-size:18px;font-weight:700;color:white;margin-bottom:8px;">{recommendation}</div>
  <div style="font-size:13px;color:rgba(255,255,255,0.6);line-height:1.6;">{rec_detail}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='font-size:15px;font-weight:700;color:#cbd5e1;margin-bottom:16px;'>📊 Score Breakdown</div>", unsafe_allow_html=True)

for label, weight, color in [
    ("Repayment Behaviour", 40, "#a855f7"),
    ("Outstanding Exposure", 40, "#fbbf24"),
    ("Transaction History",  20, "#34d399"),
]:
    st.markdown(f"""
    <div style="margin-bottom:14px;">
      <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
        <span style="font-size:13px;color:#94a3b8;">{label}</span>
        <span style="font-size:12px;font-weight:600;color:{color};">{weight}%</span>
      </div>
      <div style="background:rgba(255,255,255,0.06);border-radius:999px;height:6px;overflow:hidden;">
        <div style="width:{weight}%;height:100%;
          background:linear-gradient(90deg,{color}88,{color});border-radius:999px;"></div>
      </div>
    </div>""", unsafe_allow_html=True)