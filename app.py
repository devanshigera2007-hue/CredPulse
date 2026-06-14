import streamlit as st

st.markdown("""
<div style="
background:linear-gradient(135deg,#7C3AED,#A855F7);
padding:40px;
border-radius:25px;
margin-bottom:30px;
">

<h1 style="color:white;font-size:60px;">
💳 CredPulse
</h1>

<h3 style="color:white;">
Credit Intelligence Platform for Local Retailers
</h3>

</div>
""", unsafe_allow_html=True)

st.markdown("## Welcome")

st.write("""
CredPulse helps retailers:

✅ Track customer credit

✅ Monitor repayments

✅ Evaluate customer trust

✅ Assess credit risk

✅ Make smarter credit decisions
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("👥 Customer Management")

with col2:
    st.info("💳 Credit Tracking")

with col3:
    st.warning("🎯 Decision Support")