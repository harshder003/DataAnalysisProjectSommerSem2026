"""
Data Exploration Script for Cycling Data Analysis

This script loads the preprocessed cycling data and provides comprehensive
information about the dataset including data types, unique values, and basic statistics.
"""

import pandas as pd
import numpy as np
import sys
import io

# Set UTF-8 encoding for stdout to handle special characters (Windows compatibility)
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)


def explore_cycling_data(csv_file='/input_data/cycling.csv'):
    """
    Load and explore the cycling dataset.
    
    Parameters:
    -----------
    csv_file : str
        Path to the CSV file containing preprocessed cycling data
    """
    print("="*80)
    print("CYCLING DATA EXPLORATION")
    print("="*80)
    
    # Load the data
    print(f"\nLoading data from {csv_file}...")
    df = pd.read_csv(csv_file, encoding='utf-8')
    
    print(f"\nData loaded successfully!")
    print(f"Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")
    
    # Display first few rows
    print("\n" + "="*80)
    print("FIRST 10 ROWS OF THE DATASET")
    print("="*80)
    try:
        print(df.head(10).to_string())
    except UnicodeEncodeError:
        # Fallback: save to string and replace problematic characters
        print(df.head(10).to_string().encode('ascii', 'replace').decode('ascii'))
    
    # Data types
    print("\n" + "="*80)
    print("DATA TYPES")
    print("="*80)
    print(df.dtypes)
    
    # Detailed information about each column
    print("\n" + "="*80)
    print("DETAILED COLUMN INFORMATION")
    print("="*80)
    
    for col in df.columns:
        print(f"\n--- Column: {col} ---")
        print(f"  Data type: {df[col].dtype}")
        print(f"  Non-null count: {df[col].notna().sum()} / {len(df)}")
        print(f"  Null count: {df[col].isna().sum()}")
        
        # For categorical/object columns
        if df[col].dtype == 'object':
            n_unique = df[col].nunique()
            print(f"  Unique values: {n_unique}")
            
            if n_unique < 10:
                print(f"  Unique values list:")
                unique_vals = df[col].unique()
                for i, val in enumerate(sorted(unique_vals), 1):
                    count = (df[col] == val).sum()
                    print(f"    {i}. '{val}' (appears {count} times)")
            else:
                print(f"  First 10 unique values: {list(df[col].unique()[:10])}")
                print(f"  (Showing first 10 out of {n_unique} unique values)")
        
        # For numeric columns
        elif pd.api.types.is_numeric_dtype(df[col]):
            print(f"  Summary statistics:")
            print(f"    Mean: {df[col].mean():.2f}")
            print(f"    Median: {df[col].median():.2f}")
            print(f"    Std: {df[col].std():.2f}")
            print(f"    Min: {df[col].min()}")
            print(f"    Max: {df[col].max()}")
            print(f"    25th percentile: {df[col].quantile(0.25)}")
            print(f"    75th percentile: {df[col].quantile(0.75)}")
    
    # Overall dataset summary
    print("\n" + "="*80)
    print("DATASET SUMMARY")
    print("="*80)
    print(f"\nTotal number of records: {len(df)}")
    print(f"Total number of columns: {len(df.columns)}")
    print(f"\nColumn names: {list(df.columns)}")
    
    # Missing values summary
    print("\n" + "="*80)
    print("MISSING VALUES SUMMARY")
    print("="*80)
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(missing[missing > 0])
    else:
        print("No missing values found in the dataset.")
    
    # Categorical variables summary
    print("\n" + "="*80)
    print("CATEGORICAL VARIABLES SUMMARY")
    print("="*80)
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        print(f"\n{col}:")
        print(f"  Number of unique values: {df[col].nunique()}")
        if df[col].nunique() < 10:
            print(f"  Unique values:")
            value_counts = df[col].value_counts()
            for val, count in value_counts.items():
                percentage = (count / len(df)) * 100
                print(f"    - '{val}': {count} ({percentage:.2f}%)")
    
    # Numeric variables summary
    print("\n" + "="*80)
    print("NUMERIC VARIABLES SUMMARY")
    print("="*80)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        print(df[numeric_cols].describe())
    else:
        print("No numeric variables found.")
    
    print("\n" + "="*80)
    print("EXPLORATION COMPLETE")
    print("="*80)
    
    return df


if __name__ == "__main__":
    # Explore the data
    df = explore_cycling_data()
    
    # Additional: Show sample of data
    print("\n\nSample data (first 5 rows):")
    try:
        print(df.head().to_string())
    except UnicodeEncodeError:
        print(df.head().to_string().encode('ascii', 'replace').decode('ascii'))

