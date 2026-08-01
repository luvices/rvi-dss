import shap
import joblib
import logging
import pandas as pd
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ModelExplainer:
    """Uses SHAP (SHapley Additive exPlanations) to interpret the black-box model."""
    
    def __init__(self, model_path="models/best_model.pkl"):
        try:
            self.model = joblib.load(model_path)
            logging.info(f"Loaded model for explanation from {model_path}")
        except Exception as e:
            logging.error(f"Failed to load model: {e}")
            self.model = None
            
    def generate_shap_values(self, X):
        """Calculates SHAP values for a given feature set."""
        if self.model is None:
            return None
        
        logging.info("Calculating SHAP values (This might take a while)...")
        # TreeExplainer is highly optimized for tree-based models (RF, XGBoost, etc.)
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(X)
        return explainer, shap_values
        
    def summary_plot(self, shap_values, X, show=True):
        """Generates the SHAP summary plot."""
        shap.summary_plot(shap_values, X, show=show)

if __name__ == "__main__":
    from etl import DataLoader
    from preprocessing import DataPreprocessor
    from feature_engineering import FeatureEngineer
    
    # Quick test
    df = DataLoader().load_raw_data()
    clean_df = DataPreprocessor(df).handle_missing_values()
    final_df = FeatureEngineer(clean_df).execute_all()
    
    features = [c for c in final_df.columns if c not in ['kabupaten', 'tahun', 'rvi_score']]
    X = final_df[features]
    
    explainer = ModelExplainer()
    if explainer.model:
        exp, shap_vals = explainer.generate_shap_values(X)
        logging.info("SHAP computation complete.")
