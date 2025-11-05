"""
Descriptive Analysis for Cycling Data

This script performs detailed descriptive analysis of the cycling dataset,
focusing on comparing rider classes and their performance across different stage classes.
Includes statistical measures and visualizations.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import sys
import io

# Set UTF-8 encoding for stdout (Windows compatibility)
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


def load_data(csv_file='./input_data/cycling.csv'):
    """Load the preprocessed cycling data."""
    df = pd.read_csv(csv_file, encoding='utf-8')
    return df


def descriptive_statistics_by_rider_class(df):
    """
    Calculate descriptive statistics grouped by rider class.
    
    Returns a summary DataFrame with statistics for each rider class.
    """
    print("="*80)
    print("DESCRIPTIVE STATISTICS BY RIDER CLASS")
    print("="*80)
    
    stats_by_class = df.groupby('rider_class')['points'].agg([
        ('count', 'count'),
        ('mean', 'mean'),
        ('median', 'median'),
        ('std', 'std'),
        ('min', 'min'),
        ('max', 'max'),
        ('q25', lambda x: x.quantile(0.25)),
        ('q75', lambda x: x.quantile(0.75)),
        ('iqr', lambda x: x.quantile(0.75) - x.quantile(0.25)),
        ('skewness', lambda x: stats.skew(x)),
        ('kurtosis', lambda x: stats.kurtosis(x))
    ]).round(2)
    
    print("\nSummary Statistics by Rider Class:")
    print(stats_by_class)
    
    # Additional: Percentage of zero points
    print("\nPercentage of zero points by rider class:")
    zero_pct = df.groupby('rider_class')['points'].apply(
        lambda x: (x == 0).sum() / len(x) * 100
    ).round(2)
    print(zero_pct)
    
    return stats_by_class


def descriptive_statistics_by_stage_class(df):
    """
    Calculate descriptive statistics grouped by stage class.
    
    Returns a summary DataFrame with statistics for each stage class.
    """
    print("\n" + "="*80)
    print("DESCRIPTIVE STATISTICS BY STAGE CLASS")
    print("="*80)
    
    stats_by_stage = df.groupby('stage_class')['points'].agg([
        ('count', 'count'),
        ('mean', 'mean'),
        ('median', 'median'),
        ('std', 'std'),
        ('min', 'min'),
        ('max', 'max'),
        ('q25', lambda x: x.quantile(0.25)),
        ('q75', lambda x: x.quantile(0.75)),
        ('iqr', lambda x: x.quantile(0.75) - x.quantile(0.25))
    ]).round(2)
    
    print("\nSummary Statistics by Stage Class:")
    print(stats_by_stage)
    
    return stats_by_stage


def descriptive_statistics_interaction(df):
    """
    Calculate descriptive statistics for the interaction between rider class and stage class.
    """
    print("\n" + "="*80)
    print("DESCRIPTIVE STATISTICS: RIDER CLASS × STAGE CLASS")
    print("="*80)
    
    interaction_stats = df.groupby(['rider_class', 'stage_class'])['points'].agg([
        ('count', 'count'),
        ('mean', 'mean'),
        ('median', 'median'),
        ('std', 'std')
    ]).round(2)
    
    print("\nSummary Statistics by Rider Class and Stage Class:")
    print(interaction_stats)
    
    return interaction_stats


def create_visualizations(df):
    """
    Create statistical graphics for the descriptive analysis.
    Saves all visualizations as PNG files.
    """
    print("\n" + "="*80)
    print("CREATING VISUALIZATIONS")
    print("="*80)
    
    # 1. Bar plot: Mean points by rider class
    fig, ax = plt.subplots(figsize=(10, 6))
    mean_by_class = df.groupby('rider_class')['points'].mean().sort_values(ascending=False)
    bars = ax.bar(range(len(mean_by_class)), mean_by_class.values, color=sns.color_palette("husl", len(mean_by_class)))
    ax.set_xticks(range(len(mean_by_class)))
    ax.set_xticklabels(mean_by_class.index, rotation=45, ha='right')
    ax.set_xlabel('Rider Class', fontsize=12)
    ax.set_ylabel('Mean Points', fontsize=12)
    ax.set_title('Mean Points by Rider Class', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars, mean_by_class.values)):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{val:.2f}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('./results/descriptive_barplot_mean_rider_class.png', dpi=300, bbox_inches='tight')
    print("Saved: ./results/descriptive_barplot_mean_rider_class.png")
    plt.close()
    
    # 2. Interaction plot: Mean points by rider class and stage class
    fig, ax = plt.subplots(figsize=(12, 6))
    interaction_means = df.groupby(['rider_class', 'stage_class'])['points'].mean().unstack()
    interaction_means.plot(kind='bar', ax=ax, width=0.8)
    ax.set_xlabel('Rider Class', fontsize=12)
    ax.set_ylabel('Mean Points', fontsize=12)
    ax.set_title('Mean Points by Rider Class and Stage Class', fontsize=14, fontweight='bold')
    ax.legend(title='Stage Class', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('./results/descriptive_barplot_interaction.png', dpi=300, bbox_inches='tight')
    print("Saved: ./results/descriptive_barplot_interaction.png")
    plt.close()
    
    # 3. Heatmap: Mean points by rider class and stage class
    fig, ax = plt.subplots(figsize=(10, 6))
    interaction_means = df.groupby(['rider_class', 'stage_class'])['points'].mean().unstack()
    sns.heatmap(interaction_means, annot=True, fmt='.2f', cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Mean Points'})
    ax.set_title('Mean Points Heatmap: Rider Class × Stage Class', fontsize=14, fontweight='bold')
    ax.set_xlabel('Stage Class', fontsize=12)
    ax.set_ylabel('Rider Class', fontsize=12)
    plt.tight_layout()
    plt.savefig('./results/descriptive_heatmap_interaction.png', dpi=300, bbox_inches='tight')
    print("Saved: ./results/descriptive_heatmap_interaction.png")
    plt.close()


def overall_descriptive_statistics(df):
    """Calculate overall descriptive statistics for the entire dataset."""
    print("\n" + "="*80)
    print("OVERALL DESCRIPTIVE STATISTICS")
    print("="*80)
    
    print(f"\nTotal number of observations: {len(df)}")
    print(f"\nOverall Statistics for Points:")
    print(df['points'].describe())
    
    print(f"\nAdditional Statistics:")
    print(f"  Standard Deviation: {df['points'].std():.2f}")
    print(f"  Variance: {df['points'].var():.2f}")
    print(f"  Skewness: {stats.skew(df['points']):.2f}")
    print(f"  Kurtosis: {stats.kurtosis(df['points']):.2f}")
    print(f"  Coefficient of Variation: {(df['points'].std() / df['points'].mean() * 100):.2f}%")
    
    print(f"\n  Interquartile Range (IQR): {df['points'].quantile(0.75) - df['points'].quantile(0.25):.2f}")
    print(f"  Range: {df['points'].max() - df['points'].min()}")


def main():
    """Main function to run descriptive analysis."""
    print("="*80)
    print("DESCRIPTIVE ANALYSIS OF CYCLING DATA")
    print("="*80)
    
    # Load data
    df = load_data()
    print(f"\nDataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Overall statistics
    overall_descriptive_statistics(df)
    
    # Statistics by rider class
    stats_by_class = descriptive_statistics_by_rider_class(df)
    
    # Statistics by stage class
    stats_by_stage = descriptive_statistics_by_stage_class(df)
    
    # Statistics for interaction
    interaction_stats = descriptive_statistics_interaction(df)
    
    # Create visualizations
    create_visualizations(df)
    
    print("\n" + "="*80)
    print("DESCRIPTIVE ANALYSIS COMPLETE")
    print("="*80)
    print("\nAll visualizations have been saved as PNG files.")
    
    return df, stats_by_class, stats_by_stage, interaction_stats


if __name__ == "__main__":
    df, stats_by_class, stats_by_stage, interaction_stats = main()

