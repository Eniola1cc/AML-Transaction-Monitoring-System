# Transaction Monitoring & AML Alert Prioritisation System

Financial institutions often generate too many false-positive AML alerts. This project combines **rule-based monitoring** and **machine learning** to produce a **single risk score** and ranked alert queue so investigators can focus on the highest-impact cases first.

## Current architecture

1. **Rule-based detection** (`src/rules.py`)
   - Structuring (repeated near-threshold transfers)
   - Rapid transactions (high 1-hour velocity)
   - Geographic anomalies (country mismatch)
   - Amount anomaly vs account baseline
2. **ML scoring** (`src/model.py`)
   - Isolation Forest for unsupervised anomalies
   - Optional RandomForest classifier when labels are available
3. **Risk scoring + prioritisation** (`src/risk_scoring.py`)
   - Blended risk score (0-100)
   - Alert ranking and risk bands
   - Explainable reason text for investigation workflow
4. **Dashboard** (`dashboard/app.py`)
   - Alert queue explorer with risk/country filters
   - KPI cards and risk-band distribution

---

## What will make this project better (high-impact roadmap)

### 1) Improve business-value metrics (most important)
- Track **capture@k** (e.g., suspicious cases captured in top 10/15/20% alerts).
- Add **investigator capacity simulation**: if analysts can review only N alerts/day, what % suspicious cases are captured?
- Quantify **false-positive reduction** vs baseline rule engine.

### 2) Add scenario + trade-off analysis
- Build threshold comparison table for low/medium/high risk cutoffs.
- Report precision, recall, false-positive rate, and alert volume at each threshold.
- Add policy recommendations: conservative mode (higher recall) vs lean mode (lower workload).

### 3) Strengthen pattern explainability
- For structuring: show recent transfers timeline and cumulative 24h amount.
- For velocity: show burst windows and peer percentile.
- For geo anomalies: include prior country history of account to distinguish travel vs unusual behavior.

### 4) Improve production readiness
- Move notebook logic into reproducible pipeline scripts (`data_processing.py`, `feature_engineering.py`).
- Add data quality checks (missing timestamps, negative amounts, duplicate transaction IDs).
- Add model drift monitoring (feature drift + alert-rate drift by week).

### 5) Upgrade dashboard for operations
- Add queue SLA views: overdue high-risk alerts, average time-to-review.
- Add investigator drill-down page per account with event history.
- Add model/rule explanation panel for each alert.

### 6) Portfolio polish
- Include an architecture diagram and end-to-end workflow image.
- Add sample case studies (“why this alert is high priority”).
- Publish a concise analytical report with business recommendations and next steps.

---

## Quick start

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

## Suggested final deliverables

- Detection system (rules + ML)
- Risk scoring model and prioritised alert queue
- Dashboard (Streamlit/Power BI)
- Business trade-off report
- GitHub portfolio with reproducible pipeline
