#SM_StdCalculator.py

import yfinance as YahooFinance
import pandas as Pandas

class SM_StdCalculator:
    def __init__(self, security_symbol, start_date, end_date):
        super().__init__()
        self.security_symbol = security_symbol
        self.start_date = start_date
        self.end_date = end_date

    def fetch_price_data(self, security_symbol, start_date, end_date):
        """Fetch security price data using yfinance."""
        data = YahooFinance.download(security_symbol, start=start_date, end=end_date)
        return data['Adj Close']  # Return adjusted close prices

    def calculate_std(self, security_symbol, start_date, end_date):
        """Calculate the standard deviation of the security's price over the given period."""
        prices = self.fetch_price_data(security_symbol, start_date, end_date)
        std_dev = prices.std()
        return std_dev
