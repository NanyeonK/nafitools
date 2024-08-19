import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

def cal_corr(group, var1, var2, option='all'):
    """
    Calculate the correlation between two variables for a given period.

    Args:
        group (pd.DataFrame): The data for the given period.
        var1 (str): The name of the first variable.
        var2 (str): The name of the second variable.
        option (str): The correlation type to calculate ('pearson', 'spearman', or 'all'). Defaults to 'all'.
        
    Returns:
        pd.Series: A series containing the correlation between the two variables.
    """
    # Drop NaN values for the variables being correlated
    group = group[[var1, var2]].dropna()
    
    if len(group) < 2:
        return pd.Series({'Pearson': np.nan, 'Spearman': np.nan})

    if option == 'pearson':
        pearson_corr, _ = pearsonr(group[var1], group[var2])
        return pd.Series({'Pearson': pearson_corr})
    elif option == 'spearman':
        spearman_corr, _ = spearmanr(group[var1], group[var2])
        return pd.Series({'Spearman': spearman_corr})
    elif option == 'all':
        pearson_corr, _ = pearsonr(group[var1], group[var2])
        spearman_corr, _ = spearmanr(group[var1], group[var2])
        return pd.Series({'Pearson': pearson_corr, 'Spearman': spearman_corr})
    else:
        raise ValueError("Invalid option for correlation type. Choose from 'pearson', 'spearman', or 'all'.")

def cal_per_corr(df, time_column, specific_date=None):
    """
    Calculate Pearson and Spearman correlations for each time period for all pairs of variables.
    
    Args:
        df (pd.DataFrame): The data frame containing the data.
        time_column (str): The name of the column representing time periods.
        specific_date (str or None): A specific date to filter the data. If None, calculate for all dates.
    
    Returns:
        pd.DataFrame: A data frame containing the Pearson and Spearman correlations for each time period.
    """
    if specific_date:
        df = df[df[time_column] == specific_date]

    variables = [col for col in df.columns if col != time_column]
    correlations = []

    for i, var1 in enumerate(variables):
        for var2 in variables[i+1:]:
            corr_df = df.groupby(time_column).apply(lambda group: cal_corr(group, var1, var2)).reset_index()
            corr_df['Var1'] = var1
            corr_df['Var2'] = var2
            correlations.append(corr_df)

    all_correlations = pd.concat(correlations, ignore_index=True)
    return all_correlations

def cal_ts_avcorr(correlations_df):
    """
    Calculate the time-series averages of the periodic cross-sectional correlations.
    
    Args:
        correlations_df (pd.DataFrame): A data frame containing the periodic correlations.
    
    Returns:
        pd.DataFrame: A data frame containing the time-series average Pearson and Spearman correlations.
    """
    avg_corrs = correlations_df.groupby(['Var1', 'Var2'])[['Pearson', 'Spearman']].mean().reset_index()
    return avg_corrs

def create_corr_mat(avg_corrs, variables):
    """
    Create a correlation matrix with Pearson correlations below the diagonal and Spearman correlations above the diagonal.
    
    Args:
        avg_corrs (pd.DataFrame): A data frame containing the average correlations.
        variables (list of str): List of column names representing the variables.
    
    Returns:
        pd.DataFrame: A correlation matrix.
    """
    matrix = pd.DataFrame(index=variables, columns=variables)

    for _, row in avg_corrs.iterrows():
        var1, var2 = row['Var1'], row['Var2']
        pearson, spearman = row['Pearson'], row['Spearman']
        matrix.at[var1, var2] = f"{spearman:.2f}"
        matrix.at[var2, var1] = f"{pearson:.2f}"
    
    np.fill_diagonal(matrix.values, np.nan)
    return matrix