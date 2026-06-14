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

/* Background */

.stApp{
background:#FFFDF7;
}

/* Sidebar */

section[data-testid="stSidebar"]{
background:linear-gradient(
180deg,
#7C3AED,
#A855F7
);
}

/* Sidebar text */

section[data-testid="stSidebar"] *{
color:white !important;
}

/* Main headings */

h1{
color:#7C3AED !important;
}

h2{
color:#7C3AED !important;
}

/* Metric Cards */

[data-testid="metric-container"]{
background:white;
padding:20px;
border-radius:20px;
border:2px solid #FACC15;
box-shadow:
0px 4px 15px rgba(0,0,0,0.08);
}

/* Buttons */

.stButton button{

background:linear-gradient(
90deg,
#FACC15,
#F59E0B
);

color:black;

border:none;

border-radius:14px;

font-weight:bold;

padding:10px 25px;
}

</style>
""", unsafe_allow_html=True)
