import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AML Transaction Monitoring Dashboard",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 AML Transaction Monitoring Dashboard")
st.write("Rule-based and machine-learning alert prioritisation system for suspicious transaction monitoring.")

@st.cache_data
def load_data():
    risk_band_summary = pd.read_csv("reports/risk_band_summary.csv")
    alert_summary = pd.read_csv("reports/alert_queue_summary.csv")
    model_metrics = pd.read_csv("reports/model_metrics.csv")
    feature_importance = pd.read_csv("reports/model_feature_importance.csv")
    rule_comparison = pd.read_csv("reports/rule_tuning_comparison.csv")
    business_metrics = pd.read_csv("reports/business_metrics.csv")
    alert_queue = pd.read_csv("reports/prioritised_alert_queue.csv")
    return risk_band_summary, alert_summary, model_metrics, feature_importance, rule_comparison, business_metrics, alert_queue

risk_band_summary, alert_summary, model_metrics, feature_importance, rule_comparison, business_metrics, alert_queue = load_data()

# KPIs
st.subheader("📌 Key AML Metrics")

total_transactions = int(business_metrics.loc[business_metrics["metric"] == "Total Transactions", "value"].values[0])
total_fraud = int(business_metrics.loc[business_metrics["metric"] == "Total Fraud Cases", "value"].values[0])
total_alerts = int(business_metrics.loc[business_metrics["metric"] == "Total Rule-Based Alerts", "value"].values[0])
critical_alerts = int(business_metrics.loc[business_metrics["metric"] == "Critical Risk Alerts", "value"].values[0])

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Transactions", f"{total_transactions:,}")
col2.metric("Fraud Cases", f"{total_fraud:,}")
col3.metric("Rule-Based Alerts", f"{total_alerts:,}")
col4.metric("Critical Alerts", f"{critical_alerts:,}")

st.divider()

# Risk band summary
st.subheader("⚠️ Risk Band Summary")
st.dataframe(risk_band_summary, width="stretch")

st.bar_chart(
    risk_band_summary.set_index("risk_band")["transactions"]
)

st.divider()

# Alert summary
st.subheader("🚩 Prioritised Alert Queue Summary")
st.dataframe(alert_summary, width="stretch")

st.bar_chart(
    alert_summary.set_index("risk_band")["fraud_cases"]
)

st.divider()

# Model performance
st.subheader("🤖 Machine Learning Model Performance")
st.dataframe(model_metrics, width="stretch")

metrics = model_metrics.iloc[0]

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Accuracy", f"{metrics['accuracy']:.2%}")
m2.metric("Precision", f"{metrics['precision']:.2%}")
m3.metric("Recall", f"{metrics['recall']:.2%}")
m4.metric("F1 Score", f"{metrics['f1_score']:.2%}")
m5.metric("ROC AUC", f"{metrics['roc_auc']:.4f}")

st.divider()

# Feature importance
st.subheader("📊 Top Model Features")

top_features = feature_importance.head(10)
st.dataframe(top_features, width="stretch")

st.bar_chart(
    top_features.set_index("feature")["importance"]
)

st.divider()

# Rule tuning
st.subheader("🧠 Rule Tuning Comparison")
st.write("This compares alert volume and fraud capture across rule thresholds.")
st.dataframe(rule_comparison, width="stretch")

st.divider()

# Alert explorer
st.subheader("🔎 Alert Queue Explorer")

risk_filter = st.selectbox(
    "Filter by Risk Band",
    ["All"] + sorted(alert_queue["risk_band"].unique().tolist())
)

filtered_alerts = alert_queue.copy()

if risk_filter != "All":
    filtered_alerts = filtered_alerts[filtered_alerts["risk_band"] == risk_filter]

st.write(f"Showing {len(filtered_alerts):,} alerts")

display_cols = [
    "step",
    "type",
    "amount",
    "nameOrig",
    "nameDest",
    "rule_score",
    "ml_risk_score",
    "final_risk_score",
    "risk_band",
    "isFraud"
]

st.dataframe(
    filtered_alerts[display_cols].head(1000),
    width="stretch"
)

st.caption("Note: The dashboard displays the first 1,000 filtered alerts for performance.")