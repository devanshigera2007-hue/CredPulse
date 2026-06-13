import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ── GLOBAL THEME INJECTION ──────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    /* ── Import Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Base ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #0d0d14;
        color: #e2e8f0;
    }

    /* ── Hide default Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container {
        padding: 2rem 2.5rem 3rem 2.5rem;
        max-width: 1200px;
    }

    /* ── Page header ── */
    .cp-page-header {
        margin-bottom: 2rem;
    }
    .cp-page-header h1 {
        font-size: 1.75rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 0 0 0.25rem 0;
        letter-spacing: -0.5px;
    }
    .cp-page-header p {
        font-size: 0.875rem;
        color: #64748b;
        margin: 0;
    }

    /* ── Metric cards ── */
    .cp-metric-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.4rem 1.5rem;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        position: relative;
        overflow: hidden;
        transition: border-color 0.2s ease;
    }
    .cp-metric-card:hover {
        border-color: rgba(255,255,255,0.16);
    }
    .cp-metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        border-radius: 16px 16px 0 0;
    }
    .cp-metric-card.purple::before { background: linear-gradient(90deg, #7c3aed, #a855f7); }
    .cp-metric-card.blue::before   { background: linear-gradient(90deg, #2563eb, #38bdf8); }
    .cp-metric-card.green::before  { background: linear-gradient(90deg, #059669, #34d399); }
    .cp-metric-card.amber::before  { background: linear-gradient(90deg, #d97706, #fbbf24); }

    .cp-metric-label {
        font-size: 0.75rem;
        font-weight: 500;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.6rem;
    }
    .cp-metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #f8fafc;
        letter-spacing: -1px;
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    .cp-metric-value.purple { color: #a78bfa; }
    .cp-metric-value.blue   { color: #60a5fa; }
    .cp-metric-value.green  { color: #34d399; }
    .cp-metric-value.amber  { color: #fbbf24; }

    .cp-metric-sub {
        font-size: 0.78rem;
        color: #475569;
    }
    .cp-metric-sub .up   { color: #34d399; }
    .cp-metric-sub .down { color: #f87171; }

    .cp-metric-icon {
        position: absolute;
        top: 1.2rem; right: 1.4rem;
        font-size: 1.4rem;
        opacity: 0.25;
    }

    /* ── Section headers ── */
    .cp-section-title {
        font-size: 1rem;
        font-weight: 600;
        color: #cbd5e1;
        margin: 2rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .cp-section-title::after {
        content: '';
        flex: 1;
        height: 1px;
        background: rgba(255,255,255,0.06);
        margin-left: 0.5rem;
    }

    /* ── Chart container ── */
    .cp-chart-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 1.25rem 1.5rem 0.5rem 1.5rem;
    }
    .cp-chart-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #94a3b8;
        margin-bottom: 0.25rem;
    }

    /* ── Risk badge ── */
    .cp-badge {
        display: inline-block;
        padding: 0.2rem 0.65rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .cp-badge.low    { background: rgba(52,211,153,0.12); color: #34d399; border: 1px solid rgba(52,211,153,0.2); }
    .cp-badge.medium { background: rgba(251,191,36,0.12);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.2); }
    .cp-badge.high   { background: rgba(248,113,113,0.12); color: #f87171; border: 1px solid rgba(248,113,113,0.2); }

    /* ── Customer table ── */
    .cp-table-header {
        display: grid;
        grid-template-columns: 2fr 1fr 1fr 1fr 0.8fr;
        padding: 0.5rem 0.75rem;
        font-size: 0.72rem;
        font-weight: 600;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 0.25rem;
    }
    .cp-table-row {
        display: grid;
        grid-template-columns: 2fr 1fr 1fr 1fr 0.8fr;
        padding: 0.75rem 0.75rem;
        font-size: 0.85rem;
        color: #cbd5e1;
        border-radius: 8px;
        align-items: center;
        transition: background 0.15s;
    }
    .cp-table-row:hover { background: rgba(255,255,255,0.04); }
    .cp-table-row .name { font-weight: 500; color: #f1f5f9; }

    /* ── Divider ── */
    hr { border-color: rgba(255,255,255,0.06) !important; }

    /* ── Streamlit plotly background fix ── */
    .js-plotly-plot .plotly .bg { fill: transparent !important; }
    </style>
    """, unsafe_allow_html=True)


# ── DB HELPERS ───────────────────────────────────────────────────────────────
def get_connection():
    # Change this path to match your actual DB file
    return sqlite3.connect("credpulse.db", check_same_thread=False)

def fetch_dashboard_data():
    conn = get_connection()

    total_credit = pd.read_sql("SELECT COALESCE(SUM(amount),0) as val FROM credit_transactions", conn).iloc[0,0]
    total_paid   = pd.read_sql("SELECT COALESCE(SUM(amount),0) as val FROM payments", conn).iloc[0,0]
    outstanding  = total_credit - total_paid
    cust_count   = pd.read_sql("SELECT COUNT(*) as val FROM customers", conn).iloc[0,0]
    collection_rate = (total_paid / total_credit * 100) if total_credit > 0 else 0

    # Monthly credit trend (last 6 months)
    trend = pd.read_sql("""
        SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
        FROM credit_transactions
        GROUP BY month ORDER BY month DESC LIMIT 6
    """, conn)
    trend = trend.iloc[::-1].reset_index(drop=True)

    # Top customers by outstanding
    top_customers = pd.read_sql("""
        SELECT c.name,
               COALESCE(SUM(ct.amount),0) as credited,
               COALESCE((SELECT SUM(p.amount) FROM payments p WHERE p.customer_id = c.id),0) as paid
        FROM customers c
        LEFT JOIN credit_transactions ct ON ct.customer_id = c.id
        GROUP BY c.id, c.name
        ORDER BY (credited - paid) DESC LIMIT 6
    """, conn)
    top_customers["outstanding"] = top_customers["credited"] - top_customers["paid"]
    top_customers["payment_ratio"] = (top_customers["paid"] / top_customers["credited"].replace(0,1) * 100).round(1)

    # Risk distribution (simple rule-based)
    all_customers = pd.read_sql("""
        SELECT c.id, c.name, c.credit_limit,
               COALESCE(SUM(ct.amount),0) as credited,
               COALESCE((SELECT SUM(p.amount) FROM payments p WHERE p.customer_id = c.id),0) as paid
        FROM customers c
        LEFT JOIN credit_transactions ct ON ct.customer_id = c.id
        GROUP BY c.id
    """, conn)
    conn.close()

    all_customers["outstanding"] = all_customers["credited"] - all_customers["paid"]
    all_customers["payment_ratio"] = (all_customers["paid"] / all_customers["credited"].replace(0,1))

    def trust_score(row):
        score = 100
        if row["outstanding"] > 5000:  score -= 30
        elif row["outstanding"] > 2000: score -= 15
        if row["payment_ratio"] < 0.3:  score -= 30
        elif row["payment_ratio"] < 0.6: score -= 15
        return max(0, score)

    all_customers["score"] = all_customers.apply(trust_score, axis=1)
    all_customers["risk"] = all_customers["score"].apply(
        lambda s: "Low" if s >= 80 else ("Medium" if s >= 60 else "High")
    )
    risk_dist = all_customers["risk"].value_counts().to_dict()

    return {
        "total_credit": total_credit,
        "total_paid": total_paid,
        "outstanding": outstanding,
        "cust_count": cust_count,
        "collection_rate": collection_rate,
        "trend": trend,
        "top_customers": top_customers,
        "risk_dist": risk_dist,
        "all_customers": all_customers,
    }


# ── CHART BUILDERS ───────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#94a3b8", size=12),
    margin=dict(l=0, r=0, t=10, b=0),
    showlegend=False,
)

def trend_chart(df):
    if df.empty:
        return None
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["month"], y=df["total"],
        mode="lines+markers",
        line=dict(color="#7c3aed", width=2.5),
        marker=dict(color="#a855f7", size=6),
        fill="tozeroy",
        fillcolor="rgba(124,58,237,0.08)",
        hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=200,
        xaxis=dict(showgrid=False, showline=False, tickcolor="#475569"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", showline=False,
                   tickprefix="₹", tickformat=","),
    )
    return fig

def risk_donut(risk_dist):
    labels = list(risk_dist.keys())
    values = list(risk_dist.values())
    colors = {"Low": "#34d399", "Medium": "#fbbf24", "High": "#f87171"}
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.65,
        marker=dict(colors=[colors.get(l, "#94a3b8") for l in labels],
                    line=dict(color="#0d0d14", width=2)),
        hovertemplate="<b>%{label}</b>: %{value} customers<extra></extra>",
        textinfo="none",
    ))
    total = sum(values)
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=200,
        annotations=[dict(text=f"<b>{total}</b><br><span style='font-size:10px'>customers</span>",
                          showarrow=False, font=dict(color="#f8fafc", size=16))],
    )
    return fig

def bar_chart(top_customers):
    if top_customers.empty:
        return None
    names = top_customers["name"].str[:12]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=names, y=top_customers["credited"],
        name="Credited", marker_color="rgba(99,102,241,0.7)",
        hovertemplate="<b>%{x}</b><br>Credited: ₹%{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=names, y=top_customers["paid"],
        name="Paid", marker_color="rgba(52,211,153,0.7)",
        hovertemplate="<b>%{x}</b><br>Paid: ₹%{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1,
                    font=dict(size=11, color="#94a3b8")),
        height=220,
        barmode="group",
        bargap=0.25,
        xaxis=dict(showgrid=False, tickcolor="#475569"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)",
                   tickprefix="₹", tickformat=","),
    )
    return fig


# ── MAIN PAGE ────────────────────────────────────────────────────────────────
def show_dashboard():
    inject_css()

    # Page header
    now = datetime.now().strftime("%d %b %Y")
    st.markdown(f"""
    <div class="cp-page-header">
        <h1>Dashboard</h1>
        <p>CredPulse · {now}</p>
    </div>
    """, unsafe_allow_html=True)

    data = fetch_dashboard_data()

    # ── Top metric cards ──────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="cp-metric-card purple">
            <div class="cp-metric-icon">💳</div>
            <div class="cp-metric-label">Total Credit Issued</div>
            <div class="cp-metric-value purple">₹{data['total_credit']:,.0f}</div>
            <div class="cp-metric-sub">Lifetime across all customers</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="cp-metric-card amber">
            <div class="cp-metric-icon">⏳</div>
            <div class="cp-metric-label">Outstanding Balance</div>
            <div class="cp-metric-value amber">₹{data['outstanding']:,.0f}</div>
            <div class="cp-metric-sub">Yet to be collected</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="cp-metric-card green">
            <div class="cp-metric-icon">✅</div>
            <div class="cp-metric-label">Collection Rate</div>
            <div class="cp-metric-value green">{data['collection_rate']:.1f}%</div>
            <div class="cp-metric-sub">₹{data['total_paid']:,.0f} recovered</div>
        </div>""", unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="cp-metric-card blue">
            <div class="cp-metric-icon">👥</div>
            <div class="cp-metric-label">Customers</div>
            <div class="cp-metric-value blue">{data['cust_count']}</div>
            <div class="cp-metric-sub">Active credit accounts</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row ────────────────────────────────────────────────────────────
    st.markdown('<div class="cp-section-title">📈 Analytics</div>', unsafe_allow_html=True)

    ch1, ch2 = st.columns([2, 1])

    with ch1:
        st.markdown('<div class="cp-chart-card"><div class="cp-chart-title">Credit Issued — Monthly Trend</div>', unsafe_allow_html=True)
        fig = trend_chart(data["trend"])
        if fig:
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown("<p style='color:#475569;font-size:0.85rem;padding:1rem 0'>No transaction data yet.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with ch2:
        st.markdown('<div class="cp-chart-card"><div class="cp-chart-title">Customer Risk Distribution</div>', unsafe_allow_html=True)
        rd = data["risk_dist"]
        if rd:
            fig2 = risk_donut(rd)
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
            # Legend
            color_map = {"Low": "#34d399", "Medium": "#fbbf24", "High": "#f87171"}
            legend_html = "<div style='display:flex;gap:1rem;justify-content:center;padding:0 0 0.75rem 0'>"
            for risk, count in rd.items():
                c = color_map.get(risk, "#94a3b8")
                legend_html += f"<span style='font-size:0.75rem;color:{c}'>● {risk} ({count})</span>"
            legend_html += "</div>"
            st.markdown(legend_html, unsafe_allow_html=True)
        else:
            st.markdown("<p style='color:#475569;font-size:0.85rem;padding:1rem 0'>No customer data yet.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Credit vs Payment bar chart ───────────────────────────────────────────
    st.markdown('<div class="cp-section-title">💰 Credit vs Payments — Top Customers</div>', unsafe_allow_html=True)
    st.markdown('<div class="cp-chart-card">', unsafe_allow_html=True)
    fig3 = bar_chart(data["top_customers"])
    if fig3:
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Top customers table ───────────────────────────────────────────────────
    st.markdown('<div class="cp-section-title">🏆 Top Outstanding Accounts</div>', unsafe_allow_html=True)

    df = data["top_customers"].head(6)
    all_c = data["all_customers"]

    if not df.empty:
        st.markdown("""
        <div class="cp-table-header">
            <span>Customer</span>
            <span>Credited</span>
            <span>Paid</span>
            <span>Outstanding</span>
            <span>Risk</span>
        </div>""", unsafe_allow_html=True)

        for _, row in df.iterrows():
            # get risk from all_customers
            match = all_c[all_c["name"] == row["name"]]
            risk = match["risk"].values[0] if not match.empty else "—"
            risk_class = risk.lower() if risk in ["Low","Medium","High"] else ""

            st.markdown(f"""
            <div class="cp-table-row">
                <span class="name">{row['name']}</span>
                <span>₹{row['credited']:,.0f}</span>
                <span>₹{row['paid']:,.0f}</span>
                <span>₹{row['outstanding']:,.0f}</span>
                <span><span class="cp-badge {risk_class}">{risk}</span></span>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:#475569;font-size:0.85rem'>No customer data yet.</p>", unsafe_allow_html=True)


# ── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    st.set_page_config(
        page_title="CredPulse",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    show_dashboard()