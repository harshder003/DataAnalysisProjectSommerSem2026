# Data Analysis Project - Sommer Semester 2026

A data analysis project focused on processing and analyzing cycling data.

## Project Overview

This project involves preprocessing and analyzing cycling data, starting with converting raw text data into a structured CSV format for further analysis.

## Steps Performed

### Step 1: Data Acquisition and CSV Conversion
- **Input**: Raw cycling data from `cycling.txt` file
- **Process**: 
  - Read space-separated, quoted format data from the text file
  - Parse and clean the data using CSV reader with proper delimiter handling
  - Convert the data into a structured pandas DataFrame
  - Perform data type conversions and basic data validation
  - Generate summary statistics and data overview
- **Output**: Clean, structured CSV file (`cycling.csv`) ready for analysis

The preprocessing script (`preprocess_cycling_data.py`) handles:
- Parsing space-separated quoted fields
- Data type conversion (especially for numeric points column)
- Data quality checks (missing values, unique counts)
- Summary statistics generation

## Files

- `cycling.txt` - Raw input data file
- `preprocess_cycling_data.py` - Python script for data preprocessing
- `cycling.csv` - Processed CSV output file

## Requirements

- Python 3.x
- pandas
- csv (built-in module)

## Usage

Run the preprocessing script:

```bash
python preprocess_cycling_data.py
```

This will:
1. Read data from `cycling.txt`
2. Process and validate the data
3. Display data overview and statistics
4. Save the processed data to `cycling.csv`

## Future Steps

Additional analysis steps will be documented here as the project progresses.

