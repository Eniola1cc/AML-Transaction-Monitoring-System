from __future__ import annotations

from typing import Iterable, Optional

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier

FEATURES = [
    "amount",
    "tx_count_1h",
    "near_threshold_24h",
    "amount_anomaly_ratio",
    "rule_score",
]


def train_isolation_forest(
    df: pd.DataFrame, contamination: float = 0.03
) -> IsolationForest:
    model = IsolationForest(
        n_estimators=200,
        contamination=contamination,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(df[FEATURES])
    return model


def train_classifier(
    df: pd.DataFrame, label_col: str = "is_suspicious"
) -> Optional[RandomForestClassifier]:
    if label_col not in df.columns:
        return None
    clf = RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        min_samples_leaf=3,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    clf.fit(df[FEATURES], df[label_col])
    return clf


def score_models(
    df: pd.DataFrame, iso_model: IsolationForest, clf: Optional[RandomForestClassifier]
) -> pd.DataFrame:
    out = df.copy()
    out["anomaly_score"] = -iso_model.decision_function(out[FEATURES])
    if clf is None:
        out["ml_suspicious_prob"] = (
            out["anomaly_score"] - out["anomaly_score"].min()
        ) / (out["anomaly_score"].max() - out["anomaly_score"].min() + 1e-8)
    else:
        out["ml_suspicious_prob"] = clf.predict_proba(out[FEATURES])[:, 1]
    return out
