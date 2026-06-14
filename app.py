import streamlit as st

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #0a0a12; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem; max-width: 1100px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
  background: linear-gradient(135deg, #4c1d95 0%, #7c3aed 50%, #a855f7 100%);
  padding: 48px 40px;
  border-radius: 24px;
  margin-bottom: 32px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(124,58,237,0.4);
">
  <div style="position:absolute;top:-40px;right:-40px;width:200px;height:200px;
    background:rgba(250,204,21,0.12);border-radius:50%;"></div>
  <div style="font-size:13px;font-weight:600;color:rgba(250,204,21,0.9);
    letter-spacing:0.15em;text-transform:uppercase;margin-bottom:12px;">
    ⚡ Credit Intelligence Platform
  </div>
  <div style="font-size:52px;font-weight:800;color:white;line-height:1.1;
    letter-spacing:-1.5px;margin-bottom:12px;">
    CredPulse
  </div>
  <div style="font-size:18px;color:rgba(255,255,255,0.75);font-weight:400;max-width:480px;">
    Helping local retailers make smarter credit decisions through AI-powered trust scoring and risk intelligence.
  </div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
cards = [
    ("👥", "Customers", "#7c3aed", "#4c1d95", "Add and manage customer credit profiles with full history."),
    ("💳", "Credit & Payments", "#d97706", "#92400e", "Record credit issued and track repayments in real time."),
    ("🎯", "Risk Engine", "#059669", "#064e3b", "Auto-generate trust scores and lending recommendations."),
]
for col, (icon, title, c1c, c2c, desc) in zip([c1, c2, c3], cards):
    with col:
        st.markdown(f"""
        <div style="
          background: linear-gradient(135deg, {c1c}22, {c2c}44);
          border: 1px solid {c1c}44;
          border-radius: 18px;
          padding: 24px 20px;
          height: 160px;
        ">
          <div style="font-size:28px;margin-bottom:10px;">{icon}</div>
          <div style="font-size:16px;font-weight:700;color:white;margin-bottom:8px;">{title}</div>
          <div style="font-size:13px;color:rgba(255,255,255,0.55);line-height:1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style="
  background: linear-gradient(135deg, #92400e, #d97706, #fbbf24);
  padding: 28px 32px;
  border-radius: 18px;
  box-shadow: 0 8px 32px rgba(217,119,6,0.3);
  display:flex;align-items:center;gap:20px;
">
  <div style="font-size:40px;">📈</div>
  <div>
    <div style="font-size:18px;font-weight:700;color:#1a1a2e;margin-bottom:4px;">
      Built for Bharat's Local Retailers
    </div>
    <div style="font-size:14px;color:rgba(26,26,46,0.75);">
      CredPulse replaces notebooks and WhatsApp with a structured, intelligent credit management system.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    for f in ["Track customer credit history", "Record repayments instantly", "Maintain a digital ledger"]:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;padding:10px 0;
          border-bottom:1px solid rgba(255,255,255,0.06);">
          <span style="color:#a855f7;font-size:18px;">✦</span>
          <span style="color:#cbd5e1;font-size:14px;">{f}</span>
        </div>""", unsafe_allow_html=True)
with col2:
    for f in ["Generate AI trust scores", "Assess customer risk level", "Get credit recommendations"]:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;padding:10px 0;
          border-bottom:1px solid rgba(255,255,255,0.06);">
          <span style="color:#fbbf24;font-size:18px;">✦</span>
          <span style="color:#cbd5e1;font-size:14px;">{f}</span>
        </div>""", unsafe_allow_html=True)