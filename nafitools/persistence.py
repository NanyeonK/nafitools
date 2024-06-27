import pandas as pd
import numpy as np

def cal_cs_persistence(df, time_column, value_columns, entity_column=None, max_tau=5):
    """
    Calculate the cross-sectional Pearson correlations for multiple variables measured tau periods apart for multiple tau values.
    
    Args:
        df (pd.DataFrame): The data frame containing the data.
        time_column (str): The name of the column representing time periods.
        value_columns (list of str): The names of the columns representing the values of the variables.
        entity_column (str or None): The name of the column representing the entities. If None, calculate persistence without entity grouping.
        max_tau (int): The maximum number of periods apart to measure persistence.
    
    Returns:
        dict of pd.DataFrame: A dictionary containing the persistence correlations for each variable.
    """
    persistence_results = {}

    for value_column in value_columns:
        # Ensure the dataframe is sorted by the time column (and entity column if provided)
        if entity_column:
            df = df.sort_values(by=[time_column, entity_column]).reset_index(drop=True)
        else:
            df = df.sort_values(by=[time_column]).reset_index(drop=True)
        
        # Create a dictionary to store the results
        results = {f't+{tau}': [] for tau in range(1, max_tau + 1)}
        results['Year'] = []

        # Get unique time periods
        unique_times = df[time_column].unique()

        # Loop over each time period
        for t in unique_times:
            period_df = df[df[time_column] == t]
            
            if len(period_df) == 0:
                continue

            correlations = []
            
            for tau in range(1, max_tau + 1):
                future_time = t + pd.DateOffset(months=tau)
                
                if future_time not in unique_times:
                    correlations.append(np.nan)
                    continue
                
                shifted_df = df[df[time_column] == future_time]
                
                if entity_column:
                    # Merge on entities to ensure we only consider those with valid values for both t and t+tau
                    merged_df = pd.merge(period_df, shifted_df, on=entity_column, suffixes=('', f'_shifted_{tau}'))
                else:
                    # If no entity column, just ensure both periods have data
                    merged_df = pd.concat([period_df.reset_index(), shifted_df.reset_index()], axis=1, keys=['t', 't+tau'])

                if len(merged_df) == 0:
                    correlations.append(np.nan)
                    continue
                
                # Calculate means
                X_t = merged_df[value_column] if entity_column else merged_df[('t', value_column)]
                X_t_tau = merged_df[f'{value_column}_shifted_{tau}'] if entity_column else merged_df[('t+tau', value_column)]
                mean_X_t = X_t.mean()
                mean_X_t_tau = X_t_tau.mean()

                # Calculate numerator and denominator separately
                numerator = ((X_t - mean_X_t) * (X_t_tau - mean_X_t_tau)).sum()
                denominator = np.sqrt(((X_t - mean_X_t) ** 2).sum() * ((X_t_tau - mean_X_t_tau) ** 2).sum())
                
                if denominator == 0:
                    correlations.append(np.nan)
                else:
                    pearson_corr = numerator / denominator
                    correlations.append(pearson_corr)
            
            results['Year'].append(t)
            for tau, corr in zip(range(1, max_tau + 1), correlations):
                results[f't+{tau}'].append(corr)
        
        results_df = pd.DataFrame(results)
        results_df.set_index('Year', inplace=True)
        persistence_results[value_column] = results_df

    return persistence_results

def calculate_average_persistence(persistence_results, max_tau):
    """
    Calculate the time-series average of the periodic cross-sectional correlations for multiple variables.
    
    Args:
        persistence_results (dict of pd.DataFrame): A dictionary containing the periodic cross-sectional correlations for each variable.
        max_tau (int): The maximum number of periods apart to measure persistence.
    
    Returns:
        pd.DataFrame: A data frame containing the average persistence values for each variable and each lag.
    """
    avg_persistence = {f't+{tau}': [] for tau in range(1, max_tau + 1)}
    avg_persistence['Variable'] = []

    for variable, persistence_df in persistence_results.items():
        avg_persistence['Variable'].append(variable)
        for tau in range(1, max_tau + 1):
            avg_persistence[f't+{tau}'].append(persistence_df[f't+{tau}'].mean())

    avg_persistence_df = pd.DataFrame(avg_persistence)
    avg_persistence_df.set_index('Variable', inplace=True)
    return avg_persistence_df