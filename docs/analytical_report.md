# AML Transaction Monitoring System — Analytical Report

## 1) Business Problem
Financial crime investigation teams often face high alert volumes with limited analyst capacity. The core objective is to reduce low-value review effort and prioritise transactions with the highest likelihood of suspicious behaviour.

## 2) Dataset Overview
The project uses a simulated transaction dataset with key fields such as transaction type, amount, origin/destination accounts, account balances, and fraud labels. This enables controlled experimentation of AML workflow logic.

## 3) End-to-End Workflow
1. Data processing and quality checks.
2. Feature engineering for behavioural and transactional signals.
3. Rule-based suspicious-pattern detection.
4. Random Forest model training and evaluation.
5. Combined risk scoring and risk-band assignment.
6. Prioritised alert output and dashboard reporting.

## 4) SQL Processing Layer
A dedicated `sql/` layer now provides:
- Table creation scripts for accounts and transactions.
- Data loading and validation queries.
- Transaction-level summary aggregations.
- Account behaviour feature extraction.
- Suspicious pattern and prioritised queue candidate queries.

## 5) Feature Engineering
Engineered features include transaction frequency, high-risk transaction type counts, near-threshold transaction behaviour, and account-level behavioural baselines.

## 6) Rule-Based AML Detection
Rules capture common AML indicators:
- Structuring-like behaviour near reporting thresholds.
- Rapid transaction velocity.
- Geographic mismatches.
- Unusual transaction amounts relative to account baseline.

## 7) Machine Learning Model
A Random Forest classifier is used to estimate suspicious behaviour likelihood. Performance is tracked with accuracy, precision, recall, F1-score, and ROC-AUC.

## 8) Risk Scoring Method
The final risk score combines rule-based intensity and ML probability into a 0–100 scale. Transactions are segmented into `Low`, `Medium`, `High`, and `Critical` bands to support operational triage.

## 9) Scenario / Trade-Off Analysis
The project compares threshold settings to demonstrate the alert-volume versus fraud-capture trade-off. Stricter thresholds reduce workload but may lower detection coverage.

## 10) Dashboard Explanation
The Streamlit dashboard provides:
- AML KPI overview.
- Risk-band distribution.
- Alert queue summaries.
- Model metrics and top features.
- Rule-tuning comparison.
- Filterable alert explorer (when detailed queue file exists).

## 11) Business Impact
The system supports investigator productivity by surfacing high-risk alerts first and enabling evidence-based prioritisation decisions.

## 12) Limitations
- Dataset is simulated, not live bank data.
- No integrated case-management workflow.
- Model behaviour may differ in production environments with changing transaction patterns.

## 13) Future Improvements
- Integrate persistent SQL database workflow in production runtime.
- Add temporal velocity and graph/network analytics.
- Introduce model monitoring and drift detection.
- Extend to investigator case-routing and feedback loop.
