"""
Created By    : Lai Hon Foong
Date Creation : 5 Aug 2020 
"""
from bs4 import BeautifulSoup 
from selenium.webdriver.support.select import Select
import pandas as pd
import time

def get_lists_malaysia_stock(obj_chromedriver = None,
                             str_websitename  = None):
    
    """
    Process Description:
        (1) Open the investing.com website
        (2) Select the option for the malaysia all stock
        (3) Extract all the Company Name and Hyperlink from the HTML Table
        (4) Return lists
    """

    list_companyname = []
    list_href        = []
    
    #(1) Open the investing.com website
    obj_chromedriver.get(str_websitename)
    
    #(2) Select the option for the malaysia all stock    
    select = Select(obj_chromedriver.find_element_by_xpath("/html/body/div[5]/section/div[6]/select"))
    select.select_by_visible_text("Malaysia all stocks")
    time.sleep(10)
    
    #(3) Extract all the Company Name and Hyperlink from the HTML Table
    #praser entire HTML document
    HTMLContent     = BeautifulSoup(obj_chromedriver.page_source, "html.parser")
    #search the specific DIV tag 
    HTMLDiv         = HTMLContent.find("div", {"id" : "marketInnerContent"})
    #search the specific TABLE tag
    HTMLTable       = HTMLDiv.find("table", {"id": "cross_rate_markets_stocks_1"})
    
    #loop the tr from the TABLE tag
    for tag_tr in HTMLTable.findAll("tr"):
        tag_td = tag_tr.find_all("td")
        #loop the column by td
        for tag_class in tag_td:
            #filter the column by specific class value
            if "plusIconTd" in tag_class["class"]:
                tag_a = tag_class.find_all("a")
                #loop the tag "a"
                for attributes in tag_a:
                    list_companyname.append(attributes["title"])
                    list_href.append(attributes["href"])
       
    #close the webpage
    obj_chromedriver.close()
    
    #(4) Return lists
    return list_companyname, list_href


def download_the_data(obj_chromedriver = None,
                      str_websitename  = None,
                      df_stocklist     = None):
    
    pass
    
    
    #go to the historical data page by clicking below full path x
    #/html/body/div[5]/section/ul[2]/li[3]/a
    
    #parse the table into excel
    
    #save the excel files
    
    
    
    