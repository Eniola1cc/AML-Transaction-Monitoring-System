from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="AML Transaction Monitoring Dashboard",
    page_icon="🚨",
    layout="wide",
)

st.title("🚨 AML Transaction Monitoring Dashboard")
st.write(
    "Rule-based and machine-learning alert prioritisation system "
    "for suspicious transaction monitoring."
)


REPORTS_DIR = Path("reports")

RISK_BAND_SUMMARY_PATH = REPORTS_DIR / "risk_band_summary.csv"
ALERT_SUMMARY_PATH = REPORTS_DIR / "alert_queue_summary.csv"
MODEL_METRICS_PATH = REPORTS_DIR / "model_metrics.csv"
FEATURE_IMPORTANCE_PATH = REPORTS_DIR / "model_feature_importance.csv"
RULE_COMPARISON_PATH = REPORTS_DIR / "rule_tuning_comparison.csv"
BUSINESS_METRICS_PATH = REPORTS_DIR / "business_metrics.csv"
ALERT_QUEUE_PATH = REPORTS_DIR / "prioritised_alert_queue.csv"


def load_csv(file_path: Path, required: bool = True) -> pd.DataFrame:
    """Load a CSV file safely."""
    if not file_path.exists():
        if required:
            st.error(f"Required file not found: {file_path}")
            st.stop()

        st.warning(f"Optional file not found: {file_path}")
        return pd.DataFrame()

    try:
        return pd.read_csv(file_path)
    except Exception as error:
        st.error(f"Unable to read {file_path}: {error}")
        st.stop()


def get_metric_value(
    business_metrics: pd.DataFrame,
    metric_name: str,
    default_value: int = 0,
) -> int:
    """Extract a metric value from the business metrics file."""
    if business_metrics.empty:
        return default_value

    if "metric" not in business_metrics.columns or "value" not in business_metrics.columns:
        return default_value

    matched_rows = business_metrics.loc[
        business_metrics["metric"] == metric_name,
        "value",
    ]

    if matched_rows.empty:
        return default_value

    return int(float(matched_rows.iloc[0]))


def show_dataframe(title: str, dataframe: pd.DataFrame) -> None:
    """Display a dataframe safely."""
    st.subheader(title)

    if dataframe.empty:
        st.info("No data available for this section yet.")
    else:
        st.dataframe(dataframe, width="stretch")


@st.cache_data
def load_data():
    risk_band_summary = load_csv(RISK_BAND_SUMMARY_PATH)
    alert_summary = load_csv(ALERT_SUMMARY_PATH)
    model_metrics = load_csv(MODEL_METRICS_PATH)
    feature_importance = load_csv(FEATURE_IMPORTANCE_PATH)
    rule_comparison = load_csv(RULE_COMPARISON_PATH)
    business_metrics = load_csv(BUSINESS_METRICS_PATH)

    # This file may be large or may not exist yet, so it is optional.
    alert_queue = load_csv(ALERT_QUEUE_PATH, required=False)

    return (
        risk_band_summary,
        alert_summary,
        model_metrics,
        feature_importance,
        rule_comparison,
        business_metrics,
        alert_queue,
    )


(
    risk_band_summary,
    alert_summary,
    model_metrics,
    feature_importance,
    rule_comparison,
    business_metrics,
    alert_queue,
) = load_data()


st.subheader("📌 Key AML Metrics")

total_transactions = get_metric_value(business_metrics, "Total Transactions")
total_fraud = get_metric_value(business_metrics, "Total Fraud Cases")
total_alerts = get_metric_value(business_metrics, "Total Rule-Based Alerts")
critical_alerts = get_metric_value(business_metrics, "Critical Risk Alerts")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Transactions", f"{total_transactions:,}")
col2.metric("Fraud Cases", f"{total_fraud:,}")
col3.metric("Rule-Based Alerts", f"{total_alerts:,}")
col4.metric("Critical Alerts", f"{critical_alerts:,}")

st.divider()


show_dataframe("⚠️ Risk Band Summary", risk_band_summary)

if not risk_band_summary.empty and {"risk_band", "transactions"}.issubset(
    risk_band_summary.columns
):
    st.bar_chart(risk_band_summary.set_index("risk_band")["transactions"])

st.divider()


show_dataframe("🚩 Prioritised Alert Queue Summary", alert_summary)

if not alert_summary.empty and {"risk_band", "fraud_cases"}.issubset(
    alert_summary.columns
):
    st.bar_chart(alert_summary.set_index("risk_band")["fraud_cases"])

st.divider()


st.subheader("🤖 Machine Learning Model Performance")

if model_metrics.empty:
    st.info("No model metrics available yet.")
else:
    st.dataframe(model_metrics, width="stretch")

    required_metric_columns = {
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "roc_auc",
    }

    if required_metric_columns.issubset(model_metrics.columns):
        metrics = model_metrics.iloc[0]

        m1, m2, m3, m4, m5 = st.columns(5)

        m1.metric("Accuracy", f"{float(metrics['accuracy']):.2%}")
        m2.metric("Precision", f"{float(metrics['precision']):.2%}")
        m3.metric("Recall", f"{float(metrics['recall']):.2%}")
        m4.metric("F1 Score", f"{float(metrics['f1_score']):.2%}")
        m5.metric("ROC AUC", f"{float(metrics['roc_auc']):.4f}")
    else:
        st.warning(
            "Model metrics file is missing one or more required columns: "
            "accuracy, precision, recall, f1_score, roc_auc."
        )

st.divider()


st.subheader("📊 Top Model Features")

if feature_importance.empty:
    st.info("No feature importance data available yet.")
else:
    top_features = feature_importance.head(10)
    st.dataframe(top_features, width="stretch")

    if {"feature", "importance"}.issubset(top_features.columns):
        st.bar_chart(top_features.set_index("feature")["importance"])
    else:
        st.warning(
            "Feature importance file must contain 'feature' and 'importance' columns."
        )

st.divider()


st.subheader("🧠 Rule Tuning Comparison")
st.write("This compares alert volume and fraud capture across rule thresholds.")

if rule_comparison.empty:
    st.info("No rule tuning comparison data available yet.")
else:
    st.dataframe(rule_comparison, width="stretch")

st.divider()


st.subheader("🔎 Alert Queue Explorer")

if alert_queue.empty:
    st.info(
        "No detailed alert queue file is available yet. "
        "Add reports/prioritised_alert_queue.csv to enable explorer mode."
    )
else:
    if "risk_band" not in alert_queue.columns:
        st.warning("The alert queue file does not contain a 'risk_band' column.")
    else:
        risk_filter = st.selectbox(
            "Filter by Risk Band",
            ["All"] + sorted(alert_queue["risk_band"].dropna().unique().tolist()),
        )

        filtered_alerts = alert_queue.copy()

        if risk_filter != "All":
            filtered_alerts = filtered_alerts[
                filtered_alerts["risk_band"] == risk_filter
            ]

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
            "isFraud",
        ]

        available_display_cols = [
            column for column in display_cols if column in filtered_alerts.columns
        ]

        if not available_display_cols:
            st.warning("No expected alert queue columns are available to display.")
        else:
            st.dataframe(
                filtered_alerts[available_display_cols].head(1000),
                width="stretch",
            )

            st.caption(
                "Note: The dashboard displays the first 1,000 filtered alerts "
                "for performance."
            )
