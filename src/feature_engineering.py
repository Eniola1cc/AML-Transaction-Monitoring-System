"""
Feature engineering utilities for the AML Transaction Monitoring System.

This module creates transaction-level features used by the rule-based
engine, machine learning model, and final risk scoring process.
"""

import pandas as pd


def add_balance_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create balance movement features.

    Args:
        df: Transaction DataFrame.

    Returns:
        DataFrame with balance-based features.
    """
    df = df.copy()

    df["balance_diff"] = (
        df["oldbalanceOrg"] - df["newbalanceOrig"] - df["amount"]
    ).abs()

    df["dest_balance_diff"] = (
        df["newbalanceDest"] - df["oldbalanceDest"] - df["amount"]
    ).abs()

    return df


def add_transaction_type_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create transaction type risk indicators.

    Args:
        df: Transaction DataFrame.

    Returns:
        DataFrame with high-risk transaction type indicator.
    """
    df = df.copy()

    high_risk_types = ["TRANSFER", "CASH_OUT"]
    df["is_high_risk_type"] = df["type"].isin(high_risk_types).astype(int)

    return df


def add_account_behaviour_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create simple account behaviour features.

    Args:
        df: Transaction DataFrame.

    Returns:
        DataFrame with origin account frequency and average amount features.
    """
    df = df.copy()

    df["origin_txn_count"] = df.groupby("nameOrig")["amount"].transform("count")
    df["origin_avg_amount"] = df.groupby("nameOrig")["amount"].transform("mean")
    df["amount_vs_origin_avg"] = df["amount"] / (df["origin_avg_amount"] + 1)

    return df


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all feature engineering steps.

    Args:
        df: Cleaned transaction DataFrame.

    Returns:
        Feature-enriched DataFrame.
    """
    df = add_balance_features(df)
    df = add_transaction_type_features(df)
    df = add_account_behaviour_features(df)

    return df
