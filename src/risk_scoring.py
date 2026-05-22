from __future__ import annotations

import pandas as pd

from src.rules import explain_flags


def assign_risk_score(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["risk_score"] = (
        0.55 * out["rule_score"] + 45 * out["ml_suspicious_prob"]
    ).clip(0, 100)
    out["alert_priority"] = (
        out["risk_score"].rank(method="first", ascending=False).astype(int)
    )
    out["explanation"] = out.apply(explain_flags, axis=1)

    out["risk_band"] = pd.cut(
        out["risk_score"],
        bins=[-1, 30, 60, 80, 100],
        labels=["Low", "Medium", "High", "Critical"],
    )
    return out.sort_values("risk_score", ascending=False)


def top_alert_capture(
    df: pd.DataFrame, label_col: str = "is_suspicious", top_pct: float = 0.15
) -> float:
    if label_col not in df.columns:
        return float("nan")
    n_top = max(1, int(len(df) * top_pct))
    top = df.nlargest(n_top, "risk_score")
    total_susp = df[label_col].sum()
    if total_susp == 0:
        return 0.0
    return float(top[label_col].sum() / total_susp)
