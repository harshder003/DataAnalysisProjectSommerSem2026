"""
Hypothesis Testing for Cycling Data

This script performs statistical hypothesis tests to answer the research questions:
1. Is there a difference between the rider classes?
2. Compare their performance on the different stage classes.

Tests include:
- Normality tests (Shapiro-Wilk, Anderson-Darling)
- Variance homogeneity tests (Levene's test)
- ANOVA (if assumptions are met) or Kruskal-Wallis test
- Post-hoc tests (Tukey HSD or Mann-Whitney U)
- Two-way ANOVA for interaction effects
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import shapiro, levene, f_oneway, kruskal, mannwhitneyu
from scipy.stats import anderson
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.anova import anova_lm
from statsmodels.formula.api import ols
import sys
import io
import warnings
warnings.filterwarnings('ignore')

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


def test_normality(data, alpha=0.05):
    """
    Test for normality using Shapiro-Wilk test.
    
    Parameters:
    -----------
    data : array-like
        Data to test
    alpha : float
        Significance level
        
    Returns:
    --------
    dict : Test results
    """
    # For large samples, use Anderson-Darling test (more appropriate)
    if len(data) > 5000:
        result = anderson(data)
        is_normal = result.statistic < result.critical_values[-1]
        return {
            'test': 'Anderson-Darling',
            'statistic': result.statistic,
            'critical_value': result.critical_values[-1],
            'p_value': None,  # Anderson-Darling doesn't provide p-value directly
            'is_normal': is_normal,
            'alpha': alpha
        }
    else:
        # Remove non-finite values
        data_clean = data[np.isfinite(data)]
        if len(data_clean) < 3:
            return None
        
        statistic, p_value = shapiro(data_clean)
        is_normal = p_value > alpha
        return {
            'test': 'Shapiro-Wilk',
            'statistic': statistic,
            'p_value': p_value,
            'is_normal': is_normal,
            'alpha': alpha
        }


def test_variance_homogeneity(groups, alpha=0.05):
    """
    Test for homogeneity of variances using Levene's test.
    
    Parameters:
    -----------
    groups : list of arrays
        Groups to test
    alpha : float
        Significance level
        
    Returns:
    --------
    dict : Test results
    """
    statistic, p_value = levene(*groups)
    equal_variances = p_value > alpha
    return {
        'test': "Levene's",
        'statistic': statistic,
        'p_value': p_value,
        'equal_variances': equal_variances,
        'alpha': alpha
    }


def research_question_1(df):
    """
    Research Question 1: Is there a difference between the rider classes?
    
    Performs appropriate statistical tests based on data assumptions.
    """
    print("="*80)
    print("RESEARCH QUESTION 1: Is there a difference between the rider classes?")
    print("="*80)
    
    # Separate data by rider class
    rider_classes = df['rider_class'].unique()
    groups = [df[df['rider_class'] == cls]['points'].values for cls in rider_classes]
    
    print(f"\nRider classes: {list(rider_classes)}")
    print(f"Group sizes: {[len(g) for g in groups]}")
    
    # Test normality for each group
    print("\n" + "-"*80)
    print("NORMALITY TESTS FOR EACH RIDER CLASS")
    print("-"*80)
    normality_results = {}
    for cls, group in zip(rider_classes, groups):
        result = test_normality(group)
        if result:
            normality_results[cls] = result
            print(f"\n{cls}:")
            print(f"  Test: {result['test']}")
            print(f"  Statistic: {result['statistic']:.4f}")
            if result['p_value'] is not None:
                print(f"  p-value: {result['p_value']:.6f}")
            else:
                print(f"  Critical value: {result['critical_value']:.4f}")
            print(f"  Normal distribution: {result['is_normal']}")
    
    # Test variance homogeneity
    print("\n" + "-"*80)
    print("VARIANCE HOMOGENEITY TEST (Levene's Test)")
    print("-"*80)
    variance_test = test_variance_homogeneity(groups)
    print(f"Test statistic: {variance_test['statistic']:.4f}")
    print(f"p-value: {variance_test['p_value']:.6f}")
    print(f"Equal variances: {variance_test['equal_variances']}")
    
    # Decide on appropriate test
    all_normal = all([r['is_normal'] for r in normality_results.values()]) if normality_results else False
    
    print("\n" + "-"*80)
    print("HYPOTHESIS TEST")
    print("-"*80)
    
    if all_normal and variance_test['equal_variances']:
        # Use ANOVA
        print("\nUsing One-Way ANOVA (assumptions met)")
        print("\nH0: All rider classes have the same mean points")
        print("H1: At least one rider class has a different mean points")
        
        f_statistic, p_value = f_oneway(*groups)
        print(f"\nF-statistic: {f_statistic:.4f}")
        print(f"p-value: {p_value:.6f}")
        
        if p_value < 0.05:
            print(f"\nResult: Reject H0 (p < 0.05)")
            print("There is a statistically significant difference between rider classes.")
            
            # Post-hoc test: Tukey HSD
            print("\n" + "-"*80)
            print("POST-HOC TEST: Tukey HSD")
            print("-"*80)
            # Prepare data for Tukey
            tukey_data = []
            tukey_labels = []
            for cls, group in zip(rider_classes, groups):
                tukey_data.extend(group)
                tukey_labels.extend([cls] * len(group))
            
            tukey_df = pd.DataFrame({'points': tukey_data, 'rider_class': tukey_labels})
            tukey_result = pairwise_tukeyhsd(tukey_df['points'], tukey_df['rider_class'], alpha=0.05)
            print(tukey_result)
            
        else:
            print(f"\nResult: Fail to reject H0 (p >= 0.05)")
            print("No statistically significant difference between rider classes.")
        
        return {
            'test': 'ANOVA',
            'f_statistic': f_statistic,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
    else:
        # Use Kruskal-Wallis test (non-parametric)
        print("\nUsing Kruskal-Wallis test (non-parametric - assumptions not met)")
        print("\nH0: All rider classes have the same distribution of points")
        print("H1: At least one rider class has a different distribution of points")
        
        h_statistic, p_value = kruskal(*groups)
        print(f"\nH-statistic: {h_statistic:.4f}")
        print(f"p-value: {p_value:.6f}")
        
        if p_value < 0.05:
            print(f"\nResult: Reject H0 (p < 0.05)")
            print("There is a statistically significant difference between rider classes.")
            
            # Post-hoc test: Mann-Whitney U (pairwise comparisons with Bonferroni correction)
            print("\n" + "-"*80)
            print("POST-HOC TEST: Mann-Whitney U (with Bonferroni correction)")
            print("-"*80)
            num_comparisons = len(rider_classes) * (len(rider_classes) - 1) // 2
            bonferroni_alpha = 0.05 / num_comparisons
            print(f"Bonferroni corrected alpha: {bonferroni_alpha:.6f}")
            print(f"Number of comparisons: {num_comparisons}")
            
            posthoc_results = []
            for i in range(len(rider_classes)):
                for j in range(i + 1, len(rider_classes)):
                    u_statistic, p_val = mannwhitneyu(groups[i], groups[j], alternative='two-sided')
                    significant = p_val < bonferroni_alpha
                    posthoc_results.append({
                        'group1': rider_classes[i],
                        'group2': rider_classes[j],
                        'u_statistic': u_statistic,
                        'p_value': p_val,
                        'significant': significant
                    })
                    print(f"\n{rider_classes[i]} vs {rider_classes[j]}:")
                    print(f"  U-statistic: {u_statistic:.4f}")
                    print(f"  p-value: {p_val:.6f}")
                    print(f"  Significant: {significant}")
            
        else:
            print(f"\nResult: Fail to reject H0 (p >= 0.05)")
            print("No statistically significant difference between rider classes.")
        
        return {
            'test': 'Kruskal-Wallis',
            'h_statistic': h_statistic,
            'p_value': p_value,
            'significant': p_value < 0.05
        }


def research_question_2(df):
    """
    Research Question 2: Compare their performance on the different stage classes.
    
    Tests if rider classes perform differently across stage classes.
    """
    print("\n\n" + "="*80)
    print("RESEARCH QUESTION 2: Compare performance on different stage classes")
    print("="*80)
    
    # Two-way ANOVA: rider_class × stage_class
    print("\n" + "-"*80)
    print("TWO-WAY ANOVA: Rider Class × Stage Class")
    print("-"*80)
    
    print("\nH0: No interaction effect between rider class and stage class")
    print("H1: There is an interaction effect")
    print("\nH0: No main effect of rider class")
    print("H1: There is a main effect of rider class")
    print("\nH0: No main effect of stage class")
    print("H1: There is a main effect of stage class")
    
    # Fit two-way ANOVA model
    model = ols('points ~ C(rider_class) + C(stage_class) + C(rider_class):C(stage_class)', data=df).fit()
    anova_table = anova_lm(model, typ=2)
    
    print("\nTwo-Way ANOVA Results:")
    print(anova_table)
    
    # Check for interaction effect
    interaction_p = anova_table.loc['C(rider_class):C(stage_class)', 'PR(>F)']
    rider_main_p = anova_table.loc['C(rider_class)', 'PR(>F)']
    stage_main_p = anova_table.loc['C(stage_class)', 'PR(>F)']
    
    print("\n" + "-"*80)
    print("INTERPRETATION")
    print("-"*80)
    
    if interaction_p < 0.05:
        print(f"\nInteraction Effect: SIGNIFICANT (p = {interaction_p:.6f})")
        print("The effect of rider class depends on the stage class.")
        print("Performing separate tests for each stage class...")
        
        # Separate tests for each stage class
        stage_classes = df['stage_class'].unique()
        stage_results = {}
        
        for stage_cls in stage_classes:
            print("\n" + "-"*80)
            print(f"TEST FOR STAGE CLASS: {stage_cls}")
            print("-"*80)
            
            stage_df = df[df['stage_class'] == stage_cls]
            rider_classes = stage_df['rider_class'].unique()
            groups = [stage_df[stage_df['rider_class'] == cls]['points'].values for cls in rider_classes]
            
            # Test normality
            all_normal = True
            for cls, group in zip(rider_classes, groups):
                result = test_normality(group)
                if result and not result['is_normal']:
                    all_normal = False
                    break
            
            # Test variance homogeneity
            variance_test = test_variance_homogeneity(groups)
            
            if all_normal and variance_test['equal_variances']:
                f_stat, p_val = f_oneway(*groups)
                test_name = 'ANOVA'
                statistic = f_stat
            else:
                h_stat, p_val = kruskal(*groups)
                test_name = 'Kruskal-Wallis'
                statistic = h_stat
            
            stage_results[stage_cls] = {
                'test': test_name,
                'statistic': statistic,
                'p_value': p_val,
                'significant': p_val < 0.05
            }
            
            print(f"\nTest: {test_name}")
            print(f"Statistic: {statistic:.4f}")
            print(f"p-value: {p_val:.6f}")
            if p_val < 0.05:
                print(f"Result: SIGNIFICANT - Rider classes differ in {stage_cls} stages")
            else:
                print(f"Result: NOT SIGNIFICANT - No difference between rider classes in {stage_cls} stages")
        
    else:
        print(f"\nInteraction Effect: NOT SIGNIFICANT (p = {interaction_p:.6f})")
        print("The effect of rider class does not depend on the stage class.")
    
    if rider_main_p < 0.05:
        print(f"\nMain Effect of Rider Class: SIGNIFICANT (p = {rider_main_p:.6f})")
    else:
        print(f"\nMain Effect of Rider Class: NOT SIGNIFICANT (p = {rider_main_p:.6f})")
    
    if stage_main_p < 0.05:
        print(f"\nMain Effect of Stage Class: SIGNIFICANT (p = {stage_main_p:.6f})")
    else:
        print(f"\nMain Effect of Stage Class: NOT SIGNIFICANT (p = {stage_main_p:.6f})")
    
    return {
        'interaction_p': interaction_p,
        'rider_main_p': rider_main_p,
        'stage_main_p': stage_main_p,
        'anova_table': anova_table
    }


def main():
    """Main function to run hypothesis tests."""
    print("="*80)
    print("HYPOTHESIS TESTING FOR CYCLING DATA")
    print("="*80)
    
    # Load data
    df = load_data()
    print(f"\nDataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Research Question 1
    rq1_results = research_question_1(df)
    
    # Research Question 2
    rq2_results = research_question_2(df)
    
    print("\n\n" + "="*80)
    print("HYPOTHESIS TESTING COMPLETE")
    print("="*80)
    
    return rq1_results, rq2_results


if __name__ == "__main__":
    rq1_results, rq2_results = main()

