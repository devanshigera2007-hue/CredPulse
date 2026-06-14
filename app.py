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

.stApp {
    background-color: #0F172A;
}

section[data-testid="stSidebar"] {
    background: #1E1B4B;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

h1, h2, h3 {
    color: white !important;
}

[data-testid="metric-container"] {
    background: #1E293B;
    border-radius: 15px;
    padding: 15px;
    border: 1px solid #334155;
}

.stButton button {
    background: #FACC15;
    color: black;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
# 💳 CredPulse

### Credit Intelligence Platform

---

📊 Portfolio Health

🟢 Excellent

---

🎯 Decision Accuracy

96%

---

🏆 Trusted Retail Network
""")