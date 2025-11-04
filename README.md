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

### Step 2: Data Exploration
- **Input**: Processed CSV data from `cycling.csv` file
- **Process**: 
  - Load the preprocessed cycling dataset
  - Analyze data types for all columns
  - Identify categorical variables and list unique values (for variables with <10 unique values)
  - Generate detailed statistics for numeric variables
  - Check for missing values across all columns
  - Display sample data rows
- **Output**: Comprehensive data exploration report saved to `logging.txt`

The exploration script (`explore_cycling_data.py`) provides:
- Complete data type information for each column
- Unique value counts and lists for categorical variables
- Summary statistics for numeric variables
- Missing value analysis
- Dataset overview and structure

## Files

- `cycling.txt` - Raw input data file
- `preprocess_cycling_data.py` - Python script for data preprocessing
- `cycling.csv` - Processed CSV output file
- `explore_cycling_data.py` - Python script for comprehensive data exploration
- `logging.txt` - Output log file containing detailed data exploration results

## Requirements

- Python 3.x
- pandas
- numpy
- csv (built-in module)

## Usage

### Step 1: Preprocess the data

Run the preprocessing script:

```bash
python preprocess_cycling_data.py
```

This will:
1. Read data from `cycling.txt`
2. Process and validate the data
3. Display data overview and statistics
4. Save the processed data to `cycling.csv`

### Step 2: Explore the data

Run the exploration script:

```bash
python explore_cycling_data.py
```

This will:
1. Load the processed data from `cycling.csv`
2. Analyze data types and structure
3. Display detailed information about categorical and numeric variables
4. Save the complete exploration output to `logging.txt`

## Future Steps

Additional analysis steps will be documented here as the project progresses.

