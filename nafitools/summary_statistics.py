import pandas as pd
from scipy.stats import skew, kurtosis, pearsonr, spearmanr, rankdata

def cal_cs_stats(df, time_column, value_column, additional_percentiles=False):
    """
    Calculate cross-sectional statistics for each time period, handling NaN values and reporting them.
    
    Args:
        df (pd.DataFrame): The data frame containing the data.
        time_column (str): The name of the column representing time periods.
        value_column (str): The name of the column representing the values of X.
        additional_percentiles (bool or list of float): Additional percentiles to calculate (optional).
    
    Returns:
        pd.DataFrame: A data frame containing the calculated statistics for each time period.
    """
    # Drop NaN values in the value column and report them
    nan_report = df[df[value_column].isna()]
    if not nan_report.empty:
        print(f"NaN values found in column {value_column} for the following rows:")
        print(nan_report)
    df_clean = df.dropna(subset=[value_column])
    
    # Define additional percentiles if required
    if additional_percentiles is True:
        additional_percentiles_list = [0.01, 0.02, 0.03, 0.04, 0.96, 0.97, 0.98, 0.99]
    elif isinstance(additional_percentiles, list):
        additional_percentiles_list = additional_percentiles
    else:
        additional_percentiles_list = []
    
    # Function to calculate the required statistics for a given period
    def calc_period_stats(group):
        stats = {
            'Time': group[time_column].iloc[0],  # Time column
            'Mean': group[value_column].mean(),
            'SD': group[value_column].std(),
            'Skew': skew(group[value_column], nan_policy='omit'),
            'Kurt': kurtosis(group[value_column], nan_policy='omit'),
            'Min': group[value_column].min(),
            'Median': group[value_column].median(),
            'Max': group[value_column].max(),
            'P5': group[value_column].quantile(0.05),
            'P25': group[value_column].quantile(0.25),
            'P75': group[value_column].quantile(0.75),
            'P95': group[value_column].quantile(0.95),
            'N': group[value_column].count(),
            'NaN_count': group[value_column].isna().sum()  # Report the number of NaN values
        }
        
        for percentile in additional_percentiles_list:
            stats[f'P{int(percentile*100)}'] = group[value_column].quantile(percentile)
        
        return pd.Series(stats)
    
    # Group the data by the time column and apply the function
    stats_df = df_clean.groupby(time_column, group_keys=False).apply(calc_period_stats).reset_index(drop=True)
    
    return stats_df

def cal_ts_stats(stats_df):
    """
    Calculate the time-series averages of the cross-sectional statistics.
    
    Args:
        stats_df (pd.DataFrame): A data frame containing cross-sectional statistics for each time period.
    
    Returns:
        pd.Series: A series containing the time-series averages of the cross-sectional statistics.
    """
    # Exclude the time column for averaging
    stats_to_average = stats_df.drop(columns=['Time'])
    
    # Calculate the time-series averages
    time_series_averages = stats_to_average.mean()
    
    df = pd.DataFrame(time_series_averages).T

    return df