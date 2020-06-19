# # stock-analyst.py

from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options  
import sys
import re
import requests


def getData(attr):

    data = soup.find(text=re.compile(attr)).find_next('div').contents[0].strip()
    return data

if __name__=="__main__":

    ticker = sys.argv[1]
    url = f"https://www.morningstar.com/stocks/xnas/{ticker}/quote"

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
    
    print("Price: ", price2)
    print("P/E: ", getData("Price/Earnings"))
    print("Debt/Equity: ", getData("Debt/Equity"))
    print("ROIC: ", getData("Invested Capital %"))

    browser.close()   