import streamlit as st

st.set_page_config(
    page_title="CredPulse",
    page_icon="💳",
    layout="wide"
)
st.markdown("""
<div style="
background:linear-gradient(135deg,#7C3AED,#A855F7);
padding:40px;
border-radius:25px;
margin-bottom:30px;
">

<h1 style="color:white;">
💳 CredPulse
</h1>

<h3 style="color:white;">
Credit Intelligence Platform for Local Retailers
</h3>

</div>
""", unsafe_allow_html=True)

col1,col2,col3 = st.columns(3)

with col1:
    st.info("👥 Customer Management")

with col2:
    st.success("💰 Credit Tracking")

with col3:
    st.warning("🎯 Smart Credit Decisions")

st.markdown("---")

st.header("Welcome")

st.write("""
CredPulse helps local retailers:

✅ Track customer credit

✅ Monitor repayments

✅ Calculate trust scores

✅ Assess risk levels

✅ Make smarter credit decisions
""")