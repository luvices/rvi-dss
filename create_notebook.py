import nbformat as nbf

nb = nbf.v4.new_notebook()

text_1 = """\
# Regional Vulnerability Intelligence (RVI) - Data Pipeline & EDA
Notebook ini dibuat untuk melakukan pembersihan data, Exploratory Data Analysis (EDA), dan pembuatan model Machine Learning berdasarkan data `master_dataset.csv`.

*Pastikan Anda sudah menjalankan `generate_mock_data.py` atau memiliki file `master_dataset.csv` sebelum menjalankan notebook ini.*
"""

code_1 = """\
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for seaborn
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Load Data
df = pd.read_csv('master_dataset.csv')
display(df.head())
"""

text_2 = """\
## 1. Data Cleaning
Mari kita periksa missing values dan tipe datanya.
"""

code_2 = """\
print("Informasi Dataset:")
df.info()

print("\\nJumlah Missing Values per Kolom:")
print(df.isnull().sum())
"""

code_3 = """\
# Mengisi missing values dengan median (karena data mungkin memiliki outlier)
for col in ['curah_hujan', 'suhu', 'kelembaban', 'sanitasi']:
    df[col] = df[col].fillna(df[col].median())

print("\\nJumlah Missing Values setelah cleaning:")
print(df.isnull().sum())
"""

text_3 = """\
## 2. Exploratory Data Analysis (EDA)
### 2.1 Distribusi Variabel Target
Misalkan kita ingin menganalisis `produksi_padi` sebagai variabel target kita.
"""

code_4 = """\
sns.histplot(df['produksi_padi'], kde=True, bins=20, color='skyblue')
plt.title('Distribusi Produksi Padi')
plt.xlabel('Produksi Padi (Ton)')
plt.ylabel('Frekuensi')
plt.show()
"""

text_4 = """\
### 2.2 Korelasi antar Fitur
Mari kita lihat hubungan antara variabel iklim, sosial ekonomi, dan produksi padi.
"""

code_5 = """\
# Select only numerical columns for correlation
numeric_cols = df.select_dtypes(include=[np.number]).columns
corr = df[numeric_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Heatmap Korelasi Fitur RVI')
plt.show()
"""

text_5 = """\
### 2.3 Tren Produksi Padi per Tahun
"""

code_6 = """\
yearly_prod = df.groupby('tahun')['produksi_padi'].mean().reset_index()

sns.lineplot(data=yearly_prod, x='tahun', y='produksi_padi', marker='o', linewidth=2.5, color='green')
plt.title('Rata-rata Produksi Padi per Tahun (2018-2023)')
plt.xlabel('Tahun')
plt.ylabel('Rata-rata Produksi Padi')
plt.xticks(df['tahun'].unique())
plt.show()
"""

text_6 = """\
## 3. Modeling (Prediksi Kerentanan / Vulnerability)
Kita akan membuat model **Random Forest Regressor** untuk memprediksi hasil produksi padi. 
Kabupaten yang prediksinya rendah bisa dikategorikan sebagai daerah yang lebih rentan secara pangan.
"""

code_7 = """\
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Fitur yang digunakan
features = ['curah_hujan', 'suhu', 'kelembaban', 'ipm', 'kemiskinan', 'sanitasi', 'air_bersih']
target = 'produksi_padi'

X = df[features]
y = df[target]

# Split data (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Jumlah data training: {len(X_train)}")
print(f"Jumlah data testing: {len(X_test)}")
"""

code_8 = """\
# Inisialisasi dan latih model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Prediksi menggunakan data testing
y_pred = model.predict(X_test)

# Evaluasi Model
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"Root Mean Squared Error (RMSE): {rmse:,.2f}")
print(f"R-squared (R2 Score): {r2:.4f}")
"""

text_7 = """\
### 3.1 Feature Importance
Fitur apa saja yang paling berkontribusi terhadap produksi padi berdasarkan model kita?
"""

code_9 = """\
feature_imp = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)

sns.barplot(x=feature_imp, y=feature_imp.index, palette='viridis', hue=feature_imp.index, legend=False)
plt.title('Feature Importance (Random Forest)')
plt.xlabel('Importance Score')
plt.ylabel('Fitur')
plt.show()
"""

nb['cells'] = [
    nbf.v4.new_markdown_cell(text_1),
    nbf.v4.new_code_cell(code_1),
    nbf.v4.new_markdown_cell(text_2),
    nbf.v4.new_code_cell(code_2),
    nbf.v4.new_code_cell(code_3),
    nbf.v4.new_markdown_cell(text_3),
    nbf.v4.new_code_cell(code_4),
    nbf.v4.new_markdown_cell(text_4),
    nbf.v4.new_code_cell(code_5),
    nbf.v4.new_markdown_cell(text_5),
    nbf.v4.new_code_cell(code_6),
    nbf.v4.new_markdown_cell(text_6),
    nbf.v4.new_code_cell(code_7),
    nbf.v4.new_code_cell(code_8),
    nbf.v4.new_markdown_cell(text_7),
    nbf.v4.new_code_cell(code_9)
]

with open('RVI_Pipeline.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Berhasil membuat RVI_Pipeline.ipynb")
