# AML Transaction Monitoring System

A rule-based and machine-learning AML transaction monitoring system for detecting suspicious financial transactions, scoring risk, and prioritising alerts for investigation.

## Business Context

Financial institutions process large volumes of transactions every day. Traditional AML monitoring systems often generate many false-positive alerts, making it difficult for investigators to focus on the most suspicious activity.

This project simulates an AML alert prioritisation workflow. It combines transaction rules, engineered behavioural features, machine learning, risk scoring, and a Streamlit dashboard to help analysts focus on the highest-risk transactions first.

## Project Objective

The objective of this project is to build an end-to-end AML transaction monitoring system that can:

- Detect suspicious transaction patterns
- Generate rule-based alerts
- Train a machine learning model for fraud detection
- Produce a final risk score
- Categorise transactions into risk bands
- Prioritise alerts for investigation
- Compare rule thresholds and alert trade-offs
- Present results in an interactive Streamlit dashboard

## Key Features

- SQL/Python-style transaction processing
- Feature engineering for transaction behaviour
- Rule-based AML detection
- Machine learning model training
- Risk scoring and alert prioritisation
- Risk band segmentation
- Rule tuning and threshold comparison
- Model performance reporting
- Streamlit dashboard for investigation workflow

## Dataset Summary

The project uses a transaction dataset containing:

- Transaction step/time
- Transaction type
- Transaction amount
- Origin account
- Destination account
- Origin and destination balances
- Fraud label

The dashboard currently analyses:

- Total transactions: 6,362,620
- Fraud cases: 8,213
- Rule-based alerts: 1,779,421
- Critical alerts: 8,162

## Project Structure

```text
AML-Transaction-Monitoring-System/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   └── analytical_report.md
│
├── models/
│   └── random_forest_aml_model.pkl
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_rule_based_detection.ipynb
│   ├── 04_model_training.ipynb
│   └── 05_risk_scoring.ipynb
│
├── reports/
│   ├── alert_queue_summary.csv
│   ├── business_metrics.csv
│   ├── model_feature_importance.csv
│   ├── model_metrics.csv
│   ├── risk_band_summary.csv
│   └── rule_tuning_comparison.csv
│
├── src/
│   ├── data_processing.py
│   ├── feature_engineering.py
│   ├── model.py
│   ├── risk_scoring.py
│   └── rules.py
│
├── requirements.txt
└── README.md

Methodology
1. Data Processing
The raw transaction data is loaded, inspected, cleaned, and prepared for analysis. The processing stage checks data structure, missing values, transaction types, and fraud distribution.
2. Feature Engineering
New transaction features are created to support AML detection and model training. These include:
Balance movement difference
High-risk transaction type indicator
Average amount sent
Total amount sent
Account behaviour features
Rule-based alert indicators
3. Rule-Based Detection
The rule engine flags suspicious activity based on AML-style indicators such as:
High-risk transaction types
Unusual balance movement
Suspicious transfer and cash-out behaviour
Rule score thresholds
4. Machine Learning
A Random Forest classification model is trained to identify suspicious and fraudulent transaction patterns. Model performance is evaluated using accuracy, precision, recall, F1 score, and ROC AUC.
5. Risk Scoring
The system combines rule-based signals and machine learning output to create a final risk score. Transactions are grouped into:
Critical
High
Medium
Low
This allows investigators to review the most suspicious alerts first.
6. Scenario and Trade-Off Analysis
The project compares different rule thresholds to show the trade-off between alert volume and fraud capture.
Example:
ScenarioAlerts CreatedFraud CapturedAlert Fraud Rate
Original Rules: score >= 21,779,4218,1860.0046
Strict Rules: score >= 3606,3855,2970.0087
This shows that stricter rules reduce alert volume but may also reduce fraud capture.
Model Performance
ModelAccuracyPrecisionRecallF1 ScoreROC AUC
Random Forest99.74%97.60%99.03%98.31%0.9996
Key Business Insights
The Critical risk band contains the highest concentration of fraud.
Prioritising Critical and High alerts can reduce investigation workload.
Rule threshold tuning can significantly reduce alert volume.
Machine learning improves prioritisation by ranking alerts based on risk.
The dashboard gives investigators a practical alert queue for review.
Dashboard
The Streamlit dashboard includes:
Key AML metrics
Risk band summary
Prioritised alert queue
Model performance metrics
Top model features
Rule tuning comparison
Alert queue explorer
To run the dashboard:
streamlit run dashboard/app.py
Installation
Clone the repository:
git clone https://github.com/Eniola1cc/AML-Transaction-Monitoring-System.git
cd AML-Transaction-Monitoring-System
Create and activate a virtual environment:
python3 -m venv .venv
source .venv/bin/activate
Install requirements:
pip install -r requirements.txt
Run the dashboard:
streamlit run dashboard/app.py
Deliverables
Detection system
Risk scoring model
Prioritised alert queue
Streamlit dashboard
Analytical report
GitHub portfolio project
Business Recommendation
AML investigation teams should prioritise Critical and High risk alerts first. Medium alerts can be reviewed when analyst capacity allows, while Low alerts can be monitored with less manual review.
This approach helps reduce false-positive workload while keeping focus on the transactions most likely to represent financial crime risk.
Future Improvements
Add SQL database integration
Add investigator case management workflow
Add time-based velocity features
Add account-level network analysis
Add model drift monitoring
Add Power BI version of the dashboard
Deploy the dashboard online
