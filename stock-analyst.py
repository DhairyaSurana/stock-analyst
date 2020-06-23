# # stock-analyst.py

from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from yahooquery import Ticker
from statistics import mean
import sys
import re
import time
import os


def getTextData(soup, attr):

    try:
        label = soup.find(text=re.compile(attr))
        data = label.find_next('div').contents[0].strip() 

    except Exception:
        return None

    return data

if __name__=="__main__":

    ticker_list = ["PCRFY", "MSFT", "AMZN", "AAPL", "TSLA", "ZNGA", "CCLP"]
    dur_list = []

    try:
    
        chrome_options = Options()  
        chrome_options.add_argument("--headless")   # Allows web access without opening browser
        chrome_options.add_argument('--window-size=1920x1080')  # Allows certain elements to be reachable when headless chrome is enabled
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) # Gets rid of official Selenium connection messages
        chrome_options.add_argument('--log-level=3') # Disables chrome-related console messages
        browser = webdriver.Chrome(options=chrome_options)

        url = "https://www.morningstar.com/stocks"
        browser.get(url)

        for ticker in ticker_list:

            start_time = time.time()

            company = Ticker(ticker)
            fin_data = company.financial_data[ticker]

            # Enter ticker symbol in search bar  
            # Repeat process if correct url is not loaded
            conn_attempt = 0
            while "quote" not in browser.current_url:       

                browser.find_element_by_tag_name("input").send_keys(ticker)
                time.sleep(1)
                browser.find_element_by_tag_name("input").send_keys(Keys.RETURN)
                time.sleep(2)

                conn_attempt+=1
            
            print("Connection Attempts: ", conn_attempt)
            
            # Get Finance URL
            fin_url = browser.current_url.replace("quote", "financials")
            browser.get(fin_url)
            browser.implicitly_wait(5)
            print("URL: ", browser.current_url)
            
            # Create Soup object
            soup_cnt = 1
            soup = BeautifulSoup(browser.page_source,'lxml')
            while soup.find(text=re.compile("Price/Earnings")) is None:
                soup = BeautifulSoup(browser.page_source,'lxml')
                soup_cnt+=1

            print("Soup Attempts: ", soup_cnt)

            # Get Company Stats:
            pe_ratio = getTextData(soup, "Price/Earnings")
            roic = getTextData(soup, "Invested Capital %")

            # Print Company Stats
            print("Company: ", ticker)
            print("     Price: ", fin_data["currentPrice"])
            print("     P/E: ", pe_ratio)
            print("     Debt/Equity: ", round(fin_data["debtToEquity"]/100, 2))
            print("     ROIC: ", roic, end="\n\n")

            # Calculate runtime for current iteration (stock)
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
    