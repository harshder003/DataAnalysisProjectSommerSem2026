"""
Preprocess cycling.txt data and convert it to CSV format.

This script reads the space-separated, quoted format cycling data
and converts it to a standard CSV file for further analysis.
"""

import csv
import pandas as pd


def preprocess_cycling_data(input_file='./input_data/cycling.txt', output_file='./input_data/cycling.csv'):
    """
    Convert cycling.txt from space-separated quoted format to CSV.
    
    Parameters:
    -----------
    input_file : str
        Path to the input cycling.txt file
    output_file : str
        Path to the output CSV file
    """
    print(f"Reading data from {input_file}...")
    
    # Read the file and parse space-separated quoted fields
    data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        # Use csv.reader with space delimiter to handle quoted fields properly
        reader = csv.reader(f, delimiter=' ', quotechar='"')
        
        for row in reader:
            # Filter out empty strings that may result from multiple spaces
            row = [field.strip() for field in row if field.strip()]
            if row:  # Skip empty rows
                data.append(row)
    
    print(f"Parsed {len(data)} rows (including header)")
    
    # Convert to DataFrame for easier handling
    if len(data) > 0:
        # First row is header
        header = data[0]
        rows = data[1:]
        
        # Create DataFrame
        df = pd.DataFrame(rows, columns=header)
        
        # Convert points to numeric (it might be stored as string)
        df['points'] = pd.to_numeric(df['points'], errors='coerce')
        
        # Display basic info about the data
        print("\nData Overview:")
        print(f"Shape: {df.shape}")
        print(f"\nColumn names: {list(df.columns)}")
        print(f"\nData types:")
        print(df.dtypes)
        print(f"\nMissing values:")
        print(df.isnull().sum())
        print(f"\nUnique values in categorical columns:")
        print(f"Rider classes: {list(df['rider_class'].unique())}")
        print(f"Stage classes: {list(df['stage_class'].unique())}")
        print(f"Number of unique riders: {df['all_riders'].nunique()}")
        print(f"Number of unique stages: {df['stage'].nunique()}")
        
        # Print summary statistics (avoid printing actual data with special characters)
        print(f"\nSummary statistics for points:")
        print(df['points'].describe())
        
        # Save to CSV
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"\nSuccessfully saved preprocessed data to {output_file}")
        
        return df
    else:
        print("Error: No data found in the file")
        return None


if __name__ == "__main__":
    # Preprocess the data
    df = preprocess_cycling_data()
    
    if df is not None:
        print("\n" + "="*50)
        print("Preprocessing completed successfully!")
        print("="*50)

