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
