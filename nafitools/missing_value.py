import pandas as pd
import numpy as np 

class fill_missing_value:
    def __init__(self):
        pass
    
    #############################
    #    Drop missing values    #
    #############################
    
    def drop_missing(self, df):
        return df.dropna()
    
    #############################
    #     Simple imputation     #
    #############################
    
    # Fill missing values with simple way
    def fill_mean(self, df):
        return df.fillna(df.mean())
    
    # Fill missing values with median
    def fill_median(self, df):
        return df.fillna(df.median())
    
    # Fill missing values with mode
    def fill_mode(self, df):
        return df.fillna(df.mode().iloc[0])
    
    # Fill missing values with zero
    def fill_zero(self, df):
        return df.fillna(0)
    
    # Fill missing values with forward fill
    def fill_ffill(self, df):
        return df.fillna(method='ffill')
    
    # Fill missing values with backward fill
    def fill_bfill(self, df):
        return df.fillna(method='bfill')
    
    #############################
    #  Statistical imputation   #
    #############################
    
    # Fill missing values with linear interpolation
    def fill_linear_interpolation(self, df):
        return df.interpolate(method='linear')
    
    # Fill missing values with polynomial interpolation
    def fill_polynomial_interpolation(self, df, degree=2):
        return df.interpolate(method='polynomial', order=degree)
    
    # Fill missing values with KNN imputation
    def fill_knn(self, df, k=3):
        from sklearn.impute import KNNImputer # KNNImputer is a class in sklearn.impute
        imputer = KNNImputer(n_neighbors=k)
        return pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
    
    # Fill missing values with spline interpolation
    def fill_spline_interpolation(self, df):
        return df.interpolate(method='spline', order=2)
    
    # Fill missing values with time series interpolation
    def fill_time_series_interpolation(self, df):
        return df.interpolate(method='time')
    
    # Fill missing values with rolling mean
    def fill_rolling_mean(self, df, window=3):
        return df.fillna(df.rolling(window=window, min_periods=1).mean())
    
    # Fill missing values with rolling median
    def fill_rolling_median(self, df, window=3):
        return df.fillna(df.rolling(window=window, min_periods=1).median())
    
    # Fill missing values with rolling mode
    def fill_rolling_mode(self, df, window=3):
        return df.fillna(df.rolling(window=window, min_periods=1).apply(lambda x: x.mode().iloc[0]))
    
    # Fill missing values with rolling interpolation
    def fill_rolling_interpolation(self, df, window=3):
        return df.fillna(df.rolling(window=window, min_periods=1).apply(lambda x: x.interpolate(method='linear')))
    
    # Fill missing values with exponential moving average
    def fill_ewm_mean(self, df, span=3):
        return df.fillna(df.ewm(span=span, adjust=False).mean())
    
    # Fill missing values with exponential moving median
    def fill_ewm_median(self, df, span=3):
        return df.fillna(df.ewm(span=span, adjust=False).median())
    
    # Fill missing values with exponential moving mode
    def fill_ewm_mode(self, df, span=3):
        return df.fillna(df.ewm(span=span, adjust=False).apply(lambda x: x.mode().iloc[0]))
    
    # Fill missing values with exponential moving interpolation
    def fill_ewm_interpolation(self, df, span=3):
        return df.fillna(df.ewm(span=span, adjust=False).apply(lambda x: x.interpolate(method='linear')))
    
    # Fill missing values with seasonal decomposition
    def fill_seasonal_decomposition(self, df, freq=12):
        from statsmodels.tsa.seasonal import seasonal_decompose # seasonal_decompose is a class in statsmodels.tsa.seasonal
        decomp = seasonal_decompose(df, period=freq)
        return df.fillna(decomp.trend + decomp.seasonal)
    
    # Fill missing values with moving average
    def fill_moving_average(self, df, window=3):
        return df.fillna(df.rolling(window=window, min_periods=1).mean())
    
    # Fill missing values with moving median
    def fill_moving_median(self, df, window=3):
        return df.fillna(df.rolling(window=window, min_periods=1).median())
    
    # Fill missing values with moving mode
    def fill_moving_mode(self, df, window=3):
        return df.fillna(df.rolling(window=window, min_periods=1).apply(lambda x: x.mode().iloc[0]))
    
    # Fill missing values with moving interpolation
    def fill_moving_interpolation(self, df, window=3):
        return df.fillna(df.rolling(window=window, min_periods=1).apply(lambda x: x.interpolate(method='linear')))
    
    # Fill missing values with moving exponential moving average
    def fill_moving_ewm_mean(self, df, span=3):
        return df.fillna(df.ewm(span=span, adjust=False).mean())
    
    # Fill missing values with moving exponential moving median
    def fill_moving_ewm_median(self, df, span=3):
        return df.fillna(df.ewm(span=span, adjust=False).median())
    
    # Fill missing values with moving exponential moving mode
    def fill_moving_ewm_mode(self, df, span=3):
        return df.fillna(df.ewm(span=span, adjust=False).apply(lambda x: x.mode().iloc[0]))
    
    # Fill missing values with moving exponential moving interpolation
    def fill_moving_ewm_interpolation(self, df, span=3):
        return df.fillna(df.ewm(span=span, adjust=False).apply(lambda x: x.interpolate(method='linear')))
    
    #############################################
    # Fill missing values with domain knowledge #
    #############################################
    
    
    # Missing Data in Asset Pricing Panels
    # https://doi.org/10.7910/DVN/QR6PHI
    
    
    
    
    # Missing Financial Data
    # https://github.com/sven-lerner/missing_data_pub
    
    # Missing Values Handling for Machine Learning Portolfios
    # https://github.com/jack-mccoy/missing_data