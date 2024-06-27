import pandas as pd
import numpy as np

class UnivariatePortfolioAnalyzer:
    def __init__(self, df, time_column, id_column):
        """
        Initialize the UnivariatePortfolioAnalyzer with the data frame, time column, and ID column.
        
        Args:
            df (pd.DataFrame): The data frame containing the data.
            time_column (str): The name of the column representing time periods.
            id_column (str): The name of the column representing unique entity IDs.
        """
        self.df = df
        self.time_column = time_column
        self.id_column = id_column

    def cal_bp(self, value_column, num_portfolios, custom_percentiles=None):
        """
        Calculate breakpoints for a given variable based on specified quantiles for univariate portfolio analysis.
        
        Args:
            value_column (str): The name of the column representing the values to calculate breakpoints for.
            num_portfolios (int): The number of portfolios to be formed each time period.
            custom_percentiles (list of float, optional): Custom percentiles to calculate breakpoints. If None, evenly spaced percentiles are used.
        
        Returns:
            pd.DataFrame: A data frame containing the breakpoints for each time period.
        """
        if custom_percentiles:
            assert all(0 < p < 100 for p in custom_percentiles), "Percentiles must be between 0 and 100"
            percentiles = custom_percentiles
        else:
            percentiles = [k * 100 / num_portfolios for k in range(1, num_portfolios)]
        
        quantiles = [p / 100 for p in percentiles]
        breakpoints = self.df.groupby(self.time_column)[value_column].quantile(quantiles).unstack()
        breakpoints.columns = [f'B{k+1} ({round(percentiles[k], 3)})' for k in range(len(percentiles))]
        return breakpoints

    def cal_multi_bp(self, characteristics, num_portfolios=5, custom_percentiles=None):
        """
        Calculate breakpoints for multiple characteristics in the dataset using the cal_bp function.

        Parameters:
        - characteristics (list of str): List of column names of the firm characteristics to calculate breakpoints for.
        - num_portfolios (int): The number of portfolios to calculate. Default is 5.
        - custom_percentiles (list of float): Custom percentiles for breakpoints. Should be between 0 and 100.

        Returns:
        - breakpoints_dict (dict): A dictionary where keys are characteristic names and values are DataFrames with dates as index and breakpoints as columns.
        """
        breakpoints_dict = {}
        
        for characteristic in characteristics:
            breakpoints_dict[characteristic] = self.cal_bp(characteristic, num_portfolios, custom_percentiles)

        return breakpoints_dict

    @staticmethod
    def modify_bp(breakpoints):
        """
        Modify breakpoints to ensure there are no duplicate edges and they are monotonically increasing.
        
        Args:
            breakpoints (pd.Series): A series of breakpoints for a single time period.
        
        Returns:
            pd.Series: Modified breakpoints with no duplicates and are monotonically increasing.
        """
        unique_breakpoints = breakpoints.drop_duplicates()
        while len(unique_breakpoints) < len(breakpoints):
            breakpoints += np.random.uniform(0, 1e-10, size=breakpoints.shape)
            unique_breakpoints = breakpoints.drop_duplicates()
        # Ensure breakpoints are monotonically increasing
        return np.sort(breakpoints)

    def assign_portfolios(self, breakpoints, value_column, keep_columns=None, method='drop'):
        """
        Assign portfolios based on calculated breakpoints.

        Args:
            breakpoints (pd.DataFrame): The data frame containing the breakpoints for each time period.
            value_column (str): The name of the column representing the values to assign to portfolios.
            keep_columns (list of str, optional): List of column names to keep in the resulting DataFrame. If None, only time_column, value_column, and portfolio are kept.
            method (str): Method to handle duplicate breakpoints. 'drop' to drop duplicates, 'modify' to add small random values.
        
        Returns:
            pd.DataFrame: The data frame with the specified columns and an additional column for portfolio assignment.
        """
        if keep_columns is None:
            keep_columns = []

        df = self.df[[self.id_column, self.time_column, value_column] + keep_columns].copy()

        # Remove rows with NaN values in the value column
        df = df.dropna(subset=[value_column])

        # Check for and handle duplicate index labels
        if df.index.duplicated().any():
            df = df.reset_index(drop=True)
        
        df['portfolio'] = np.nan

        for time_period in breakpoints.index:
            period_data = df[df[self.time_column] == time_period]
            period_breakpoints = breakpoints.loc[time_period].dropna().values
            
            if method == 'drop':
                period_breakpoints = np.unique(period_breakpoints)
            elif method == 'modify':
                period_breakpoints = self.modify_bp(period_breakpoints)
            
            # Ensure breakpoints are monotonically increasing
            period_breakpoints = np.sort(period_breakpoints)

            if not np.all(np.diff(period_breakpoints) > 0):
                print(f"Warning: Non-monotonic breakpoints detected for period {time_period}.")
                continue
            
            portfolios = pd.cut(
                period_data[value_column],
                bins=[-np.inf] + period_breakpoints.tolist() + [np.inf],
                labels=[f'P{k+1}' for k in range(len(period_breakpoints) + 1)],
                include_lowest=True
            )
            df.loc[period_data.index, 'portfolio'] = portfolios

        return df[[self.id_column, self.time_column, value_column] + keep_columns + ['portfolio']]

    def number_of_stocks_per_portfolio(self, portfolio_column):
        """
        Calculate the number of stocks in each portfolio per time period.

        Args:
            portfolio_column (str): The name of the column representing portfolio assignments.
        
        Returns:
            pd.DataFrame: A data frame containing the number of stocks in each portfolio for each time period.
        """
        return self.df.groupby([self.time_column, portfolio_column]).size().unstack(fill_value=0)

    def cal_port_value(self, portfolio_column, value_column, weight_column=None):
        """
        Calculate average values for each portfolio and the difference between the highest and lowest portfolios.

        Args:
            portfolio_column (str): The name of the column representing portfolio assignments.
            value_column (str): The name of the column representing the values to average.
            weight_column (str, optional): The name of the column representing the weights. If None, equal weights are used.

        Returns:
            pd.DataFrame: A data frame with the average values for each portfolio and the difference between the highest and lowest portfolios for each time period.
        """
        if weight_column is None:
            self.df['weight'] = 1
        else:
            self.df['weight'] = self.df[weight_column]

        self.df['weighted_value'] = self.df[value_column] * self.df['weight']
        avg_values = self.df.groupby([self.time_column, portfolio_column]).apply(lambda x: x['weighted_value'].sum() / x['weight'].sum()).reset_index(name=f'avg_{value_column}')

        # Calculate the difference between the highest and lowest portfolios for each time period
        high_portfolio = f'P{self.df[portfolio_column].nunique()}'
        low_portfolio = 'P1'
        
        diff_values = avg_values.pivot(index=self.time_column, columns=portfolio_column, values=f'avg_{value_column}')
        diff_values['diff'] = diff_values[high_portfolio] - diff_values[low_portfolio]
        
        return avg_values, diff_values[['diff']].reset_index()

    def calculate_average_portfolio_values(self, portfolio_column, value_column, weight_column=None):
        """
        Calculate average values for each portfolio and the difference between the highest and lowest portfolios.

        Args:
            portfolio_column (str): The name of the column representing portfolio assignments.
            value_column (str): The name of the column representing the values to average.
            weight_column (str, optional): The name of the column representing the weights. If None, equal weights are used.

        Returns:
            pd.DataFrame: A data frame with the average values for each portfolio and the difference between the highest and lowest portfolios for each time period.
        """
        if weight_column is None:
            self.df['weight'] = 1
        else:
            self.df['weight'] = self.df[weight_column]

        self.df['weighted_value'] = self.df[value_column] * self.df['weight']
        avg_values = self.df.groupby([self.time_column, portfolio_column]).apply(lambda x: x['weighted_value'].sum() / x['weight'].sum()).reset_index(name=f'avg_{value_column}')

        # Pivot the average values to get portfolios as columns
        pivot_avg_values = avg_values.pivot(index=self.time_column, columns=portfolio_column, values=f'avg_{value_column}')
        
        # Calculate the difference between the highest and lowest portfolios for each time period
        high_portfolio = pivot_avg_values.columns[-1]
        low_portfolio = pivot_avg_values.columns[0]
        pivot_avg_values['diff'] = pivot_avg_values[high_portfolio] - pivot_avg_values[low_portfolio]
        
        # Rename columns to match the required format
        pivot_avg_values.columns = [f'P{k+1}' for k in range(len(pivot_avg_values.columns) - 1)] + ['diff']
        
        return pivot_avg_values.reset_index()

    def calculate_portfolio_returns(self, portfolio_column, return_column, weight_column=None):
        """
        Calculate average returns for each portfolio and the difference between the highest and lowest portfolios.

        Args:
            portfolio_column (str): The name of the column representing portfolio assignments.
            return_column (str): The name of the column representing the returns to average.
            weight_column (str, optional): The name of the column representing the weights. If None, equal weights are used.

        Returns:
            pd.DataFrame: A data frame with the average returns for each portfolio and the difference between the highest and lowest portfolios for each time period.
        """
        if weight_column is None:
            self.df['weight'] = 1
        else:
            self.df['weight'] = self.df[weight_column]

        self.df['weighted_return'] = self.df[return_column] * self.df['weight']
        avg_returns = self.df.groupby([self.time_column, portfolio_column]).apply(lambda x: x['weighted_return'].sum() / x['weight'].sum()).reset_index(name=f'avg_{return_column}')

        # Pivot the average returns to get portfolios as columns
        pivot_avg_returns = avg_returns.pivot(index=self.time_column, columns=portfolio_column, values=f'avg_{return_column}')
        
        # Calculate the difference between the highest and lowest portfolios for each time period
        high_portfolio = pivot_avg_returns.columns[-1]
        low_portfolio = pivot_avg_returns.columns[0]
        pivot_avg_returns['diff'] = pivot_avg_returns[high_portfolio] - pivot_avg_returns[low_portfolio]
        
        # Rename columns to match the required format
        pivot_avg_returns.columns = [f'P{k+1}' for k in range(len(pivot_avg_returns.columns) - 1)] + ['diff']
        
        return pivot_avg_returns.reset_index()

    def summarize_results(self, avg_values):
        """
        Summarize the results by calculating the time-series means of the period average values of the outcome variable for each portfolio and the difference portfolio.

        Args:
            avg_values (pd.DataFrame): Data frame containing the average values for each portfolio and the difference.

        Returns:
            pd.DataFrame: A data frame with the time-series means of the period average values of the outcome variable for each portfolio and the difference portfolio.
        """
        summary = avg_values.mean().to_frame(name='mean').T
        summary[self.time_column] = 'Mean'
        return summary
