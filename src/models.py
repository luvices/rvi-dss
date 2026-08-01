import logging
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from evaluation import ModelEvaluator
import joblib
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ModelTrainer:
    """Trains and compares multiple ML algorithms for RVI Prediction."""
    
    def __init__(self, df, target_col='rvi_score'):
        self.df = df
        self.target_col = target_col
        # Features exclude non-numeric or target columns
        self.features = [c for c in df.columns if c not in ['kabupaten', 'tahun', 'rvi_score']]
        
        self.models = {
            "Linear Regression": LinearRegression(),
            "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
            "Extra Trees": ExtraTreesRegressor(n_estimators=100, random_state=42),
            "XGBoost": XGBRegressor(n_estimators=100, random_state=42, objective='reg:squarederror'),
            "LightGBM": LGBMRegressor(n_estimators=100, random_state=42, verbose=-1),
            "CatBoost": CatBoostRegressor(iterations=100, random_state=42, verbose=0)
        }
        self.best_model = None
        self.best_model_name = None
        
    def train_and_evaluate(self):
        """Train all models, evaluate, and pick the best one."""
        X = self.df[self.features]
        y = self.df[self.target_col]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        results = []
        for name, model in self.models.items():
            logging.info(f"Training {name}...")
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            eval_result = ModelEvaluator.evaluate(y_test, y_pred, model_name=name)
            results.append(eval_result)
            
        comparison_df = ModelEvaluator.compare_models(results)
        logging.info("\n=== Model Comparison ===")
        print(comparison_df.to_string(index=False))
        
        self.best_model_name = comparison_df.iloc[0]['Model']
        self.best_model = self.models[self.best_model_name]
        
        logging.info(f"Best Model selected: {self.best_model_name}")
        return comparison_df
        
    def save_best_model(self, path="models/best_model.pkl"):
        """Saves the best performing model."""
        if self.best_model:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            joblib.dump(self.best_model, path)
            logging.info(f"Best model saved to {path}")
        else:
            logging.error("No model trained yet!")

if __name__ == "__main__":
    from etl import DataLoader
    from preprocessing import DataPreprocessor
    from feature_engineering import FeatureEngineer
    
    df = DataLoader().load_raw_data()
    clean_df = DataPreprocessor(df).handle_missing_values()
    final_df = FeatureEngineer(clean_df).execute_all()
    
    trainer = ModelTrainer(final_df)
    trainer.train_and_evaluate()
    trainer.save_best_model()
