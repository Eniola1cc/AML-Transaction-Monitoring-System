from __future__ import annotations

import pandas as pd
import streamlit as st

st.set_page_config(page_title="AML Alert Prioritisation", layout="wide")
st.title("Transaction Monitoring & AML Alert Prioritisation System")

st.sidebar.title("AML Dashboard")
st.sidebar.info(
    """
    AML Transaction Monitoring System

    Features:
    - Rule-Based Detection
    - ML Risk Scoring
    - Alert Prioritisation
    - Fraud Analytics
    """
)
st.sidebar.header("Filters")


@st.cache_data
def load_alert_data() -> pd.DataFrame:
    return pd.read_csv("reports/alert_queue_summary.csv")


@st.cache_data
def load_optional_report(path: str) -> pd.DataFrame | None:
    try:
        return pd.read_csv(path)
    except Exception:
        return None


try:
    df = load_alert_data()
except Exception:
    st.warning("Run the pipeline first to generate reports/alert_queue_summary.csv")
    st.stop()

risk_filter = st.sidebar.multiselect(
    "Risk band",
    sorted(df["risk_band"].dropna().unique()),
    default=sorted(df["risk_band"].dropna().unique()),
)
country_filter = st.sidebar.multiselect(
    "Country",
    sorted(df["country"].dropna().unique()),
    default=sorted(df["country"].dropna().unique())[:10],
)

filtered_alerts = df[df["risk_band"].isin(risk_filter) & df["country"].isin(country_filter)]

c1, c2, c3 = st.columns(3)
c1.metric("Transactions", f"{len(filtered_alerts):,}")
c2.metric("Avg Risk Score", f"{filtered_alerts['risk_score'].mean():.1f}")
if "is_suspicious" in filtered_alerts:
    c3.metric("Known suspicious rate", f"{100 * filtered_alerts['is_suspicious'].mean():.1f}%")

risk_band_summary = load_optional_report("reports/risk_band_summary.csv")
if risk_band_summary is not None and "fraud_rate" in risk_band_summary.columns:
    st.subheader("Risk Band Summary")
    risk_display = risk_band_summary.copy()
    risk_display["fraud_rate"] = (
        risk_display["fraud_rate"] * 100
    ).round(2).astype(str) + "%"
    st.dataframe(risk_display, use_container_width=True)

alert_summary = load_optional_report("reports/rule_tuning_comparison.csv")
if alert_summary is not None and "fraud_rate" in alert_summary.columns:
    st.subheader("Rule Tuning Comparison")
    alert_display = alert_summary.copy()
    alert_display["fraud_rate"] = (
        alert_display["fraud_rate"] * 100
    ).round(2).astype(str) + "%"
    st.dataframe(alert_display, use_container_width=True)

st.subheader("Alert Queue Explorer")
st.write(
    f"Showing first {min(len(filtered_alerts), 1000):,} "
    f"of {len(filtered_alerts):,} alerts"
)

if "isFraud" in filtered_alerts.columns:
    filtered_alerts = filtered_alerts.rename(columns={"isFraud": "fraud_flag"})

st.dataframe(
    filtered_alerts.sort_values("risk_score", ascending=False).head(1000),
    use_container_width=True,
)

st.subheader("Risk Band Distribution")
st.bar_chart(filtered_alerts["risk_band"].value_counts().sort_index())

st.divider()
st.caption("Built with Python, Scikit-learn, Pandas, and Streamlit.")
