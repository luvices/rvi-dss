import pandas as pd
import numpy as np
import logging
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ModelEvaluator:
    """Evaluates ML models using standard research metrics."""
    
    @staticmethod
    def evaluate(y_true, y_pred, model_name="Model"):
        """Calculate and return evaluation metrics."""
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        
        logging.info(f"[{model_name}] RMSE: {rmse:.4f}, MAE: {mae:.4f}, R2: {r2:.4f}")
        return {
            "Model": model_name,
            "RMSE": rmse,
            "MAE": mae,
            "R2": r2
        }

    @staticmethod
    def compare_models(results_list):
        """Returns a formatted DataFrame comparing multiple models."""
        df_results = pd.DataFrame(results_list)
        df_results = df_results.sort_values(by="RMSE", ascending=True).reset_index(drop=True)
        return df_results
