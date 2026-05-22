-- AML transaction summary metrics
SELECT
    COUNT(*) AS total_transactions,
    SUM(CASE WHEN isFraud = 1 THEN 1 ELSE 0 END) AS fraud_transactions,
    ROUND(100.0 * SUM(CASE WHEN isFraud = 1 THEN 1 ELSE 0 END) / COUNT(*), 4) AS fraud_rate_pct,
    ROUND(AVG(amount), 2) AS avg_amount
FROM transactions;

SELECT
    type,
    COUNT(*) AS tx_count,
    ROUND(SUM(amount), 2) AS total_amount,
    SUM(CASE WHEN isFraud = 1 THEN 1 ELSE 0 END) AS fraud_count
FROM transactions
GROUP BY type
ORDER BY tx_count DESC;
