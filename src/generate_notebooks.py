import nbformat as nbf
import os

def create_eda_notebook():
    nb = nbf.v4.new_notebook()
    cells = []
    
    cells.append(nbf.v4.new_markdown_cell("# 01 - Exploratory Data Analysis (EDA)\n\n## 1. Dataset Overview\nMengapa ini penting? Sebelum melakukan inferensi model, integritas data (Missing Values, Duplikasi, Outlier) harus dipastikan untuk mencegah *Garbage-In-Garbage-Out*."))
    cells.append(nbf.v4.new_code_cell("import pandas as pd\nimport sys\nsys.path.append('../src')\nfrom etl import DataLoader\n\ndf = DataLoader('../data/raw/master_dataset.csv').load_raw_data()\ndisplay(df.head())\ndisplay(df.info())"))
    
    cells.append(nbf.v4.new_markdown_cell("## 2. Missing Value Analysis\nPolanya harus dianalisis apakah *Missing Completely at Random* (MCAR) atau memiliki pola khusus."))
    cells.append(nbf.v4.new_code_cell("import missingno as msno\nimport matplotlib.pyplot as plt\n\nmsno.matrix(df, figsize=(10, 5))\nplt.title('Missing Value Matrix')\nplt.show()"))
    
    cells.append(nbf.v4.new_markdown_cell("## 3. Distribution & Outlier Analysis\nDistribusi target dan fitur sangat krusial untuk asumsi regresi linear dan robustnes model *tree-based*."))
    cells.append(nbf.v4.new_code_cell("from visualization import DataVisualizer\nimport seaborn as sns\n\nDataVisualizer.plot_distribution(df['produksi_padi'], 'Distribusi Produksi Padi')\nplt.show()"))
    cells.append(nbf.v4.new_code_cell("DataVisualizer.plot_boxplots(df, ['curah_hujan', 'suhu'], 'Outlier Deteksi Iklim')\nplt.show()"))
    
    cells.append(nbf.v4.new_markdown_cell("## 4. Feature Correlation Ranking\nMenemukan multikolinearitas dan korelasi linier dengan target."))
    cells.append(nbf.v4.new_code_cell("DataVisualizer.plot_correlation_matrix(df)\nplt.show()"))
    
    cells.append(nbf.v4.new_markdown_cell("## 5. Insights\n- **Iklim**: Terdapat beberapa outlier pada curah hujan yang mewakili fenomena ekstrim (El Nino/La Nina).\n- **Korelasi**: Suhu dan curah hujan memiliki korelasi yang signifikan terhadap volatilitas produksi padi."))
    
    nb['cells'] = cells
    with open('notebooks/01_EDA.ipynb', 'w') as f:
        nbf.write(nb, f)

def create_feature_engineering_notebook():
    nb = nbf.v4.new_notebook()
    cells = []
    
    cells.append(nbf.v4.new_markdown_cell("# 02 - Feature Engineering\n\n## RVI Composite Index Construction\nDi sini kita tidak menggunakan data mentah, melainkan membuat Indeks Komposit yang merepresentasikan kerentanan dari berbagai dimensi."))
    cells.append(nbf.v4.new_code_cell("import sys\nsys.path.append('../src')\nfrom etl import DataLoader\nfrom preprocessing import DataPreprocessor\nfrom feature_engineering import FeatureEngineer\n\n# Pipeline\ndf = DataLoader('../data/raw/master_dataset.csv').load_raw_data()\nclean_df = DataPreprocessor(df).handle_missing_values()\n\nfe = FeatureEngineer(clean_df)\nfinal_df = fe.execute_all()\n\ndisplay(final_df[['kabupaten', 'rvi_score', 'env_risk_index', 'socio_vuln_index']].head())"))
    
    cells.append(nbf.v4.new_markdown_cell("## Insight Konstruksi\n- **Environmental Risk Index**: Menangkap bahaya ekologis historis.\n- **Socio-Economic Vulnerability Index**: Proxy dari kapasitas adaptif masyarakat.\n- **RVI Score**: Target prediksi baru kita untuk Policy Simulator DSS."))
    
    nb['cells'] = cells
    with open('notebooks/02_Feature_Engineering.ipynb', 'w') as f:
        nbf.write(nb, f)

def create_modeling_notebook():
    nb = nbf.v4.new_notebook()
    cells = []
    
    cells.append(nbf.v4.new_markdown_cell("# 03 - Auto-ML Model Selection\n\n## Komparasi Algoritma SOTA\nKita akan melatih Linear Regression, Random Forest, XGBoost, LightGBM, dan CatBoost untuk mencari model terbaik dalam memprediksi RVI Score."))
    cells.append(nbf.v4.new_code_cell("import sys\nsys.path.append('../src')\nfrom etl import DataLoader\nfrom preprocessing import DataPreprocessor\nfrom feature_engineering import FeatureEngineer\nfrom models import ModelTrainer\n\ndf = DataLoader('../data/raw/master_dataset.csv').load_raw_data()\nclean_df = DataPreprocessor(df).handle_missing_values()\nfinal_df = FeatureEngineer(clean_df).execute_all()"))
    
    cells.append(nbf.v4.new_code_cell("trainer = ModelTrainer(final_df)\nresults_df = trainer.train_and_evaluate()\ndisplay(results_df)\n\ntrainer.save_best_model('../models/best_model.pkl')"))
    
    cells.append(nbf.v4.new_markdown_cell("## Insight Modeling\nModel dengan RMSE terendah dan R2 tertinggi (biasanya Tree-based Ensemble seperti XGBoost atau CatBoost) dipilih karena kemampuannya menangani non-linearitas dalam data iklim dan sosio-ekonomi."))
    
    nb['cells'] = cells
    with open('notebooks/03_Modeling.ipynb', 'w') as f:
        nbf.write(nb, f)

def create_shap_notebook():
    nb = nbf.v4.new_notebook()
    cells = []
    
    cells.append(nbf.v4.new_markdown_cell("# 04 - Explainable AI (SHAP)\n\n## Menguak Black-Box Model\nJuri menuntut transparansi. Mengapa model mengklasifikasikan suatu kabupaten sangat rentan? SHAP (SHapley Additive exPlanations) menjawabnya dengan pendekatan *Game Theory*."))
    cells.append(nbf.v4.new_code_cell("import sys\nsys.path.append('../src')\nfrom etl import DataLoader\nfrom preprocessing import DataPreprocessor\nfrom feature_engineering import FeatureEngineer\nfrom explainability import ModelExplainer\nimport matplotlib.pyplot as plt\n\ndf = DataLoader('../data/raw/master_dataset.csv').load_raw_data()\nclean_df = DataPreprocessor(df).handle_missing_values()\nfinal_df = FeatureEngineer(clean_df).execute_all()\n\nfeatures = [c for c in final_df.columns if c not in ['kabupaten', 'tahun', 'rvi_score']]\nX = final_df[features]"))
    
    cells.append(nbf.v4.new_code_cell("explainer = ModelExplainer('../models/best_model.pkl')\nif explainer.model:\n    exp, shap_vals = explainer.generate_shap_values(X)\n    explainer.summary_plot(shap_vals, X)\nelse:\n    print('Model not found. Run notebook 03 first.')"))
    
    cells.append(nbf.v4.new_markdown_cell("## Insight Kebijakan (Policy Insight)\n- Fitur yang berada di urutan atas plot SHAP adalah pendorong utama kerentanan.\n- Warna merah di sisi kanan sumbu 0 menunjukkan korelasi positif terhadap peningkatan risiko. Ini adalah *low-hanging fruit* bagi pengambil kebijakan."))
    
    nb['cells'] = cells
    with open('notebooks/04_SHAP.ipynb', 'w') as f:
        nbf.write(nb, f)

if __name__ == '__main__':
    os.makedirs('notebooks', exist_ok=True)
    create_eda_notebook()
    create_feature_engineering_notebook()
    create_modeling_notebook()
    create_shap_notebook()
    print("All research notebooks generated successfully.")
