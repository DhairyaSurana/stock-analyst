# # stock-analyst.py

from bs4 import BeautifulSoup
from selenium import webdriver 
import sys
import re
import requests


def getData(attr):

    data = soup.find(text=re.compile(attr)).find_next('div').contents[0].strip()
    return data

if __name__=="__main__":

    ticker = sys.argv[1]
    url = f"https://www.morningstar.com/stocks/xnas/{ticker}/quote"

    browser = webdriver.Chrome()
    browser.get(url)

    soup = BeautifulSoup(browser.page_source,'lxml')

    price = soup.find('div', {'id':'message-box-price'})
    price2 = price.text.strip()
    print("Price: ", price2)

    url = f"https://www.morningstar.com/stocks/xnas/{ticker}/financials"
    browser.get(url)
    soup = BeautifulSoup(browser.page_source,'lxml')
    
    pe_ratio = getData("Price/Earnings")
    debt_equ_ratio = getData("Debt/Equity")
    roic = getData("Invested Capital %")

    print("P/E: ", pe_ratio)
    print("Debt/Equity: ", debt_equ_ratio)
    print("ROIC: ", roic)

    browser.close()