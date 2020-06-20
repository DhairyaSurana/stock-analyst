# # stock-analyst.py

from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
from yahooquery import Ticker
from statistics import mean
import sys
import re
import requests
import time

# def getURL(browser, ticker):

#     browser.find_element_by_class_name("mdc-site-search__form").send_keys(ticker)
#     return browser.current_url

def getData(attr):

    data = soup.find(text=re.compile(attr)).find_next('div').contents[0].strip()
    return data

if __name__=="__main__":

    ticker_list = ["PCRFY", "MSFT", "AMZN", "AAPL", "TSLA", "ZNGA", "CCLP"]
    dur_list = []

    chrome_options = Options()  
    #chrome_options.add_argument("--headless")   # Allows web access without opening browser
    #chrome_options.add_argument('--window-size=1920x1080')
    #chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--log-level=3') # Prevents headless chrome-related console messages from printing
    browser = webdriver.Chrome(options=chrome_options)

    url = f"https://www.morningstar.com/stocks"
    browser.get(url)

    for ticker in ticker_list:

        start_time = time.time()

        # Enter ticker symbol in search bar        
        browser.find_element_by_tag_name("input").send_keys(ticker)
        time.sleep(2)
        browser.find_element_by_tag_name("input").send_keys(Keys.RETURN)

        time.sleep(5)
        soup = BeautifulSoup(browser.page_source,'lxml')

        # Try to find the price, if not, try again    
        price = soup.find('div', {'id':'message-box-price'})
        #price = browser.find_element_by_id('message-box-price')
        price2 = price.text.strip()
            

    
        # Click on 'Financials' tab
        browser.find_element_by_link_text("Financials").send_keys(Keys.RETURN)
        time.sleep(2)
        soup = BeautifulSoup(browser.page_source,'lxml')

        company = Ticker(ticker)
        
        print("Company: ", ticker)
        #print("    Price: ", company.financial_data[ticker]['currentPrice'])
        print("     Price: ", price2)
        print("     P/E: ", getData("Price/Earnings"))
        print("     Debt/Equity: ", getData("Debt/Equity"))
        print("     ROIC: ", getData("Invested Capital %"))

        duration = round(time.time() - start_time, 2) 
        dur_list.append(duration)

        print()

    print("Avg Runtime: ", mean(dur_list), " s")
    browser.close()   