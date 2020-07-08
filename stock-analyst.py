# Author: Dhairya Surana

import pycurl
import certifi
import time
from io import BytesIO 
import re
import datetime
import concurrent.futures
import sys

MAX_THREADS = 30


def getURL(ticker):

    b_obj = BytesIO() 
    crl = pycurl.Curl() 

    # Set URL value
    crl.setopt(pycurl.CAINFO, certifi.where())
    crl.setopt(crl.URL, f'https://www.wsj.com/market-data/quotes/{ticker}/financials')

    # Write bytes that are utf-8 encoded
    crl.setopt(crl.WRITEDATA, b_obj)

    # Perform a file transfer 
    crl.perform() 

    # Get the content stored in the BytesIO object (in byte characters) 
    result =  b_obj.getvalue().decode('utf8')

    crl.close()

    time.sleep(0.15)

    return result


def getPages(ticker_list):

    print("Getting URLs...", end="\n\n")

    threads = min(MAX_THREADS, len(ticker_list))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        return executor.map(getURL, ticker_list)

def getData(html):

    html_text = re.sub('<[^<]+?>', '', html)

    name_start = "<span class=\"companyName\">"
    name_end = "</span> <span class=\"tickerName\">"
    try:
        print("Company: ", html[html.index(name_start) + len(name_start) : html.index(name_end)])
    except:
        print("Company: not found")

    price_start = "<span id=\"quote_val\">"
    price_end = "</span></span> <span class=\"cr_sym\""
    try:
        print("     Price: ", html[html.index(price_start) + len(price_start) : html.index(price_end)])
    except:
        print("     Price: not found")

    pe_start = "P/E Ratio (TTM)"
    pe_end = "P/E Ratio (including extraordinary items)"
    try:
        print("     P/E Ratio: ", html_text[html_text.index(pe_start) + len(pe_start) : html_text.index(pe_end)])
    except:
        print(      "P/E Ratio: not found")

    roc_start = "Return on Total Capital"
    roc_end = "Return on Invested Capital"
    try:
        print("     ROC: ", html_text[html_text.index(roc_start) + len(roc_start) : html_text.index(roc_end)])
    except:
        print("     ROC: not found")

    print()

    
if __name__ == "__main__":

    start_time = time.time()
    
    try:
        file = open(sys.argv[1], 'rb')
        
    except Exception as e:
        SystemExit(e)

    ticker_list = [line.rstrip().decode("utf-8") for line in file.readlines()]

    page_list = getPages(ticker_list)
    list(map(getData, page_list))

    print("Runtime: ", time.time() - start_time, " s")