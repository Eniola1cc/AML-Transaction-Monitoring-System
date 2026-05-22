-- Account-level behavioural features for downstream Python modelling
WITH account_tx AS (
    SELECT
        nameOrig AS account_id,
        COUNT(*) AS tx_count,
        SUM(amount) AS total_sent,
        AVG(amount) AS avg_amount_sent,
        SUM(CASE WHEN type IN ('TRANSFER', 'CASH_OUT') THEN 1 ELSE 0 END) AS high_risk_type_count,
        SUM(CASE WHEN amount BETWEEN 8000 AND 9999 THEN 1 ELSE 0 END) AS near_threshold_count,
        SUM(CASE WHEN isFraud = 1 THEN 1 ELSE 0 END) AS fraud_count
    FROM transactions
    GROUP BY nameOrig
)
SELECT
    a.account_id,
    a.home_country,
    atx.tx_count,
    ROUND(atx.total_sent, 2) AS total_sent,
    ROUND(atx.avg_amount_sent, 2) AS avg_amount_sent,
    atx.high_risk_type_count,
    atx.near_threshold_count,
    atx.fraud_count,
    ROUND(1.0 * atx.fraud_count / NULLIF(atx.tx_count, 0), 6) AS fraud_ratio
FROM accounts a
JOIN account_tx atx
    ON a.account_id = atx.account_id
ORDER BY fraud_ratio DESC, atx.tx_count DESC;
