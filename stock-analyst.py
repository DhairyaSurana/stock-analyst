# # stock-analyst.py

from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options  
from yahooquery import Ticker
from statistics import mean
import sys
import re
import requests
import time

def getData(attr):

    data = soup.find(text=re.compile(attr)).find_next('div').contents[0].strip()
    return data

if __name__=="__main__":

    ticker_list = ["AAPL", "TSLA", "ZNGA", "CCLP"]
    dur_list = []

    for ticker in ticker_list:

        start_time = time.time()

        #url = f"https://www.morningstar.com/stocks/xnas/{ticker}/financials"
        url = f"https://www.morningstar.com/stocks/xnas/{ticker.lower()}/quote"

        r = requests.get(url)

        try:
            r.raise_for_status()
        except Exception as e:
            raise SystemExit(e)

        chrome_options = Options()  
        chrome_options.add_argument("--headless")   # Allows web access without opening browser
        chrome_options.add_argument('--log-level=3') # Prevents headless chrome-related console messages from printing
        browser = webdriver.Chrome(options=chrome_options)

        browser.get(url)

        soup = BeautifulSoup(browser.page_source,'lxml')

        price = soup.find('div', {'id':'message-box-price'})
        price2 = price.text.strip()
    

        url = f"https://www.morningstar.com/stocks/xnas/{ticker}/financials"
        browser.get(url)
        soup = BeautifulSoup(browser.page_source,'lxml')

        company = Ticker(ticker)
        
        #print("Price: ", company.financial_data[ticker]['currentPrice'])
        print("Company: ", ticker)
        print("     Price: ", price2)
        print("     P/E: ", getData("Price/Earnings"))
        print("     Debt/Equity: ", getData("Debt/Equity"))
        print("     ROIC: ", getData("Invested Capital %"))

        duration = round(time.time() - start_time, 2) 
        dur_list.append(duration)

        print()

    print("Avg Runtime: ", mean(dur_list), " s")
    browser.close()   