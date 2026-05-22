-- Create AML transaction monitoring tables in SQLite
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS accounts;

CREATE TABLE accounts (
    account_id TEXT PRIMARY KEY,
    home_country TEXT NOT NULL,
    account_type TEXT,
    opened_date TEXT
);

CREATE TABLE transactions (
    transaction_id TEXT PRIMARY KEY,
    step INTEGER,
    timestamp TEXT,
    type TEXT,
    amount REAL,
    nameOrig TEXT,
    oldbalanceOrg REAL,
    newbalanceOrig REAL,
    nameDest TEXT,
    oldbalanceDest REAL,
    newbalanceDest REAL,
    country TEXT,
    isFraud INTEGER DEFAULT 0,
    FOREIGN KEY (nameOrig) REFERENCES accounts(account_id)
);

CREATE INDEX idx_transactions_origin ON transactions(nameOrig);
CREATE INDEX idx_transactions_dest ON transactions(nameDest);
CREATE INDEX idx_transactions_ts ON transactions(timestamp);
CREATE INDEX idx_transactions_type ON transactions(type);
