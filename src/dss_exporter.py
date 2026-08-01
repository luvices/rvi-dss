import json
import logging
import pandas as pd
from etl import DataLoader
from preprocessing import DataPreprocessor
from feature_engineering import FeatureEngineer
from models import ModelTrainer
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def export_dss_data():
    logging.info("Preparing Decision Support System Data...")
    
    df = DataLoader("data/raw/master_dataset.csv").load_raw_data()
    clean_df = DataPreprocessor(df).handle_missing_values()
    final_df = FeatureEngineer(clean_df).execute_all()
    
    # Get latest year data
    latest_year = final_df['tahun'].max()
    current_df = final_df[final_df['tahun'] == latest_year].copy()
    
    # Sort by RVI score (Highest vulnerability first)
    top_vulnerable = current_df.sort_values(by='rvi_score', ascending=False).head(10)
    safest = current_df.sort_values(by='rvi_score', ascending=True).head(10)
    
    # Train Model (Mocking the pipeline for extraction)
    trainer = ModelTrainer(final_df)
    results = trainer.train_and_evaluate()
    
    # Generate mock policy recommendations based on sub-indices
    recs = []
    for _, row in top_vulnerable.iterrows():
        action = "Tingkatkan Subsidi Pertanian"
        if row['env_risk_index'] > 0.7:
            action = "Distribusi Bibit Tahan Iklim Ekstrem"
        elif row['socio_vuln_index'] > 0.7:
            action = "Perluasan Jaring Pengaman Sosial (Bansos)"
        elif row['health_risk_score'] > 0.7:
            action = "Perbaikan Infrastruktur Air & Sanitasi"
            
        recs.append({
            "kabupaten": row['kabupaten'],
            "rvi_score": round(row['rvi_score'], 3),
            "recommendation": action,
            "risk_level": "Tinggi" if row['rvi_score'] > 0.6 else "Menengah"
        })
        
    export_payload = {
        "metadata": {
            "latest_year": int(latest_year),
            "total_regions": len(current_df)
        },
        "top_vulnerable": top_vulnerable[['kabupaten', 'rvi_score', 'env_risk_index', 'socio_vuln_index', 'health_risk_score']].to_dict(orient='records'),
        "safest": safest[['kabupaten', 'rvi_score', 'env_risk_index', 'socio_vuln_index', 'health_risk_score']].to_dict(orient='records'),
        "recommendations": recs,
        "model_performance": results.to_dict(orient='records')
    }
    
    os.makedirs('dashboard', exist_ok=True)
    with open('dashboard/dss_data.js', 'w') as f:
        f.write("const dssData = ")
        json.dump(export_payload, f, indent=4)
        f.write(";")
        
    logging.info("DSS data exported successfully to dashboard/dss_data.js")

if __name__ == "__main__":
    export_dss_data()
