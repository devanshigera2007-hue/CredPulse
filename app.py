import streamlit as st

st.markdown("""
<div style="
background:linear-gradient(135deg,#7C3AED,#A855F7);
padding:30px;
border-radius:25px;
">

<h1 style="
color:white;
margin:0;
font-size:48px;
">
💳 CredPulse
</h1>

<p style="
color:white;
font-size:18px;
margin-top:10px;
">
AI-Powered Credit Intelligence Platform
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

st.markdown("""
# Welcome 👋

Manage customer credit, monitor repayments,
assess risk, and make smarter lending decisions.
""")

st.write("")

col1,col2,col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="
    background:white;
    padding:25px;
    border-radius:20px;
    border-left:6px solid #7C3AED;
    box-shadow:0px 4px 15px rgba(0,0,0,0.08);
    ">

    <h3>👥 Customers</h3>

    Add and manage customer profiles.

    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
    background:white;
    padding:25px;
    border-radius:20px;
    border-left:6px solid #FACC15;
    box-shadow:0px 4px 15px rgba(0,0,0,0.08);
    ">

    <h3>💳 Credit</h3>

    Record and monitor credit issued.

    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="
    background:white;
    padding:25px;
    border-radius:20px;
    border-left:6px solid #22C55E;
    box-shadow:0px 4px 15px rgba(0,0,0,0.08);
    ">

    <h3>🎯 Decisions</h3>

    View trust score and risk analysis.

    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

st.markdown("## 🚀 Platform Features")

col1,col2 = st.columns(2)

with col1:
    st.success("Track customer credit history")
    st.success("Record repayments")
    st.success("Maintain digital ledger")

with col2:
    st.info("Generate trust scores")
    st.info("Assess customer risk")
    st.info("Receive credit recommendations")

st.write("")
st.write("")

st.markdown("""
<div style="
background:linear-gradient(135deg,#FACC15,#F59E0B);
padding:25px;
border-radius:20px;
color:black;
">

<h2>
📈 Smart Credit Decisions
</h2>

<p>
CredPulse helps local retailers reduce defaults,
identify trustworthy customers and make
data-driven credit decisions.
</p>

</div>
""", unsafe_allow_html=True)