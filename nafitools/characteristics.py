import numpy as np
import pandas as pd

class accounting_variables:
    
    def ac_sale(self):
        """Sales
        Compustat: SALE, (REVT)
        Description: SALE
        Group: Income Statement
            
        sale = SALE (or REVT if SALE is missing)
        """

        fa = self.data
        
        if fa.sale == None:
            return fa.revt 
        else:
            return fa.sale
    
    def ac_cogs(self):
        """Cost of Goods Sold
        Compustat: COGS
        Description: Cost of Goods Sold
        Group: Income Statement
        
        cogs = COGS
        """
        
        fa = self.data
        
        return fa.cogs
    
    def ac_gp(self):
        """Gross Profit
        Compustat: SALE, COGS
        Description: Gross Profit
        Group: Income Statement
        
        gp = sale - cogs
        """
        
        fa = self.data
        
        return fa.sale - fa.cogs
    
    def ac_xsga(self):
        """Selling, General, and Administrative Expenses
        Compustat: XSGA
        Description: 
        Group: Income Statement
        
        xsga = XSGA
        """
        
        fa = self.data
        
        return fa.xsga
    
    def ac_xad(self):
        """Advertising Expenses
        Compustat: XAD
        Description: Advertising Expenses
        Group: Income Statement
        
        xda = XAD
        * not available in GLOBAL
        """
        
        fa = self.data
        
        return fa.xad
    
    def ac_xrd(self):
        """Research and Development Expenses
        Compustat: XRD
        Description: Research and Development Expenses
        Group: Income Statement
        
        xrd = XRD
        * not available in GLOBAL
        """
        
        fa = self.data
        
        return fa.xrd
    
    def ac_xlr(self):
        """Staff Expenses
        Compustat: XLR
        Description: 
        Group: Income Statement
        
        xlr = XLR
        """
        
        fa = self.data
        
        return fa.xlr
    
    def ac_spi(self):
        """Special Items
        Compustat: SPI
        Despcription: Special Items
        Group: Income Statement
        
        spi = SPI
        """
        
        fa = self.data
        
        return fa.spi
    
    def ac_xopr(self):
        """
        """
        
        fa = self.data
        
        if fa.xopr == None:
            return ac_cogs(self) + fa.xsga
        
        return fa.xopr
    
    def ac_ebitda(self):
        """
        """
        
        fa = self.data
        
        if fa.ebitda == None:
            if fa.oibdp == None:
                return ac_sale(self) - ac_opex(self)
        
        return fa.ebitda
    
    def ac_dp(self):
        """
        """
        
        fa = self.data
        
        return fa.dp
    
    def ac_ebit(self):
        """
        """
        
        fa = self.data
        
        if fa.ebit == None:
            if fa.oibdp == None:
                return ac_sale(self) - ac_opex(self)
            return fa.OIADP
        
        
        return fa.ebit
    
    def ac_int(self):
        """
        """
        
        fa = self.data
        
        return fa.xint
    
    def ac_op(self):
        """
        """
        
        fa = self.data
        
        ebitda = ac_ebitda(self)
        xrd = ac_xrd(self)
        
        return ebitda + xrd
    
    def ac_ope(self):
        """
        Fama and French (2015)
        """
        
        fa = self.data
        
        ebitda = ac_ebitda(self)
        xint = ac_int(self)
        
        return ebitda - xint
    
    def ac_pi(self):
        """
        """
        
        fa = self.data
        
        if fa.pi == None:
            return ac_ebit(self) - ac_int(self) + ac_spi(self) + fa.nopi
        else: 
            return fa.pi
    
    def ac_tax(self):
        """
        """
        
        fa = self.data
        
        return fa.tax
    
    def ac_xido(self):
        """
        """
        
        fa = self.data
        
        return fa.xido
    
    def ac_ni(self):
        """
        """
        
        fa = self.data
        
        return fa.ib
    
    def ac_nix(self):
        """
        """
        
        fa = self.data
        
        return fa.nix
    
    
    
    
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