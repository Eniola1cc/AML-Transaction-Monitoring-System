from __future__ import annotations

import numpy as np
import pandas as pd


def apply_rule_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Create interpretable AML rule flags and a rule risk score.

    Expected columns:
    transaction_id, account_id, timestamp, amount, country, home_country
    """
    out = df.copy()
    out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True)

    # Velocity: many tx in a short period
    out = out.sort_values(["account_id", "timestamp"])
    tx_per_hour = (
        out.set_index("timestamp")
        .groupby("account_id")["transaction_id"]
        .rolling("1h")
        .count()
        .reset_index(name="tx_count_1h")
    )
    out = out.merge(tx_per_hour, on=["account_id", "timestamp"], how="left")
    out["rapid_transactions_flag"] = (out["tx_count_1h"] >= 4).astype(int)

    # Structuring: repeated medium-size transactions below reporting threshold
    near_threshold = out["amount"].between(8_000, 9_999)
    out["near_threshold_tx"] = near_threshold.astype(int)
    structuring_window = (
        out.set_index("timestamp")
        .groupby("account_id")["near_threshold_tx"]
        .rolling("24h")
        .sum()
        .reset_index(name="near_threshold_24h")
    )
    out = out.merge(structuring_window, on=["account_id", "timestamp"], how="left")
    out["structuring_flag"] = (out["near_threshold_24h"] >= 3).astype(int)

    # Geographic anomaly
    out["geo_anomaly_flag"] = (out["country"] != out["home_country"]).astype(int)

    # Normalize amount anomaly vs account baseline
    acct_med = out.groupby("account_id")["amount"].transform("median")
    out["amount_anomaly_ratio"] = (out["amount"] / acct_med.replace(0, np.nan)).fillna(
        1.0
    )
    out["amount_anomaly_flag"] = (out["amount_anomaly_ratio"] >= 3.0).astype(int)

    out["rule_score"] = (
        30 * out["structuring_flag"]
        + 25 * out["rapid_transactions_flag"]
        + 20 * out["geo_anomaly_flag"]
        + 25 * out["amount_anomaly_flag"]
    )
    return out


def explain_flags(row: pd.Series) -> str:
    explanations = []
    if row.get("structuring_flag", 0) == 1:
        explanations.append("Structuring pattern detected")
    if row.get("rapid_transactions_flag", 0) == 1:
        explanations.append("Rapid transaction velocity")
    if row.get("geo_anomaly_flag", 0) == 1:
        explanations.append("Geographic anomaly")
    if row.get("amount_anomaly_flag", 0) == 1:
        explanations.append("Unusual amount vs account baseline")
    return "; ".join(explanations) if explanations else "No major rule triggers"
