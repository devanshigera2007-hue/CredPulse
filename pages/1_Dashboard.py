import streamlit as st

st.title("📊 Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Outstanding Credit",
        "₹28,500",
        "+12%"
    )

with col2:
    st.metric(
        "Customers",
        "47",
        "+5"
    )

with col3:
    st.metric(
        "Overdue Amount",
        "₹4,200",
        "-8%"
    )

with col4:
    st.metric(
        "Collection Rate",
        "88%",
        "+3%"
    )

st.divider()

st.subheader("Business Overview")

st.line_chart(
    {
        "Credit Issued":[1000,2000,1500,3000,2500,4000],
        "Collections":[500,1800,1200,2800,2200,3500]
    }
)