import pandas as pd
import numpy as np
import json
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

def process_and_export():
    print("Reading data...")
    df = pd.read_csv('master_dataset.csv')
    
    # 1. Cleaning Data
    for col in ['curah_hujan', 'suhu', 'kelembaban', 'sanitasi']:
        df[col] = df[col].fillna(df[col].median())
        
    # 2. Train Model to get Feature Importance
    features = ['curah_hujan', 'suhu', 'kelembaban', 'ipm', 'kemiskinan', 'sanitasi', 'air_bersih']
    target = 'produksi_padi'
    
    X = df[features]
    y = df[target]
    
    # Using all data for training just to get feature importance for dashboard purposes
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Calculate some metrics (overfitted since train=test, but it's for dummy display)
    y_pred = model.predict(X)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    r2 = r2_score(y, y_pred)
    
    feature_imp = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
    
    # 3. Prepare JSON Data
    # 3.1 Raw Data per year and region for charts
    regions = df['kabupaten'].unique().tolist()
    years = sorted(df['tahun'].unique().tolist())
    
    trend_data = {}
    for region in regions:
        region_df = df[df['kabupaten'] == region].sort_values('tahun')
        trend_data[region] = region_df['produksi_padi'].tolist()
        
    # 3.2 Metrics and Importance
    export_data = {
        "metrics": {
            "total_regions": len(regions),
            "total_records": len(df),
            "model_r2": round(r2, 4),
            "model_rmse": round(rmse, 2)
        },
        "feature_importance": {
            "labels": feature_imp.index.tolist(),
            "values": [round(val, 4) for val in feature_imp.values.tolist()]
        },
        "trends": {
            "years": years,
            "data": trend_data
        },
        "raw_data": df.to_dict(orient='records')
    }
    
    with open('dashboard_data.js', 'w') as f:
        f.write('const dashboardData = ')
        json.dump(export_data, f, indent=4)
        f.write(';')
        
    print("Successfully exported to dashboard_data.js")

if __name__ == "__main__":
    process_and_export()
