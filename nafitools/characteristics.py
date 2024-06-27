import numpy as np
import pandas as pd

# characteristics
class characteristics:
    
    # Simple function to calculate the percentage change
    def c_at_gr1(self):
        """
        Asset Growth.
        Paper: Cooper, Gulen, and Schill (2008)
        
        Original Sample: 1968-2003
        Definition: The growth rate of total assets, scaled by the lagged total assets.
        Formula: (AT[t] / AT[t-12]) - 1
        Sign: -1
        Original significance: negative
        """
        fa = self.data
        char = self.pct_change(fa.at)
        return char
    
    def c_sale_gr1(self):
        """
        Sales Growth (12 months)
        Paper: Lakonishok, Shleifer, and Vishny (1994)
        
        Original sample: 1968-1988
        Definition: 
        Formula: (SALE[t] / SALE[t-12]) - 1
        Sign: -1
        Original significance: positive
        """
        
        fa = self.data
        char = self.pct_change(fa.sale)
        return char
    
    def c_sale_gr3(self):
        """
        Sales Growth (36 month)
        Paper: Lakonishok, Shleifer, and Vishny (1994)
        
        Original sample: 1968-1988
        Definition:
        Formula: (SALE[t] / SALE[t-36]) - 1
        Sign: -1
        Original significance: positive
        """
        
        fa = self.data
        char = self.pct_change(fa.sale, 36)
        return char
    
    def c_ca_gr1(self):
        """
        Short-term Debt Growth (36 months)
        
        """