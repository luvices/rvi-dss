import pandas as pd
import numpy as np
import logging
from sklearn.preprocessing import MinMaxScaler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FeatureEngineer:
    """Constructs composite indices for Regional Vulnerability Intelligence."""
    
    def __init__(self, df):
        self.df = df.copy()
        self.scaler = MinMaxScaler()
        
    def _normalize(self, col):
        """Helper to normalize a column between 0 and 1."""
        return self.scaler.fit_transform(self.df[[col]]).flatten()

    def create_environmental_risk_index(self):
        """
        Creates ERI based on rainfall anomalies and temperature extremes.
        High rainfall or extreme temperatures indicate higher risk.
        """
        logging.info("Creating Environmental Risk Index (ERI)...")
        norm_hujan = self._normalize('curah_hujan')
        norm_suhu = self._normalize('suhu')
        # Simple weighted sum (can be adjusted based on expert domain)
        self.df['env_risk_index'] = (norm_hujan * 0.6) + (norm_suhu * 0.4)
        return self.df
        
    def create_socioeconomic_vulnerability_index(self):
        """
        Creates SVI based on poverty and inverse of HDI (IPM).
        High poverty and low HDI = High Vulnerability.
        """
        logging.info("Creating Socio-Economic Vulnerability Index (SVI)...")
        norm_kemiskinan = self._normalize('kemiskinan')
        # Inverse IPM (Higher IPM = Lower Vulnerability)
        inv_ipm = 1 - self._normalize('ipm')
        self.df['socio_vuln_index'] = (norm_kemiskinan * 0.7) + (inv_ipm * 0.3)
        return self.df
        
    def create_health_sanitation_score(self):
        """
        Creates HSS based on clean water and proper sanitation.
        Lower values indicate higher vulnerability. We invert it for Risk.
        """
        logging.info("Creating Health & Sanitation Risk Score (HSS)...")
        norm_sanitasi = self._normalize('sanitasi')
        norm_air = self._normalize('air_bersih')
        # Inverse: lower sanitation/water means higher risk
        self.df['health_risk_score'] = 1 - ((norm_sanitasi * 0.5) + (norm_air * 0.5))
        return self.df
        
    def create_composite_rvi_score(self):
        """
        Creates the final Regional Vulnerability Intelligence (RVI) Score.
        This is a weighted combination of all sub-indices.
        This serves as our primary composite label/target for advanced policy DSS.
        """
        logging.info("Creating Composite RVI Score...")
        self.df['rvi_score'] = (
            (self.df['env_risk_index'] * 0.4) +
            (self.df['socio_vuln_index'] * 0.4) +
            (self.df['health_risk_score'] * 0.2)
        )
        return self.df
        
    def execute_all(self):
        self.create_environmental_risk_index()
        self.create_socioeconomic_vulnerability_index()
        self.create_health_sanitation_score()
        self.create_composite_rvi_score()
        logging.info("Feature engineering complete.")
        return self.df

if __name__ == "__main__":
    from etl import DataLoader
    from preprocessing import DataPreprocessor
    
    df = DataLoader().load_raw_data()
    clean_df = DataPreprocessor(df).handle_missing_values()
    fe = FeatureEngineer(clean_df)
    final_df = fe.execute_all()
    print(final_df[['kabupaten', 'rvi_score', 'env_risk_index', 'socio_vuln_index']].head())
