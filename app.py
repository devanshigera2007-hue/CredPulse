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

/* =========================
   MAIN APP
========================= */

.stApp{
background: linear-gradient(
135deg,
#050816 0%,
#0F172A 40%,
#111827 100%
);
color:white;
}

/* =========================
   SIDEBAR
========================= */

section[data-testid="stSidebar"]{
background: linear-gradient(
180deg,
#12071F,
#24103A,
#3B1364
);
border-right:1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] *{
color:white !important;
}

/* =========================
   HEADINGS
========================= */

h1{
color:white !important;
font-weight:800 !important;
}

h2{
color:white !important;
font-weight:700 !important;
}

h3{
color:white !important;
}

/* =========================
   METRIC CARDS
========================= */

[data-testid="metric-container"]{

background: rgba(255,255,255,0.05);

border:1px solid rgba(255,255,255,0.08);

padding:20px;

border-radius:24px;

backdrop-filter: blur(12px);

box-shadow:
0px 8px 30px rgba(0,0,0,0.35);

}

/* =========================
   BUTTONS
========================= */

.stButton button{

background: linear-gradient(
90deg,
#FACC15,
#F59E0B
);

color:black;

font-weight:700;

border:none;

border-radius:14px;

padding:12px 24px;

transition:0.3s;

}

.stButton button:hover{

transform:translateY(-2px);

box-shadow:
0px 0px 20px rgba(250,204,21,0.4);

}

/* =========================
   INPUTS
========================= */

.stTextInput input,
.stNumberInput input,
.stDateInput input{

background:#1E293B !important;

color:white !important;

border-radius:12px !important;

}

/* =========================
   SELECT BOXES
========================= */

div[data-baseweb="select"]{

background:#1E293B;

border-radius:12px;

}

/* =========================
   TABLES
========================= */

[data-testid="stDataFrame"]{

background:#1E293B;

border-radius:20px;

padding:10px;

}

/* =========================
   SUCCESS BOX
========================= */

.stSuccess{

border-radius:20px;

}

/* =========================
   INFO BOX
========================= */

.stInfo{

border-radius:20px;

}

/* =========================
   GOLD GLOW
========================= */

.gold-card{

background:linear-gradient(
135deg,
#FACC15,
#F59E0B
);

padding:25px;

border-radius:24px;

color:black;

font-weight:bold;

box-shadow:
0px 10px 25px rgba(250,204,21,0.3);

}

/* =========================
   PURPLE CARD
========================= */

.purple-card{

background:linear-gradient(
135deg,
#6D28D9,
#9333EA
);

padding:25px;

border-radius:24px;

color:white;

box-shadow:
0px 10px 25px rgba(147,51,234,0.3);

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

---

Built for Local Retailers
""")