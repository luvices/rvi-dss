import matplotlib.pyplot as plt
import seaborn as sns
import logging

class DataVisualizer:
    """Creates publication-quality plots for research papers and notebooks."""
    
    def __init__(self):
        sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
        plt.rcParams['figure.figsize'] = (12, 8)
        
    @staticmethod
    def plot_correlation_matrix(df, title="Feature Correlation Ranking"):
        """Plot a highly annotated correlation heatmap."""
        plt.figure(figsize=(10, 8))
        corr = df.select_dtypes(include=['float64', 'int64']).corr()
        sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5)
        plt.title(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        return plt
        
    @staticmethod
    def plot_distribution(series, title="Distribution Analysis"):
        """Plot histogram and KDE for a feature."""
        plt.figure(figsize=(10, 6))
        sns.histplot(series, kde=True, bins=30, color='royalblue')
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel(series.name)
        plt.ylabel('Frequency')
        plt.tight_layout()
        return plt
        
    @staticmethod
    def plot_boxplots(df, features, title="Outlier Detection (Boxplot)"):
        """Plot boxplots for multiple features to detect outliers."""
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df[features], palette="Set2")
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt
