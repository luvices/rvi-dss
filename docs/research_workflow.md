# RVI - Research Workflow & Methodology

> [!IMPORTANT]
> This document outlines the rigorous methodology used to construct the Regional Vulnerability Intelligence (RVI) platform. It is designed to withstand scrutiny from academic judges and government policymakers.

## 1. Problem Statement
Indonesia faces critical challenges in climate change adaptation and regional food security. Existing vulnerability assessments often rely on fragmented data and static models. The problem is a lack of an **actionable, explainable, and multi-dimensional vulnerability intelligence system** at the regency/city level.

## 2. Dataset Architecture
We utilize a data fusion approach, combining:
- **Agro-Climate Data**: Rice production, temperature anomalies, rainfall (simulated from BPS proxy).
- **Socio-Economic Data**: Poverty rates, Human Development Index (IPM).
- **Sanitation Data**: Clean water access and sanitation scores.

## 3. Composite Feature Engineering
Instead of using raw variables directly for prediction (which lacks depth), we engineered three foundational composite indices:
- `env_risk_index`: A weighted combination of rainfall anomalies and temperature extremes.
- `socio_vuln_index`: Synthesizing poverty levels and the inverse of HDI.
- `health_risk_score`: Aggregating sanitation and clean water access.

These indices are combined into the **Composite RVI Score (0.0 to 1.0)**. 
*Higher RVI Score = Higher Vulnerability & Urgency for Policy Intervention.*

## 4. Auto-ML Model Selection
To avoid "algorithm bias", we evaluated multiple state-of-the-art models:
- Linear Regression
- Random Forest
- Extra Trees
- XGBoost
- LightGBM
- CatBoost

**Evaluation Metrics**: RMSE, MAE, R-Squared ($R^2$). 
The best model is programmatically selected and serialized for the Decision Support System (DSS).

## 5. Explainable AI (XAI) via SHAP
Black-box models are unacceptable for public policy. We implement **SHAP (SHapley Additive exPlanations)** to interpret model predictions. 
- *Global Interpretability*: Understanding which composite index drives national vulnerability.
- *Local Interpretability*: Understanding why a specific regency (e.g., Ciamis) is highly vulnerable, allowing for targeted recommendations.

## 6. Decision Support System (DSS)
The raw predictions are exported to a web-based DSS Dashboard.
The dashboard transforms mathematical scores into **Policy Actions**, bridging the gap between Data Science and Public Administration.
