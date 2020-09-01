"""
Created By    : Lai Hon Foong
Date Creation : 5 Aug 2020 
"""

#internal library
# from lib.set_logging import set_logging
# from lib.set_webdriver import set_chromedriver
# from lib.set_webdriver import set_firefoxdriver
# from config import set_configinfo
# import lib.process_webdriver as process_webdriver

from selenium import webdriver
from datetime import datetime
import logging
import pandas as pd
import os
import time

from bs4 import BeautifulSoup 
from selenium.webdriver.support.select import Select

import threading
from multiprocessing import Pool
from multiprocessing import Process
from multiprocessing import Queue


str_websitename_equitiesmalaysia = "https://www.investing.com/equities/malaysia"
str_websitename_investing        = "https://www.investing.com"


from multiprocessing import Pool
from selenium.webdriver.chrome.options import Options 

def testing_download_the_data(list_values):
    # print(str_websitename_investing + list_value[1])
    # print(list_value[0])
    # print(list_values)
    
    #create the chrome driver instance
    driver_option = Options()
    driver_option.add_argument("--headless")
    driver_option.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    obj_driver = webdriver.Chrome(executable_path = r"C:\Users\User\Documents\AlgoTrading\chromedriver.exe",
                                  chrome_options = driver_option)

     for list_value in list_values:
        
        try:
            #(1) Open the investing.com website
            obj_driver.get(str_websitename_investing + list_value[1])
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
            df.to_csv(os.path.join(r"C:\Users\User\Documents\AlgoTrading\historical_download", list_value[0] + ".csv"), index = False)
            #(4) check if the download file success or not
            # if os.path.isfile(os.path.join(fp_his_download, str_companyname + ".csv")):
            #     is_download_success = True
        except:
            print("error")
    #     # is_download_success = False
        
    obj_driver.close()


def main():

    #load MalaysiaStocklist
    #process with existing list or half way list
    data = pd.read_csv(r"C:\Users\User\Documents\AlgoTrading\source_code\MalaysiaStock_MasterLists.csv")
    
    
    data = data.values.tolist()
    
    # print(data[2][1])
    
    ### Split into 4 symbols
    num=10
    div=[data[i::num] for i in range(num)]
    start=time.time()

    ### Multiprocessing with Process
    processes = [Process(target=testing_download_the_data,args=(div[i],)) for i in range(num)]

    # # Run processes
    for p in processes:p.start()
    for p in processes:p.join()

    #close the chrome
    # obj_driver.close()

if __name__ == "__main__":

    #create the instance confiinfo from the config.ini
    # configInfo      = set_configinfo()  

    # #setup logging
    # #create the dummy date string for the logger file name
    # dummy_date      = datetime.now().strftime("%y%m%d")
    # fn_logging      = configInfo.fn["fn_log_downloadmalaysiastocklist"]  + "_" + dummy_date + ".log"

    # obj_logger      = set_logging(fp       = configInfo.fp["fp_log_file"],
    #                               fn       = fn_logging,
    #                               setlevel = configInfo.level["level"])

    #execute the main procedures
    main()