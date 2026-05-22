"""
Data processing utilities for the AML Transaction Monitoring System.

This module contains reusable functions for loading transaction data,
cleaning columns, validating required fields, and preparing the dataset
for feature engineering and modelling.
"""

from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = [
    "step",
    "type",
    "amount",
    "nameOrig",
    "oldbalanceOrg",
    "newbalanceOrig",
    "nameDest",
    "oldbalanceDest",
    "newbalanceDest",
]


def load_transactions(file_path: str) -> pd.DataFrame:
    """
    Load transaction data from a CSV file.

    Args:
        file_path: Path to the raw transaction CSV file.

    Returns:
        A pandas DataFrame containing transaction records.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Transaction file not found: {file_path}")

    return pd.read_csv(path)


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the transaction dataset.

    This function standardises transaction type values, removes duplicate
    records, and ensures key numeric columns are numeric.

    Args:
        df: Raw transaction DataFrame.

    Returns:
        Cleaned transaction DataFrame.
    """
    df = df.copy()

    if "type" in df.columns:
        df["type"] = df["type"].astype(str).str.strip().str.upper()

    numeric_columns = [
        "amount",
        "oldbalanceOrg",
        "newbalanceOrig",
        "oldbalanceDest",
        "newbalanceDest",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df = df.drop_duplicates().reset_index(drop=True)

    return df


def validate_transactions(df: pd.DataFrame) -> None:
    """
    Validate that the dataset contains the required transaction columns.

    Args:
        df: Transaction DataFrame.

    Raises:
        ValueError: If required columns are missing.
    """
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def prepare_transactions(file_path: str) -> pd.DataFrame:
    """
    Load, validate, and clean transaction data.

    Args:
        file_path: Path to the transaction CSV file.

    Returns:
        Prepared transaction DataFrame.
    """
    df = load_transactions(file_path)
    validate_transactions(df)
    df = clean_transactions(df)

    return df
