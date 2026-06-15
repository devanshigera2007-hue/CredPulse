import streamlit as st
import sqlite3

# ==========================
# PAGE STYLE
# ==========================

st.markdown("""
<style>

/* ── Base ── */
[data-testid="stAppViewContainer"] {
    background-color: #0e1117;
}
[data-testid="stMainBlockContainer"] {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* ── Page header ── */
.page-title {
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.15rem;
}
.page-subtitle {
    font-size: 0.9rem;
    color: #6b7280;
    margin-bottom: 1.8rem;
}

/* ── Stat cards (top row) ── */
.stat-card {
    background: #12151f;
    border-radius: 14px;
    padding: 1.3rem 1.4rem 1.2rem;
    border-top: 3px solid #7c3aed;
    height: 100%;
}
.stat-card.amber  { border-top-color: #f59e0b; }
.stat-card.green  { border-top-color: #10b981; }
.stat-card.blue   { border-top-color: #3b82f6; }
.stat-card.purple { border-top-color: #7c3aed; }
.stat-card.red    { border-top-color: #ef4444; }

.stat-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 0.45rem;
}
.stat-icon {
    font-size: 1.4rem;
    margin-bottom: 0.5rem;
    display: block;
}
.stat-value {
    font-size: 2rem;
    font-weight: 800;
    color: #a78bfa;
    line-height: 1.1;
}
.stat-value.amber  { color: #f59e0b; }
.stat-value.green  { color: #10b981; }
.stat-value.blue   { color: #60a5fa; }
.stat-value.white  { color: #ffffff; }
.stat-value.red    { color: #ef4444; }

.stat-sub {
    font-size: 0.78rem;
    color: #6b7280;
    margin-top: 0.3rem;
}

/* ── Score gauge card ── */
.score-card {
    background: linear-gradient(135deg, #1e1b4b 0%, #1a1d2e 100%);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    border: 1px solid #2d2f45;
    margin-bottom: 1.2rem;
}
.score-big {
    font-size: 5rem;
    font-weight: 900;
    line-height: 1;
}
.score-label {
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #9ca3af;
    margin-top: 0.4rem;
}
.score-bar-bg {
    background: #2d2f45;
    border-radius: 999px;
    height: 10px;
    margin: 1.2rem auto 0;
    max-width: 280px;
    overflow: hidden;
}
.score-bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.6s ease;
}

/* ── Risk banner ── */
.risk-banner {
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.risk-banner.low    { background: #052e16; border: 1px solid #16a34a; }
.risk-banner.medium { background: #1c1700; border: 1px solid #ca8a04; }
.risk-banner.high   { background: #1f0808; border: 1px solid #dc2626; }

.risk-badge {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
}
.risk-badge.low    { background: #16a34a22; color: #4ade80; }
.risk-badge.medium { background: #ca8a0422; color: #fbbf24; }
.risk-badge.high   { background: #dc262622; color: #f87171; }

.risk-rec {
    color: #d1d5db;
    font-size: 0.95rem;
    font-weight: 500;
}

/* ── Factor cards ── */
.factor-card {
    background: #12151f;
    border-radius: 14px;
    padding: 1.3rem 1.4rem;
    height: 100%;
}
.factor-card.repayment { border-top: 3px solid #10b981; }
.factor-card.exposure  { border-top: 3px solid #f59e0b; }
.factor-card.history   { border-top: 3px solid #3b82f6; }

.factor-title {
    font-size: 0.85rem;
    font-weight: 700;
    color: #e5e7eb;
    margin: 0.5rem 0 0.25rem;
}
.factor-weight {
    font-size: 0.7rem;
    color: #6b7280;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.9rem;
}
.factor-value {
    font-size: 1.5rem;
    font-weight: 800;
    margin-bottom: 0.3rem;
}
.factor-value.green  { color: #10b981; }
.factor-value.amber  { color: #f59e0b; }
.factor-value.blue   { color: #60a5fa; }
.factor-desc {
    font-size: 0.78rem;
    color: #6b7280;
}

/* ── Summary card ── */
.summary-card {
    background: #12151f;
    border-radius: 14px;
    padding: 1.5rem 1.6rem;
    margin-top: 0.5rem;
}
.summary-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 0;
    border-bottom: 1px solid #1f2233;
    font-size: 0.9rem;
}
.summary-row:last-child { border-bottom: none; }
.summary-key   { color: #9ca3af; }
.summary-val   { color: #e5e7eb; font-weight: 600; }
.summary-val.accent { color: #a78bfa; }

/* ── Section header ── */
.section-header {
    font-size: 1.1rem;
    font-weight: 700;
    color: #ffffff;
    margin: 1.6rem 0 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Selectbox label ── */
.select-label {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 0.4rem;
}

/* ── Streamlit overrides ── */
div[data-baseweb="select"] > div {
    background-color: #12151f !important;
    border: 1px solid #2d2f45 !important;
    border-radius: 10px !important;
    color: #e5e7eb !important;
}
div[data-baseweb="select"] * { color: #e5e7eb !important; }
[data-testid="stSelectbox"] label { display: none; }

</style>
""", unsafe_allow_html=True)

# ==========================
# DATABASE
# ==========================

conn = sqlite3.connect("credpulse.db")

customers = conn.execute(
    "SELECT id, name FROM customers"
).fetchall()

if not customers:
    st.warning("No customers found.")
    st.stop()

# ==========================
# PAGE HEADER
# ==========================

st.markdown('<div class="page-title">🎯 Credit Decision Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Customer trust scoring and lending recommendations</div>', unsafe_allow_html=True)

# ==========================
# CUSTOMER SELECTOR
# ==========================

st.markdown('<div class="select-label">Select Customer</div>', unsafe_allow_html=True)
selected_customer = st.selectbox(
    "Select Customer",
    [c[1] for c in customers],
    label_visibility="collapsed"
)

customer_id = next(
    c[0] for c in customers if c[1] == selected_customer
)

# ==========================
# CUSTOMER DATA
# ==========================

total_credit = conn.execute(
    "SELECT COALESCE(SUM(amount),0) FROM credit_transactions WHERE customer_id=?",
    (customer_id,)
).fetchone()[0]

total_payments = conn.execute(
    "SELECT COALESCE(SUM(amount),0) FROM payments WHERE customer_id=?",
    (customer_id,)
).fetchone()[0]

tx_count = conn.execute(
    "SELECT COUNT(*) FROM credit_transactions WHERE customer_id=?",
    (customer_id,)
).fetchone()[0]

conn.close()

outstanding = total_credit - total_payments

# ==========================
# CREDIT SCORE MODEL  ← untouched
# ==========================

score = 50

if outstanding <= 500:
    score += 25
elif outstanding <= 2000:
    score += 15
elif outstanding <= 5000:
    score += 5
else:
    score -= 20

if total_credit > 0:
    repayment_ratio = total_payments / total_credit
    if repayment_ratio >= 0.80:
        score += 20
    elif repayment_ratio >= 0.50:
        score += 10
    elif repayment_ratio > 0:
        score += 5
    else:
        score -= 10

if tx_count >= 10:
    score += 15
elif tx_count >= 5:
    score += 10
elif tx_count >= 2:
    score += 5

score = max(0, min(100, round(score)))

# ==========================
# RISK LEVEL  ← untouched
# ==========================

if score >= 80:
    risk_level = "low"
    risk_label = "🟢 LOW RISK"
    recommendation = "Safe to extend additional credit"
elif score >= 50:
    risk_level = "medium"
    risk_label = "🟡 MEDIUM RISK"
    recommendation = "Extend credit with caution"
else:
    risk_level = "high"
    risk_label = "🔴 HIGH RISK"
    recommendation = "Do not extend further credit"

repayment_ratio_pct = (
    round((total_payments / total_credit) * 100, 1)
    if total_credit > 0 else 0
)

# ==========================
# SCORE GAUGE
# ==========================

if score >= 80:
    score_color = "#10b981"
    bar_color   = "#10b981"
elif score >= 50:
    score_color = "#f59e0b"
    bar_color   = "#f59e0b"
else:
    score_color = "#ef4444"
    bar_color   = "#ef4444"

st.markdown(f"""
<div class="score-card">
    <div class="stat-label" style="color:#9ca3af;">TRUST SCORE</div>
    <div class="score-big" style="color:{score_color};">{score}</div>
    <div class="score-label">out of 100</div>
    <div class="score-bar-bg">
        <div class="score-bar-fill"
             style="width:{score}%; background:{bar_color};"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================
# RISK BANNER
# ==========================

st.markdown(f"""
<div class="risk-banner {risk_level}">
    <span class="risk-badge {risk_level}">{risk_label}</span>
    <span class="risk-rec">{recommendation}</span>
</div>
""", unsafe_allow_html=True)

# ==========================
# TOP METRICS ROW
# ==========================

st.markdown('<div class="section-header">📊 Score Breakdown</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card purple">
        <span class="stat-icon">🎯</span>
        <div class="stat-label">Trust Score</div>
        <div class="stat-value">{score}<span style="font-size:1rem;color:#6b7280;">/100</span></div>
        <div class="stat-sub">Overall creditworthiness</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card amber">
        <span class="stat-icon">⏳</span>
        <div class="stat-label">Outstanding</div>
        <div class="stat-value amber">₹{outstanding:,.0f}</div>
        <div class="stat-sub">Yet to be collected</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card green">
        <span class="stat-icon">✅</span>
        <div class="stat-label">Repayment Rate</div>
        <div class="stat-value green">{repayment_ratio_pct}%</div>
        <div class="stat-sub">₹{total_payments:,.0f} paid back</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card blue">
        <span class="stat-icon">📦</span>
        <div class="stat-label">Transactions</div>
        <div class="stat-value blue">{tx_count}</div>
        <div class="stat-sub">Total credit events</div>
    </div>
    """, unsafe_allow_html=True)

# spacing
st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ==========================
# FACTOR CARDS
# ==========================

st.markdown('<div class="section-header">⚙️ Score Factors</div>', unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown(f"""
    <div class="factor-card repayment">
        <div style="font-size:1.5rem">💳</div>
        <div class="factor-title">Repayment Behaviour</div>
        <div class="factor-weight">40% weight</div>
        <div class="factor-value green">₹{total_payments:,.0f}</div>
        <div class="factor-desc">repaid so far — higher repayments increase trust</div>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown(f"""
    <div class="factor-card exposure">
        <div style="font-size:1.5rem">📉</div>
        <div class="factor-title">Credit Exposure</div>
        <div class="factor-weight">40% weight</div>
        <div class="factor-value amber">₹{outstanding:,.0f}</div>
        <div class="factor-desc">outstanding — lower exposure reduces risk</div>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown(f"""
    <div class="factor-card history">
        <div style="font-size:1.5rem">📈</div>
        <div class="factor-title">Transaction History</div>
        <div class="factor-weight">20% weight</div>
        <div class="factor-value blue">{tx_count}</div>
        <div class="factor-desc">transactions — more history improves reliability</div>
    </div>
    """, unsafe_allow_html=True)

# spacing
st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ==========================
# CREDIT SUMMARY
# ==========================

st.markdown('<div class="section-header">🧾 Credit Summary</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="summary-card">
    <div class="summary-row">
        <span class="summary-key">Customer</span>
        <span class="summary-val">{selected_customer}</span>
    </div>
    <div class="summary-row">
        <span class="summary-key">Total Credit Issued</span>
        <span class="summary-val accent">₹{total_credit:,.0f}</span>
    </div>
    <div class="summary-row">
        <span class="summary-key">Total Payments Received</span>
        <span class="summary-val" style="color:#10b981;">₹{total_payments:,.0f}</span>
    </div>
    <div class="summary-row">
        <span class="summary-key">Outstanding Balance</span>
        <span class="summary-val" style="color:#f59e0b;">₹{outstanding:,.0f}</span>
    </div>
    <div class="summary-row">
        <span class="summary-key">Repayment Rate</span>
        <span class="summary-val">{repayment_ratio_pct}%</span>
    </div>
    <div class="summary-row">
        <span class="summary-key">Number of Transactions</span>
        <span class="summary-val">{tx_count}</span>
    </div>
    <div class="summary-row">
        <span class="summary-key">Trust Score</span>
        <span class="summary-val accent">{score} / 100</span>
    </div>
    <div class="summary-row">
        <span class="summary-key">Risk Level</span>
        <span class="summary-val">{risk_label}</span>
    </div>
    <div class="summary-row">
        <span class="summary-key">Recommendation</span>
        <span class="summary-val">{recommendation}</span>
    </div>
</div>
""", unsafe_allow_html=True)