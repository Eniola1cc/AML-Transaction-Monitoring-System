-- Suspicious patterns and prioritised queue candidate query
WITH enriched AS (
    SELECT
        t.*,
        CASE WHEN t.amount BETWEEN 8000 AND 9999 THEN 1 ELSE 0 END AS structuring_hint,
        CASE WHEN t.type IN ('TRANSFER', 'CASH_OUT') THEN 1 ELSE 0 END AS high_risk_type_hint,
        CASE WHEN t.country <> a.home_country THEN 1 ELSE 0 END AS geo_mismatch_hint,
        (CASE WHEN t.amount BETWEEN 8000 AND 9999 THEN 30 ELSE 0 END
          + CASE WHEN t.type IN ('TRANSFER', 'CASH_OUT') THEN 25 ELSE 0 END
          + CASE WHEN t.country <> a.home_country THEN 20 ELSE 0 END
        ) AS rule_score
    FROM transactions t
    LEFT JOIN accounts a
      ON t.nameOrig = a.account_id
)
SELECT
    transaction_id,
    timestamp,
    nameOrig,
    nameDest,
    type,
    amount,
    isFraud,
    structuring_hint,
    high_risk_type_hint,
    geo_mismatch_hint,
    rule_score
FROM enriched
WHERE rule_score >= 45
ORDER BY rule_score DESC, amount DESC
LIMIT 500;
