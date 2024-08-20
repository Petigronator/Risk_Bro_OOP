#SM_GraphDisplay.py

import yfinance as YahooFinance
from matplotlib import pyplot as Pyplot
import os

class SM_GraphDisplay:
    def __init__(self, security_symbol, start_date, end_date, save_path ='Graph_Photo_Generator/graph.png'):
        super().__init__()
        self.security_symbol = security_symbol
        self.start_date = start_date
        self.end_date = end_date
        self.save_path = save_path

    def fetch_price_data(self):
        """Fetch security price data using yfinance."""
        data = YahooFinance.download(self.security_symbol, start=self.start_date, end=self.end_date)
        return data['Adj Close']

    def plot_adjusted_close(self):
        """Plot the adjusted closing prices for the security."""
        prices = self.fetch_price_data()
        Pyplot.figure(figsize=(10, 5))
        prices.plot(title=f"Adjusted Close Prices for {self.security_symbol} between {self.start_date} and {self.end_date}")
        Pyplot.xlabel('Date')
        Pyplot.ylabel('Adjusted Close Price')
        Pyplot.grid(True)
        Pyplot.savefig(self.save_path)
        Pyplot.show()
        return self.save_path
