import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Truncate
def truncate(data, column=False, lower=0.01, upper=0.99, copy=True):
    """
    Truncates the input data by removing values outside the specified quantiles.
    
    Parameters:
    data (pd.Series or pd.DataFrame): The data to be truncated.
    column (str or bool): The column to be truncated or False to truncate all columns. Defaults to False.
    lower (float): The lower quantile threshold. Defaults to 0.01.
    upper (float): The upper quantile threshold. Defaults to 0.99.
    copy (bool): Whether to return a copy of the data or to modify it in place. Defaults to True.
    
    Returns:
        pd.Series or pd.DataFrame: The truncated data.
    """
    print(f"Data truncated between {lower} and {upper}\n")
    
    if copy:
        data = data.copy()
    
    if column:
        col_data = data[column]
        
        print(f"Original maximum of {column}: {col_data.max()} and Original minimum of {column}: {col_data.min()}\n")
        
        qtl = col_data.quantile([lower, upper])
        
        # Remove values below the lower quantile
        col_data = col_data[col_data >= qtl.loc[lower]]
        
        # Remove values above the upper quantile
        col_data = col_data[col_data <= qtl.loc[upper]]
        
        data = data[data[column].isin(col_data)]
        
        print(f"New maximum of {column}: {col_data.max()} and New minimum of {column}: {col_data.min()}\n")
    else:
        for col in data.columns:
            col_data = data[col]
            
            original_max = col_data.max()
            original_min = col_data.min()
            
            qtl = col_data.quantile([lower, upper])
            
            # Apply truncation
            mask = (col_data >= qtl.loc[lower]) & (col_data <= qtl.loc[upper])
            col_data = col_data[mask]
            
            data = data[mask]
            
            new_max = col_data.max()
            new_min = col_data.min()
            
            print(f"Column: {col}")
            print(f"Original maximum: {original_max}, Original minimum: {original_min}")
            print(f"New maximum: {new_max}, New minimum: {new_min}\n")
    
    return data

# Winsorize
def winsorize(data, column=False, lower=0.01, upper=0.99, copy=True):
    """
    Winsorizes the input data by replacing extreme values with the nearest values within the specified quantiles.
    
    Parameters:
    data (pd.Series or pd.DataFrame): The data to be winsorized.
    column (str or bool): The column to be winsorized or False to winsorize all columns. Defaults to False.
    lower (float): The lower quantile threshold. Defaults to 0.01.
    upper (float): The upper quantile threshold. Defaults to 0.99.
    copy (bool): Whether to return a copy of the data or to modify it in place. Defaults to True.
    
    Returns:
        pd.Series or pd.DataFrame: The winsorized data.
    """
    if copy:
        data = data.copy()
    
    if column:
        col_data = data[column]
        
        print(f"Original maximum of {column}: {col_data.max()} and Original minimum of {column}: {col_data.min()}\n")
        
        qtl = col_data.quantile([lower, upper])
        
        # Replace values below the lower quantile
        col_data[col_data < qtl.loc[lower]] = qtl.loc[lower]
        
        # Replace values above the upper quantile
        col_data[col_data > qtl.loc[upper]] = qtl.loc[upper]
        
        data[column] = col_data
        
        print(f"New maximum of {column}: {col_data.max()} and New minimum of {column}: {col_data.min()}\n")
    else:
        for col in data.columns:
            col_data = data[col]
            
            print(f"Original maximum of {col}: {col_data.max()} and Original minimum of {col}: {col_data.min()}\n")
            
            qtl = col_data.quantile([lower, upper])
            
            # Replace values below the lower quantile
            col_data[col_data < qtl.loc[lower]] = qtl.loc[lower]
            
            # Replace values above the upper quantile
            col_data[col_data > qtl.loc[upper]] = qtl.loc[upper]
            
            data[col] = col_data
            
            print(f"New maximum of {col}: {col_data.max()} and New minimum of {col}: {col_data.min()}\n")
    
    return data

# missing data 
## I recommend to see 

# missing value report
def report_nan_counts_per_col(data, visualize=False):
    """
    Reports and returns the number of NaN values in each column of the given DataFrame.
    
    Parameters:
    data (pd.DataFrame): The data to be checked for NaN values.
    visualize (bool): Whether to visualize the NaN counts. Defaults to False.
    
    Returns:
        pd.DataFrame: A dataframe with the count of NaN values for each column.
    """
    nan_counts = data.isna().sum()
    
    nan_report = pd.DataFrame({
        'NaN Count': nan_counts
    })
    
    print("NaN values report:")
    for col, count in nan_counts.items():
        print(f"Column: {col}, NaN count: {count}")
    
    if visualize:
        plt.figure(figsize=(12, 8))
        plt.bar(nan_report.index, nan_report['NaN Count'], color='tab:blue', alpha=0.6)
        plt.xlabel('Columns')
        plt.ylabel('NaN Count')
        plt.title('NaN Counts by Column')
        plt.xticks(rotation=45)
        plt.tight_layout()  # Ensure everything fits without overlap
        plt.show()
    
    return nan_report

## Drop columns with high missing values
def drop_col_with_high_nan(data, threshold=0.3, drop_col=False):
    """
    Drops columns from the DataFrame where the percentage of NaN values exceeds the threshold.
    
    Parameters:
    data (pd.DataFrame): The data to be processed.
    threshold (float): The percentage threshold for dropping columns. Defaults to 0.3 (30%).
    drop_col (bool): Whether to return the dropped columns. Defaults to False.
    
    Returns:
        pd.DataFrame: The DataFrame with columns dropped based on the NaN threshold.
        (optional) pd.DataFrame: The DataFrame with the dropped columns if return_dropped is True.
    """
    total_counts = data.shape[0]
    nan_counts = data.isna().sum()
    nan_percentages = nan_counts / total_counts
    
    columns_to_drop = nan_percentages[nan_percentages > threshold].index
    cleaned_data = data.drop(columns=columns_to_drop)
    
    print(f"Columns dropped (NaN percentage > {threshold * 100}%): {list(columns_to_drop)}")
    
    if drop_col:
        return cleaned_data, [columns_to_drop]
    
    return cleaned_data

## report nan counts per row
def report_nan_counts_per_row(data, visualize=False):
    """
    Reports and returns the number and percentage of NaN values in each row of the given DataFrame.
    
    Parameters:
    data (pd.DataFrame): The data to be checked for NaN values.
    visualize (bool): Whether to visualize the NaN counts. Defaults to False.
    
    Returns:
        pd.DataFrame: A dataframe with the count and percentage of NaN values for each row.
    """
    nan_counts = data.isna().sum(axis=1)
    total_columns = data.shape[1]
    nan_percentages = (nan_counts / total_columns) * 100
    
    nan_report = pd.DataFrame({
        'NaN Count': nan_counts,
        'NaN Percentage': nan_percentages
    })
    
    print("NaN values report per row:")
    for idx, row in nan_report.iterrows():
        print(f"Row: {idx}, NaN count: {row['NaN Count']}, NaN percentage: {row['NaN Percentage']:.2f}%")
    
    if visualize:
        plt.figure(figsize=(12, 8))
        plt.bar(nan_report.index, nan_report['NaN Count'], color='tab:blue', alpha=0.6)
        plt.xlabel('Rows')
        plt.ylabel('NaN Count')
        plt.title('NaN Counts by Row')
        plt.xticks(rotation=45)
        plt.tight_layout()  # Ensure everything fits without overlap
        plt.show()
    
    return nan_report


# Penny stock filter
## By price
def remove_penny_stocks(data, price_column, action='remove'):
    """
    Removes or replaces with NaN the rows where the stock price is less than 5 dollars.
    
    Parameters:
    data (pd.DataFrame): The input DataFrame.
    price_column (str): The column name that contains the stock prices.
    action (str): The action to take on penny stocks ('remove' or 'nan'). Defaults to 'remove'.
    
    Returns:
        pd.DataFrame: The DataFrame with penny stocks removed or replaced with NaN.
    """
    if action not in ['remove', 'nan']:
        raise ValueError("Action must be either 'remove' or 'nan'")
    
    if action == 'remove':
        # Remove rows where the stock price is less than 5 dollars
        data = data[data[price_column] >= 5]
    elif action == 'nan':
        # Replace stock prices less than 5 dollars with NaN
        data.loc[data[price_column] < 5, :] = np.nan
    
    return data

## By market capitalization
def filter_firm_by_size(data, date_column='date', size_column='size', threshold=0.05, show_thresholds=False):
    """
    Filters out companies from the DataFrame where the 'size' value is in the bottom 5% for each date.
    
    Parameters:
    data (pd.DataFrame): The data to be processed.
    date_column (str): The column name representing the dates. Defaults to 'date'.
    size_column (str): The column name representing the size. Defaults to 'size'.
    threshold (float): The proportion threshold for filtering. Defaults to 0.05 (bottom 5%).
    show_thresholds (bool): Whether to print the threshold values for each date. Defaults to False.
    
    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    data[date_column] = pd.to_datetime(data[date_column])
    
    # Calculate the threshold value for the bottom 5% for each date
    size_thresholds = data.groupby(date_column)[size_column].transform(lambda x: x.quantile(threshold))
    
    if show_thresholds:
        threshold_values = data.groupby(date_column)[size_column].quantile(threshold)
        print("Threshold values for each date:")
        print(threshold_values)
    
    # Filter out companies with size value less than the threshold
    filtered_data = data[data[size_column] >= size_thresholds]
    
    return filtered_data

## report nan counts per id and year
### I don't recommend to use this function. It is not useful.
def report_nan_counts_per_id_and_year(data, id_column, date_column, visualize=False):
    """
    Reports and returns the number and percentage of NaN values per ID and year in the given DataFrame.
    
    Parameters:
    data (pd.DataFrame): The data to be checked for NaN values.
    id_column (str): The column name representing the IDs.
    date_column (str): The column name representing the dates.
    visualize (bool): Whether to visualize the NaN counts. Defaults to False.
    
    Returns:
        pd.DataFrame: A dataframe with the count and percentage of NaN values per ID and year.
    """
    data[date_column] = pd.to_datetime(data[date_column])
    data['Year'] = data[date_column].dt.year
    
    grouped = data.groupby([id_column, 'Year'])
    nan_counts = grouped.apply(lambda x: x.isna().sum().sum())
    total_counts = grouped.size() * data.shape[1]
    nan_percentages = (nan_counts / total_counts) * 100
    
    nan_report = pd.DataFrame({
        'NaN Count': nan_counts,
        'NaN Percentage': nan_percentages
    }).reset_index()
    
    print("NaN values report per ID and year:")
    for idx, row in nan_report.iterrows():
        print(f"ID: {row[id_column]}, Year: {row['Year']}, NaN count: {row['NaN Count']}, NaN percentage: {row['NaN Percentage']:.2f}%")
    
    if visualize:
        # Summarize the NaN counts for better visualization
        summary = nan_report.groupby('Year')['NaN Count'].sum().reset_index()
        plt.figure(figsize=(12, 8))
        plt.bar(summary['Year'], summary['NaN Count'], color='tab:blue', alpha=0.6)
        plt.xlabel('Year')
        plt.ylabel('Total NaN Count')
        plt.title('Total NaN Counts by Year')
        plt.xticks(rotation=45)
        plt.tight_layout()  # Ensure everything fits without overlap
        plt.show()
    
    return nan_report

## clean data with high nan
def clean_data_with_high_nan(data, id_col, col_threshold=0.3, row_threshold=0.3, return_dropped_cols=False, return_dropped_rows=False):
    """
    Cleans the DataFrame by dropping columns and rows where the percentage of NaN values exceeds the thresholds.
    
    Parameters:
    data (pd.DataFrame): The data to be processed.
    id_col (str): The name of the column that represents the id.
    col_threshold (float): The percentage threshold for dropping columns. Defaults to 0.3 (30%).
    row_threshold (float): The percentage threshold for dropping rows. Defaults to 0.3 (30%).
    return_dropped_cols (bool): Whether to return the dropped columns. Defaults to False.
    return_dropped_rows (bool): Whether to return the dropped rows. Defaults to False.
    
    Returns:
        pd.DataFrame: The cleaned DataFrame.
        (optional) list: The list of dropped columns if return_dropped is True.
        (optional) list: The list of dropped ids if return_dropped is True.
    """
    # Drop columns with high NaN values
    total_counts = data.shape[0]
    nan_counts = data.isna().sum()
    nan_percentages = nan_counts / total_counts
    
    columns_to_drop = nan_percentages[nan_percentages > col_threshold].index
    cleaned_data = data.drop(columns=columns_to_drop)
    
    print(f"Columns dropped (NaN percentage > {col_threshold * 100}%): {list(columns_to_drop)}")
    
    # Track dropped ids
    dropped_ids = set()

    # Drop rows with high NaN values for each id group
    def filter_group(group):
        total_counts = group.shape[1]
        nan_counts = group.isna().sum(axis=1)
        nan_percentages = nan_counts / total_counts
        drop_rows = nan_percentages > row_threshold
        dropped_ids.update(group[drop_rows][id_col].tolist())
        return group[~drop_rows]
    
    cleaned_data = cleaned_data.groupby(id_col).apply(filter_group).reset_index(drop=True)
    
    if return_dropped_cols:
        if return_dropped_rows:
            return cleaned_data, list(columns_to_drop), list(dropped_ids)
        else:
            return cleaned_data, list(columns_to_drop)
    
    
    return cleaned_data