import pandas as pd
import numpy as np
import os

def generate_research_data(output_path="data/raw/master_dataset.csv"):
    kabupaten_kota = [
        "Kabupaten Bogor", "Kabupaten Sukabumi", "Kabupaten Cianjur", "Kabupaten Bandung", 
        "Kabupaten Garut", "Kabupaten Tasikmalaya", "Kabupaten Ciamis", "Kabupaten Kuningan", 
        "Kabupaten Cirebon", "Kabupaten Majalengka", "Kabupaten Sumedang", "Kabupaten Indramayu", 
        "Kabupaten Subang", "Kabupaten Purwakarta", "Kabupaten Karawang", "Kabupaten Bekasi", 
        "Kabupaten Bandung Barat", "Kabupaten Pangandaran", "Kota Bogor", "Kota Sukabumi", 
        "Kota Bandung", "Kota Cirebon", "Kota Bekasi", "Kota Depok", "Kota Cimahi", 
        "Kota Tasikmalaya", "Kota Banjar"
    ]
    
    # 20 years of data (2004-2023) for robust ML testing
    tahun = list(range(2004, 2024))
    
    data = []
    np.random.seed(42)
    
    for kab in kabupaten_kota:
        base_produksi = np.random.uniform(50000, 1500000)
        base_hujan = np.random.uniform(1500, 3500)
        base_suhu = np.random.uniform(23.0, 28.0)
        base_ipm = np.random.uniform(65.0, 80.0)
        base_kemiskinan = np.random.uniform(4.0, 15.0)
        
        for t in tahun:
            produksi_padi = max(0, int(base_produksi * (1 + np.random.normal(0, 0.15))))
            curah_hujan = max(500, int(base_hujan * (1 + np.random.normal(0, 0.2))))
            suhu = round(base_suhu + np.random.normal(0, 0.6), 1)
            kelembaban = max(50, min(100, int(np.random.normal(80, 7))))
            
            # IPM tends to increase
            ipm = round(base_ipm + (t - 2004) * np.random.uniform(0.1, 0.4), 2)
            ipm = min(100, ipm)
            
            # Kemiskinan fluctuates but generally trends down
            kemiskinan = round(base_kemiskinan - (t - 2004) * np.random.uniform(0.0, 0.15) + np.random.normal(0, 0.8), 2)
            kemiskinan = max(0, kemiskinan)
            
            sanitasi = round(np.random.uniform(60.0, 95.0), 2)
            air_bersih = round(np.random.uniform(65.0, 98.0), 2)
            
            data.append([
                kab, t, produksi_padi, curah_hujan, suhu, kelembaban, 
                ipm, kemiskinan, sanitasi, air_bersih
            ])
            
    df = pd.DataFrame(data, columns=[
        "kabupaten", "tahun", "produksi_padi", "curah_hujan", 
        "suhu", "kelembaban", "ipm", "kemiskinan", "sanitasi", "air_bersih"
    ])
    
    # Introduce missing values to simulate real world
    for col in ["curah_hujan", "suhu", "kelembaban", "sanitasi"]:
        mask = np.random.rand(len(df)) < 0.05
        df.loc[mask, col] = np.nan
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated robust dataset with {len(df)} rows at {output_path}")

if __name__ == "__main__":
    generate_research_data()
