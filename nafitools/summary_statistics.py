import pandas as pd
from scipy.stats import skew, kurtosis

def cal_cs_stats(df, time_column, value_column, additional_percentiles=False):
    """
    Calculate cross-sectional statistics for each time period.
    
    Args:
        df (pd.DataFrame): The data frame containing the data.
        time_column (str): The name of the column representing time periods.
        value_column (str): The name of the column representing the values of X.
        additional_percentiles (list of float): Additional percentiles to calculate (optional).
    
    Returns:
        pd.DataFrame: A data frame containing the calculated statistics for each time period.
    """
    if additional_percentiles:
        additional_percentiles_list = [0.01, 0.02, 0.03, 0.04, 0.96, 0.97, 0.98, 0.99]

    # Function to calculate the required statistics for a given period
    def calc_period_stats(group, additional_percentiles=additional_percentiles):
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
            'N': group[value_column].count()
        }
        
        if additional_percentiles:
            for percentile in additional_percentiles_list:
                stats[f'P{int(percentile*100)}'] = group[value_column].quantile(percentile)
        
        return pd.Series(stats)
    
    # Group the data by the time column and apply the function
    stats_df = df.groupby(time_column).apply(calc_period_stats).reset_index(drop=True)
    
    
    return stats_df

def cal_ts_averages(stats_df):
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