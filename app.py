import streamlit as st
import database

st.set_page_config(
    page_title="CredPulse",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""

<style>

/* Main App */

.stApp{
background:#0F172A;
}

/* Sidebar */

section[data-testid="stSidebar"]{
background:linear-gradient(
180deg,
#111827,
#1E293B
);
}

/* Sidebar Text */

section[data-testid="stSidebar"] *{
color:white !important;
}

/* Headers */

h1,h2,h3{
color:white !important;
}

/* Metric Cards */

[data-testid="metric-container"]{
background:#1E293B;
border:1px solid #334155;
padding:20px;
border-radius:20px;
box-shadow:0px 4px 20px rgba(0,0,0,0.2);
}

/* Buttons */

.stButton button{
background:linear-gradient(
90deg,
#FACC15,
#EAB308
);
color:black;
font-weight:bold;
border:none;
border-radius:12px;
}

/* Tables */

[data-testid="stDataFrame"]{
background:#1E293B;
border-radius:20px;
}

/* Inputs */

.stTextInput input,
.stNumberInput input{
background:#1E293B;
color:white;
}

/* Selectboxes */

div[data-baseweb="select"]{
background:#1E293B;
}

</style>

""", unsafe_allow_html=True)
st.sidebar.markdown("""

# 💳 CredPulse

### Credit Intelligence Platform

---

""")

