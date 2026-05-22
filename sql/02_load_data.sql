-- Example SQLite import script
-- Run in sqlite shell from project root:
-- .mode csv
-- .import data/processed/accounts.csv accounts
-- .import data/processed/transactions.csv transactions

-- Basic quality checks
SELECT COUNT(*) AS account_rows FROM accounts;
SELECT COUNT(*) AS transaction_rows FROM transactions;
SELECT COUNT(*) AS fraud_rows FROM transactions WHERE isFraud = 1;
