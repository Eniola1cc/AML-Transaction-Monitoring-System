# Analytical Report: AML Transaction Monitoring System

## 1. Business Problem

Financial institutions process large volumes of transactions daily. Traditional AML monitoring systems can generate high volumes of alerts, many of which may be false positives. This creates workload pressure for compliance and investigation teams.

This project demonstrates how rule-based detection, machine learning, and risk scoring can be used to prioritise suspicious transactions for analyst review.

## 2. Project Workflow

The project follows this flow:

Raw transaction data → SQL processing → Python feature engineering → rule-based detection → machine learning model → risk scoring → risk bands → Streamlit dashboard.

## 3. Data Processing

The dataset contains transaction type, amount, origin and destination accounts, origin and destination balances, and fraud labels. The data was prepared for modelling and alert scoring.

## 4. Feature Engineering

Features were created to capture transaction behaviour, including high-risk transaction type indicators, balance movement differences, transaction amount patterns, and account-level behavioural signals.

## 5. Rule-Based Detection

AML-style rules were used to flag suspicious activity such as high-risk transaction types, unusual balance movements, and suspicious transfer or cash-out behaviour.

## 6. Machine Learning

A Random Forest model was trained to classify suspicious/fraudulent transactions. Performance was evaluated using accuracy, precision, recall, F1-score, and ROC-AUC.

## 7. Risk Scoring

The project converts model and rule outputs into a final risk score and groups transactions into Critical, High, Medium, and Low risk bands.

## 8. Business Impact

The system helps investigators focus on Critical and High-risk alerts first, reducing manual review pressure and improving alert prioritisation.

## 9. Limitations

The dataset is simulated and does not represent live bank data. In production, thresholds would need validation by AML analysts, model monitoring, and periodic recalibration.

## 10. Future Improvements

Future work could include case management workflow, Power BI reporting, automated SQL execution, model drift monitoring, and investigator feedback loops.
