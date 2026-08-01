import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataPreprocessor:
    """Handles missing values, outliers, and normalization."""
    
    def __init__(self, df):
        self.df = df.copy()
        
    def handle_missing_values(self):
        """Impute missing values using median for numerical columns."""
        logging.info("Handling missing values...")
        num_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in num_cols:
            missing_count = self.df[col].isnull().sum()
            if missing_count > 0:
                median_val = self.df[col].median()
                self.df[col] = self.df[col].fillna(median_val)
                logging.info(f"Imputed {missing_count} missing values in {col} with median ({median_val}).")
        return self.df
        
    def detect_outliers(self, columns):
        """Cap outliers using IQR method."""
        logging.info("Detecting and capping outliers using IQR method...")
        for col in columns:
            if col in self.df.columns:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
                if len(outliers) > 0:
                    logging.info(f"Capping {len(outliers)} outliers in {col}.")
                    self.df[col] = np.clip(self.df[col], lower_bound, upper_bound)
        return self.df

if __name__ == "__main__":
    from etl import DataLoader
    df = DataLoader().load_raw_data()
    preprocessor = DataPreprocessor(df)
    clean_df = preprocessor.handle_missing_values()
    clean_df = preprocessor.detect_outliers(['produksi_padi', 'curah_hujan', 'suhu'])
    print(clean_df.head())
