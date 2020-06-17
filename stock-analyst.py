# stock-analyst.py

from yahooquery import Ticker
import pprint
from get_all_tickers import get_tickers as gt
import sys

if __name__ == "__main__":

    list_of_tickers = gt.get_tickers()
    limit = float(sys.argv[1])

    for ticker in list_of_tickers:
        company = Ticker(ticker)
        try:
            curr_price = company.financial_data[ticker]['currentPrice']
            if curr_price <= limit:
                print(ticker, ": $", curr_price)
        except Exception:
            print(ticker, " symbol not found")