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

### Step 3: Descriptive Analysis
- **Input**: Processed CSV data from `cycling.csv` file
- **Process**: 
  - Calculate descriptive statistics (mean, median, std, IQR, skewness, kurtosis) for overall dataset
  - Compute statistics grouped by rider class
  - Compute statistics grouped by stage class
  - Analyze interaction between rider class and stage class
  - Create statistical visualizations (box plots, violin plots, bar charts, heatmaps)
- **Output**: Detailed descriptive statistics and multiple PNG visualization files

The descriptive analysis script (`descriptive_analysis.py`) provides:
- Overall descriptive statistics for the points variable
- Statistics grouped by rider class (All Rounder, Climber, Sprinter, Unclassed)
- Statistics grouped by stage class (flat, hills, mount)
- Interaction statistics (rider class × stage class)
- Multiple statistical graphics saved as PNG files

### Step 4: Hypothesis Testing
- **Input**: Processed CSV data from `cycling.csv` file
- **Process**: 
  - Test assumptions (normality, variance homogeneity)
  - Research Question 1: Test for differences between rider classes using appropriate tests (ANOVA or Kruskal-Wallis)
  - Perform post-hoc tests (Tukey HSD or Mann-Whitney U with Bonferroni correction)
  - Research Question 2: Test interaction effects using two-way ANOVA
  - Perform separate tests for each stage class when interaction is significant
  - Create visualizations for test results
- **Output**: Statistical test results and visualization files

The hypothesis testing script (`hypothesis_testing.py`) provides:
- Normality tests (Shapiro-Wilk) for each group
- Variance homogeneity tests (Levene's test)
- Main hypothesis tests (ANOVA or Kruskal-Wallis based on assumptions)
- Post-hoc pairwise comparisons
- Two-way ANOVA for interaction effects
- Visualizations of test results saved as PNG files

## Files

- `cycling.txt` - Raw input data file
- `preprocess_cycling_data.py` - Python script for data preprocessing
- `cycling.csv` - Processed CSV output file
- `explore_cycling_data.py` - Python script for comprehensive data exploration
- `descriptive_analysis.py` - Python script for detailed descriptive analysis
- `hypothesis_testing.py` - Python script for statistical hypothesis testing
- `logging.txt` - Output log file containing detailed analysis results
- `descriptive_*.png` - Statistical visualizations from descriptive analysis (box plots, bar charts, heatmaps)
- `hypothesis_test_*.png` - Visualizations from hypothesis testing results

## Requirements

- Python 3.x
- pandas
- numpy
- matplotlib
- seaborn
- scipy
- statsmodels
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

### Step 3: Descriptive Analysis

Run the descriptive analysis script:

```bash
python descriptive_analysis.py
```

This will:
1. Load the processed data from `cycling.csv`
2. Calculate comprehensive descriptive statistics
3. Generate statistics grouped by rider class and stage class
4. Create multiple statistical visualizations
5. Save all visualizations as PNG files

### Step 4: Hypothesis Testing

Run the hypothesis testing script:

```bash
python hypothesis_testing.py
```

This will:
1. Load the processed data from `cycling.csv`
2. Test statistical assumptions (normality, variance homogeneity)
3. Perform hypothesis tests for research questions
4. Generate post-hoc tests when needed
