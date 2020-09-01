"""
Created By    : Lai Hon Foong
Date Creation : 5 Aug 2020 
"""
from bs4 import BeautifulSoup 
from selenium.webdriver.support.select import Select
from lib.set_webdriver import set_chromedriver



import logging
import pandas as pd
import time
import os

logger = logging.getLogger(__name__)

def get_lists_malaysia_stock(obj_driver = None,
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
    obj_driver.get(str_websitename)
    
    #(2) Select the option for the malaysia all stock    
    select = Select(obj_driver.find_element_by_xpath("/html/body/div[5]/section/div[6]/select"))
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
    obj_driver.close()
    
    #(4) Return lists
    return list_companyname, list_href


def download_the_data(obj_driver = None,
                      str_stockURL     = None,
                      str_companyname  = None,
                      fp_his_download  = None):
    
    is_download_success = False
    
    
    #if any error hit then alawys is_download_success return to false
    try:
        print("here1")
        #(1) Open the investing.com website
        obj_driver.get(str_stockURL)
        
        #(2) Click the "Historical Data" button
        obj_driver.find_element_by_xpath("/html/body/div[5]/section/ul[2]/li[3]/a").click()
        
        time.sleep(1)
        
        #(3) Extract all the Company Name and Hyperlink from the HTML Table
        #praser entire HTML document
        HTMLContent     = BeautifulSoup(obj_driver.page_source, "html.parser")
        #search the specific DIV tag 
        HTMLDiv         = HTMLContent.find("div", {"id" : "results_box"})
        #search the specific TABLE tag
        HTMLTable       = HTMLDiv.find("table", {"id": "curr_table"})
        #get the table with header
        tab_data = [[cell.text for cell in row.find_all(["th","td"])]
                            for row in HTMLTable.find_all("tr")]
        #convert to dataframe
        df = pd.DataFrame(tab_data)
        #set the header
        df.columns = df.iloc[0,:]
        #drop the index
        df.drop(index=0,inplace=True)
        #save as the csv file
        df.to_csv(os.path.join(fp_his_download, str_companyname + ".csv"), index = False)
        print("here")
        time.sleep(0.8)
        
        #(4) check if the download file success or not
        if os.path.isfile(os.path.join(fp_his_download, str_companyname + ".csv")):
            is_download_success = True
    except:
        print("error")
        is_download_success = False
    
    # finally:
    #     return is_download_success
        
        


def testing_download_the_data(list_value = None):
    
    
    #create the chrome driver instance
    driver = webdriver.Chrome()
    
    
    try:
        #(1) Open the investing.com website
        obj_driver.get(str_stockURL)
        
        #(2) Click the "Historical Data" button
        obj_driver.find_element_by_xpath("/html/body/div[5]/section/ul[2]/li[3]/a").click()
        
        time.sleep(1)
        
        #(3) Extract all the Company Name and Hyperlink from the HTML Table
        #praser entire HTML document
        HTMLContent     = BeautifulSoup(obj_driver.page_source, "html.parser")
        #search the specific DIV tag 
        HTMLDiv         = HTMLContent.find("div", {"id" : "results_box"})
        #search the specific TABLE tag
        HTMLTable       = HTMLDiv.find("table", {"id": "curr_table"})
        #get the table with header
        tab_data = [[cell.text for cell in row.find_all(["th","td"])]
                            for row in HTMLTable.find_all("tr")]
        #convert to dataframe
        df = pd.DataFrame(tab_data)
        #set the header
        df.columns = df.iloc[0,:]
        #drop the index
        df.drop(index=0,inplace=True)
        #save as the csv file
        df.to_csv(os.path.join(fp_his_download, str_companyname + ".csv"), index = False)
        print("here")
        time.sleep(0.8)
        
        #(4) check if the download file success or not
        if os.path.isfile(os.path.join(fp_his_download, str_companyname + ".csv")):
            is_download_success = True
    except:
        print("error")
        is_download_success = False
    
    