# Regional Vulnerability Intelligence (RVI) - GEMASTIK National Finalist Project

## 🔍 Overview
RVI is a research-grade Decision Support System (DSS) designed to address the problem of regional food security and socio-economic vulnerability. Instead of a simple predictive machine learning model, RVI constructs composite indices, compares state-of-the-art algorithms (XGBoost, LightGBM, CatBoost), utilizes eXplainable AI (SHAP) to interpret black-box decisions, and simulates policy actions for actionable recommendations.

## 📁 Project Structure
- `data/` : Contains raw, processed, and external datasets.
- `notebooks/` : Jupyter notebooks for Research-Grade EDA, Feature Engineering, Modeling, and SHAP.
- `src/` : Modularized source code for ETL, preprocessing, models, and explainability.
- `dashboard/` : Modern HTML/CSS/JS frontend acting as the Decision Support System.
- `models/` : Saved trained models.
- `reports/` : Generated figures and final reports.

## 🚀 Research Workflow
1. **Problem Statement**: High vulnerability due to climate anomalies.
2. **Objective**: Build an XAI-based DSS for regional policy simulation.
3. **Methodology**: Data Fusion -> Composite Feature Engineering -> Auto-ML -> SHAP -> Policy Simulation.

## 🛠️ Installation
```bash
pip install -r requirements.txt
```
