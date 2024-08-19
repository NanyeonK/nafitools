import pandas as pd 
import numpy as np
import wrds


 # Connect to WRDS

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

 Shrcd is the share code
     1st digit
     1 = Ordinary Common Shares
     
"""

# Before 1963 July, CRSP doesn't contain AMEX.   
# 1972 Nov, Nasdaq added at CRSP but NASDAQ stock appears in January 1969.

# Using JKP data.
    
class wrdsdata:
    def __init__(self):
        self.db = wrds.Connection()
        
    def get_jkp(self, country, sdate, edate, obs_main=1, common=1, primary_sec=1, exch_main=1, order_by_1='date', order_by_2='gvkey'):
        """
        Get the data from JKP database.
        
        
        """
        # SQL query to get the data
        query = f"""SELECT *
                    FROM contrib_global_factor.global_factor
                    WHERE excntry = '{country}'
                    AND obs_main = {obs_main}
                    AND common = {common}
                    AND primary_sec = {primary_sec}
                    AND exch_main = {exch_main}
                    AND date BETWEEN '{sdate}' AND '{edate}'
                    ORDER BY {order_by_1}, {order_by_2}
                    """
        
        return self.db.raw_sql(query)
    
    def get_crsp_monthly(self, sdate, edate,):
        """
        """
        
        query = f"""SELECT *
                    FROM crsp.msf
                    WHERE date BETWEEN '{sdate}' AND '{edate}'
                    """
                    
        return self.db.raw_sql(query)
    
    def get_crsp_daily(self, sdate, edate):
        """
        """
        
        query = f"""SELECT *
                    FROM crsp.dsf
                    WHERE date BETWEEN '{sdate}' AND '{edate}'
                    """
                    
        return self.db.raw_sql(query)
    
    def get_compustat_annual(self, sdate, edate):
        """
        """
        
        # sale, revt, cogs, xsga, xad, xrd, xlr, spi, xopr, ebitda, dp, ebit, xint, pi, tax, xido, ib, ni, dvc, dvt, 
        # capx, prstkc, purtshr, sstk, dltis, dltr, dlcch, fincf
            
        query = f"""SELECT *
                    FROM comp.funda
                    WHERE datadate BETWEEN '{sdate}' AND '{edate}'
                    """
                    
        return self.db.raw_sql(query)
    
    def get_compustat_quarterly(self, sdate, edate):
        """
        """
        
        # ibq, saleq
    
        query = f"""SELECT *
                    FROM comp.fundq
                    WHERE datadate BETWEEN '{sdate}' AND '{edate}'
                    """
                    
        return self.db.raw_sql(query)

    def get_ff_daily(self, sdate, edate):
        """
        """
        
        query = f"""SELECT *
                    FROM ff.factors_daily
                    WHERE date BETWEEN '{sdate}' AND '{edate}'
                    """
                    
        return self.db.raw_sql(query)
    
    def get_ff_monthly(self, sdate, edate):
        """
        """
        
        query = f"""SELECT *
                    FROM ff.factors_monthly
                    WHERE date BETWEEN '{sdate}' AND '{edate}'
                    """
                    
        return self.db.raw_sql(query)


