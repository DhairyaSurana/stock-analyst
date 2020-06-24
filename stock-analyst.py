# # stock-analyst.py

from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
#from get_all_tickers import get_tickers as gt
from yahooquery import Ticker
from statistics import mean
import sys
import re
import time
import os
from multiprocessing import Pool, cpu_count


def initDriver():

    chrome_options = Options()  
    chrome_options.add_argument("--headless")   # Allows web access without opening browser
    chrome_options.add_argument('--window-size=1920x1080')  # Allows certain elements to be reachable when headless chrome is enabled
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) # Gets rid of official Selenium connection messages
    chrome_options.add_argument('--log-level=3') # Disables chrome-related console messages
    
    return  webdriver.Chrome(options=chrome_options)
browser = initDriver()
def getTextData(soup, attr):

    try:
        label = soup.find(text=re.compile(attr))
        data = label.find_next('div').contents[0].strip() 

    except Exception:
        return None

    return data

def getURLs(arr):

    url = "https://www.morningstar.com/stocks"
    browser.get(url)

    url_list = []
    for ticker in arr:

        while "quote" not in browser.current_url:       

            browser.find_element_by_tag_name("input").send_keys(ticker)
            time.sleep(1)
            browser.find_element_by_tag_name("input").send_keys(Keys.RETURN)
            time.sleep(2)

            fin_url = browser.current_url.replace("quote", "financials")
            url_list.append(fin_url)

    return url_list

def scrape(url):

    browser.get(url)
    browser.implicitly_wait(5)
    # WebDriverWait(browser, 5).until(
    #             EC.presence_of_element_located((By.CLASS_NAME, 'stock__content'))
    #         )
    
    # Create Soup object
    soup_cnt = 1
    soup = BeautifulSoup(browser.page_source,'lxml')
    while soup.find(text=re.compile("Price/Earnings")) is None:
        soup = BeautifulSoup(browser.page_source,'lxml')
        soup_cnt+=1

    # Get Company Stats:
    pe_ratio = getTextData(soup, "Price/Earnings")
    roic = getTextData(soup, "Invested Capital %")

def getCompInfo(ticker):

    company = Ticker(ticker)
    fin_data = company.financial_data[ticker]

    url = "https://www.morningstar.com/stocks"
    #browser = initDriver()
    browser.get(url)

    # Enter ticker symbol in search bar  
    # Repeat process if correct url is not loaded
    conn_attempt = 0
    while "quote" not in browser.current_url:       

        browser.find_element_by_tag_name("input").send_keys(ticker)
        time.sleep(1)
        browser.find_element_by_tag_name("input").send_keys(Keys.RETURN)
        time.sleep(2)

        conn_attempt+=1
    
    # Get Finance URL
    fin_url = browser.current_url.replace("quote", "financials")
    browser.get(fin_url)
    #browser.implicitly_wait(5)
    # WebDriverWait(browser, 5).until(
    #             EC.presence_of_element_located((By.CLASS_NAME, 'stock__content'))
    #         )
    
    # Create Soup object
    soup_cnt = 1
    soup = BeautifulSoup(browser.page_source,'lxml')
    while soup.find(text=re.compile("Price/Earnings")) is None:
        soup = BeautifulSoup(browser.page_source,'lxml')
        soup_cnt+=1

    # Get Company Stats:
    pe_ratio = getTextData(soup, "Price/Earnings")
    roic = getTextData(soup, "Invested Capital %")

    # Print Company Stats
    print("Connection Attempts: ", conn_attempt)
    print("URL: ", browser.current_url)
    print("Soup Attempts: ", soup_cnt)
    print("Company: ", ticker)
    print("     Price: ", fin_data["currentPrice"])
    print("     P/E: ", pe_ratio)
    print("     Debt/Equity: ", round(fin_data["debtToEquity"]/100, 2))
    print("     ROIC: ", roic, end="\n\n")

    # browser.close()

if __name__=="__main__":

    ticker_list = ["PCRFY", "MSFT", "AMZN", "AAPL", "TSLA", "ZNGA", "CCLP"]

    try:

        with Pool(cpu_count()) as p:
            list(p.imap(getCompInfo, ticker_list))
       
        p.close()
        p.join()
            
        print("Runtime: ", time.perf_counter(), " s", end="\n\n")   
    
    except Exception as e:
        print(e)
        print()
        print("Quitting browser")

    except KeyboardInterrupt:
        print()
        print("Quitting browser")

    finally:
        os.system("taskkill /IM \"chrome.exe\" /F")