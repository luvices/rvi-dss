import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataLoader:
    """Extract, Transform, Load (ETL) pipeline for RVI project."""
    
    def __init__(self, raw_data_path="data/raw/master_dataset.csv"):
        self.raw_data_path = raw_data_path
        
    def load_raw_data(self):
        """Load raw dataset."""
        if not os.path.exists(self.raw_data_path):
            logging.error(f"Raw data file not found at {self.raw_data_path}")
            raise FileNotFoundError(f"Missing file: {self.raw_data_path}")
            
        logging.info(f"Loading raw data from {self.raw_data_path}")
        df = pd.read_csv(self.raw_data_path)
        logging.info(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns.")
        return df
    
    def save_processed_data(self, df, output_path="data/processed/cleaned_dataset.csv"):
        """Save processed dataframe to CSV."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        logging.info(f"Processed data saved to {output_path}")

if __name__ == "__main__":
    loader = DataLoader()
    df = loader.load_raw_data()
    print(df.head())
