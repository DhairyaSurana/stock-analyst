# # stock-analyst.py

from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
from yahooquery import Ticker
from statistics import mean
import sys
import re
import time
import os


def getData(soup, attr):

    data = soup.find(text=re.compile(attr)).find_next('div').contents[0].strip()
    return data

if __name__=="__main__":

    ticker_list = ["PCRFY", "MSFT", "AMZN", "AAPL", "TSLA", "ZNGA", "CCLP"]
    dur_list = []

    try:
    
        chrome_options = Options()  
        chrome_options.add_argument("--headless")   # Allows web access without opening browser
        chrome_options.add_argument('--window-size=1920x1080')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--log-level=3') # Prevents headless chrome-related console messages from printing
        browser = webdriver.Chrome(options=chrome_options)

        time.sleep(1)

        url = "https://www.morningstar.com/stocks"
        browser.get(url)

        for ticker in ticker_list:

            start_time = time.time()

            company = Ticker(ticker)
            fin_data = company.financial_data[ticker]

            # Enter ticker symbol in search bar        
            browser.find_element_by_tag_name("input").send_keys(ticker)
            time.sleep(1)
            browser.find_element_by_tag_name("input").send_keys(Keys.RETURN)

            time.sleep(2)
                
            # Click on 'Financials' tab
            browser.find_element_by_link_text("Financials").send_keys(Keys.RETURN)
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source,'lxml')

            # Print Company Stats
            print("Company: ", ticker)
            print("     Price: ", fin_data["currentPrice"])
            print("     P/E: ", getData(soup, "Price/Earnings"))
            print("     Debt/Equity: ", round(fin_data["debtToEquity"]/100, 2))
            print("     ROIC: ", getData(soup, "Invested Capital %"))
            print()

            duration = round(time.time() - start_time, 2) 
            dur_list.append(duration)

        print("Avg Runtime/stock: ", mean(dur_list), " s")
        browser.close()   
    
    except Exception as e:
        print(e)
        print()
        print("Quitting browser")
        os.system("taskkill /IM \"chrome.exe\" /F")

    except KeyboardInterrupt:
        print()
        print("Quitting browser")
        os.system("taskkill /IM \"chrome.exe\" /F")
    