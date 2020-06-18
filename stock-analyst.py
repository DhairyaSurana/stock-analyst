# # stock-analyst.py

from bs4 import BeautifulSoup
from selenium import webdriver 
import sys
import re
import requests


def getData(attr):

    stat = soup.find(text=re.compile(attr))
    data = soup.find(text=re.compile(attr)).find_next('div').contents[0].strip()

    return (stat, data)



if __name__=="__main__":

    ticker = sys.argv[1]
    url = f"https://www.morningstar.com/stocks/xnas/{ticker}/quote"

    browser = webdriver.Chrome()
    # browser.get(url)

    # soup = BeautifulSoup(browser.page_source,'lxml')

    # price = soup.find('div', {'id':'message-box-price'})
    # price2 = price.text.strip()
    # print(price2)

    url = f"https://www.morningstar.com/stocks/xnas/{ticker}/financials"
    browser.get(url)
    soup = BeautifulSoup(browser.page_source,'lxml')
    print(getData("Debt/Equity"))

    browser.close()
    
    # try:
    #     r = requests.get(url)
    #     r.raise_for_status()

    # except requests.exceptions.HTTPError as e:
    #     raise SystemExit(e) 

    # # Parse the html content
    # soup = BeautifulSoup(r.text, "lxml")
    # print(soup.text) # print the parsed data of html

    # # stats = soup.find_all("li")
    # # for div in stats:
    # #     print(div)
  