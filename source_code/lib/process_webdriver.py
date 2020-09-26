"""
Created By    : Lai Hon Foong
Date Creation : 5 Aug 2020 
"""
from bs4 import BeautifulSoup 
from selenium.webdriver.support.select import Select
from lib.set_webdriver import set_chromedriver
from selenium.webdriver.chrome.options import Options 
from selenium import webdriver

import logging
import pandas as pd
import time
import os

logger = logging.getLogger(__name__)


def get_full_lists_of_malaysia_stocks(dict_configInfo = None, 
                                     df_dataframe     = None, 
                                     str_websitename  = None):
    
    """
    Process Description:
        (1) Setup object driver
        (2) Open the investing.com website
        (3) Select the option for the malaysia all stock
        (4) Extract all the Company Name and Hyperlink from the HTML Table
        (5) fill up the value for the dataframe
        (6) return dataframe
    """

    list_companyname = []
    list_href        = []

    #(1) Setup object driver
    obj_driver = set_chromedriver(fp_download = dict_configInfo["fp_his_download"] ,
                                  fp_driver   = dict_configInfo["fp_chromedriver"])

    #(2) Open the investing.com website
    obj_driver.get(str_websitename)

    #(3) Select the option for the malaysia all stock    
    select = Select(obj_driver.find_element_by_xpath("/html/body/div[5]/section/div[6]/select"))
    select.select_by_visible_text("Malaysia all stocks")
    time.sleep(10)

    #(4) Extract all the Company Name and Hyperlink from the HTML Table
    #praser entire HTML document
    HTMLContent     = BeautifulSoup(obj_driver.page_source, "html.parser")
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
    
    #(5) fill up the value for the dataframe
    df_dataframe["attr_1"] = list_companyname
    df_dataframe["attr_2"] = list_href
    df_dataframe["attr_3"] = "To be processed"
    df_dataframe["attr_4"] = 1
    
    #(6) Return dataframe
    return df_dataframe


def download_the_data(list_values      = None,
                      dict_configInfo  = None,
                      output           = None):

    str_websitename_investing        = "https://www.investing.com"

    #(1) Setup object driver
    driver_option = Options()
    driver_option.add_argument("--headless")
    driver_option.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    obj_driver = webdriver.Chrome(executable_path = dict_configInfo.fp["fp_chromedriver"],
                                  chrome_options = driver_option)

    for list_value in list_values:
        str_url     = str_websitename_investing + list_value[1]
        fn_download = os.path.join(dict_configInfo.fp["fp_his_download"], list_value[0] + ".csv")
        #if any error hit then alawys is_download_success return to false
        try:
            #(1) Open the investing.com website
            obj_driver.get(str_url)
            #(2) Click the "Historical Data" button
            obj_driver.find_element_by_xpath("/html/body/div[5]/section/ul[2]/li[3]/a").click()
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
            df.to_csv(fn_download, index = False)
            #(4) check if the download file success or not
            list_value[2] = "Download Sucessful"
        except:
            list_value[2] = "Download Failed"
    
    if output is None:
        return list_values
    else:
        output.put(pd.DataFrame(list_values))