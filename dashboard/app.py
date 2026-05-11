from __future__ import annotations

import pandas as pd
import streamlit as st

st.set_page_config(page_title="AML Alert Prioritisation", layout="wide")
st.title("Transaction Monitoring & AML Alert Prioritisation System")

@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv("reports/alert_queue_summary.csv")

try:
    df = load_data()
except Exception:
    st.warning("Run the pipeline first to generate reports/alert_queue_summary.csv")
    st.stop()

st.sidebar.header("Filters")
risk_filter = st.sidebar.multiselect("Risk band", sorted(df["risk_band"].dropna().unique()), default=sorted(df["risk_band"].dropna().unique()))
country_filter = st.sidebar.multiselect("Country", sorted(df["country"].dropna().unique()), default=sorted(df["country"].dropna().unique())[:10])

fdf = df[df["risk_band"].isin(risk_filter) & df["country"].isin(country_filter)]

c1, c2, c3 = st.columns(3)
c1.metric("Transactions", f"{len(fdf):,}")
c2.metric("Avg Risk Score", f"{fdf['risk_score'].mean():.1f}")
if "is_suspicious" in fdf:
    c3.metric("Known suspicious rate", f"{100*fdf['is_suspicious'].mean():.1f}%")

st.subheader("Top Priority Alerts")
st.dataframe(
    fdf.sort_values("risk_score", ascending=False)[
        ["transaction_id", "account_id", "amount", "country", "risk_score", "risk_band", "explanation"]
    ].head(200),
    use_container_width=True,
)

st.subheader("Risk Band Distribution")
st.bar_chart(fdf["risk_band"].value_counts().sort_index())
