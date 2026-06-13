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

/* Main App Background */
.stApp {
    background-color: #0F172A;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #111827 0%,
        #1E293B 100%
    );
}

/* Sidebar Text */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background: #1E293B;
    border: 1px solid #334155;
    padding: 20px;
    border-radius: 16px;
}

/* Buttons */
.stButton button {
    background: linear-gradient(
        90deg,
        #6366F1,
        #8B5CF6
    );
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: bold;
}

/* Inputs */
.stTextInput input,
.stNumberInput input,
.stSelectbox {
    border-radius: 12px !important;
}

/* Headers */
h1,h2,h3 {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)
st.sidebar.markdown("""
# 💳 CredPulse

### Credit Intelligence Platform

---

Built for Local Retailers

""")

st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}

.stMetric {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
}

h1 {
    color: #0f172a;
}

</style>
""", unsafe_allow_html=True)

st.title("💳 CredPulse")

st.markdown("""
### Credit Intelligence Platform for Local Retailers

Helping retailers make smarter credit decisions through customer insights, trust scoring, and risk assessment.
""")

st.info("Use the sidebar to navigate through the platform.")
