# Author: Dhairya Surana

import pycurl
import certifi
import time
import re
import datetime
import concurrent.futures
import sys

from multiprocessing import Process
from io import BytesIO 

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
    conn = 0
    for i in range(1, 6):
        try:
            conn = i
            crl.perform()
            break
        except Exception:

            if(i == 5):
                SystemExit("Pycurl perform() attempts exceeded")
            continue 

        

    # Get the content stored in the BytesIO object (in byte characters) 
    result =  b_obj.getvalue().decode('utf8')

    crl.close()

    time.sleep(0.3)

    # name_start = "<span class=\"companyName\">"
    # roc_end = "Return on Invested Capital"

    # return result[result.index(name_start) : result.index(roc_end)]

    return (ticker, conn,  result)


def getPages(ticker_list):

    threads = min(MAX_THREADS, len(ticker_list))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        return executor.map(getURL, ticker_list)

def getData(tup, out_file):

    ticker, conn, html = tup

    html_text = re.sub('<[^<]+?>', '', html)

    name_start = "<span class=\"companyName\">"
    name_end = "</span> <span class=\"tickerName\">"

    out_file.write("URL: " + f'https://www.wsj.com/market-data/quotes/{ticker}/financials\n')
    out_file.write(f"Connection attempts: {conn}\n")
    try:
        out_file.write("Company: " + html[html.index(name_start) + len(name_start) : html.index(name_end)] + "\n")
    except:
        out_file.write("Company: not found\n")

    price_start = "<span id=\"quote_val\">"
    price_end = "</span></span> <span class=\"cr_sym\""
    try:
        out_file.write("     Price: " + html[html.index(price_start) + len(price_start) : html.index(price_end)] + "\n")
    except:
        out_file.write("     Price: not found\n")

    pe_start = "P/E Ratio (TTM)"
    pe_end = "P/E Ratio (including extraordinary items)"
    try:
        out_file.write("     P/E Ratio: " + html_text[html_text.index(pe_start) + len(pe_start) : html_text.index(pe_end)] + "\n")
    except:
        out_file.write(      "P/E Ratio: not found\n")

    roc_start = "Return on Total Capital"
    roc_end = "Return on Invested Capital"
    try:
        out_file.write("     ROC: " + html_text[html_text.index(roc_start) + len(roc_start) : html_text.index(roc_end)] + "\n")
    except:
        out_file.write("     ROC: not found\n")

    out_file.write("\n")

def playWaitAnim():

    animation = "|/-\\"
    
    idx = 0
    while True:
        print("Getting URLS...", animation[idx % len(animation)], end="\r")
        idx += 1
        time.sleep(0.1)
    
if __name__ == "__main__":

    start_time = time.time()
    
    try:
        inp_file = open(sys.argv[1], 'rb')
        out_file = open("data.txt", 'a')
        
    except Exception as e:
        SystemExit(e)

    ticker_list = [line.rstrip().decode("utf-8").split()[0] for line in inp_file.readlines()]
    inp_file.close()

    p1 = Process(target=playWaitAnim)
    p1.start()

    page_list = getPages(ticker_list)
    p1.terminate()
    print("Getting URLS... COMPLETE")

    for page in page_list:
        getData(page, out_file)

    out_file.close()


    print("Runtime: ", time.time() - start_time, " s")