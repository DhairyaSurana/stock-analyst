import pycurl
import certifi
import time
from io import BytesIO 
from bs4 import BeautifulSoup
import re
import datetime


def getPages(ticker_list):

    print("Getting URLs...", end="  ")
    start_time = time.time()

    page_list = []
    for ticker in ticker_list:

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
        html = b_obj.getvalue().decode('utf8')

        page_list.append(html)
    
    # End curl session
    crl.close()

    print("Runtime: ", time.time() - start_time, " s", end="\n\n")

    return page_list
   


def getData(pages):

    print("Gathering Data...")
    start_time = time.time()
    for html in pages:

        html_text = re.sub('<[^<]+?>', '', html)

        name_start = "<span class=\"companyName\">"
        name_end = "</span> <span class=\"tickerName\">"
        print("Company: ", html[html.index(name_start) + len(name_start) : html.index(name_end)])

        price_start = "<span id=\"quote_val\">"
        price_end = "</span></span> <span class=\"cr_sym\""
        print("     Price: ", html[html.index(price_start) + len(price_start) : html.index(price_end)])

        pe_start = "P/E Ratio (TTM)"
        pe_end = "P/E Ratio (including extraordinary items)"
        print("     P/E Ratio: ", html_text[html_text.index(pe_start) + len(pe_start) : html_text.index(pe_end)])

        roc_start = "Return on Total Capital"
        roc_end = "Return on Invested Capital"
        print("     ROC: ", html_text[html_text.index(roc_start) + len(roc_start) : html_text.index(roc_end)])
        print()

    print("Runtime: ", time.time() - start_time, " s", end="\n\n")   

    
if __name__ == "__main__":

    
    ticker_list = ["PCRFY", "MSFT", "AMZN", "AAPL", "TSLA", "ZNGA", "CCLP"]

    page_list = getPages(ticker_list)
    getData(page_list)

    print("Total Runtime: ", time.perf_counter(), " s", end="\n\n")   