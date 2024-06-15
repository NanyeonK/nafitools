import pandas as pd 
import numpy as np

import wrds
import statsmodels.api as sm
from scipy.stats import skew, kurtosis, pearsonr, spearmanr
from tabulate import tabulate

db = wrds.Connection() # Connect to WRDS

"""
We splite the data sample along two dimension: Stock exchnge and Sector.   

 Decomposing by Stock Exchange
 EXCHCD is the exchange code   
     1 = NYSE   
     2 = AMEX   
     3 = NASDAQ   
     4 = ARCA   
     
     10 = Boston Stock Exchange   
     13 = Chicago stock Exxchange   
     16 = Pacific Stock Exchange   
     17 = Philadelphia Stock Exchange   
     19 = Toronto Stock Exchange   
     20 = OTC   
     
     -2 = delisted   
     -1 = suspended   
     0 = not NYSE, AMEX, or NASDAQ   
"""

# Before 1963 July, CRSP doesn't contain AMEX.   
# 1972 Nov, Nasdaq added at CRSP but NASDAQ stock appears in January 1969.