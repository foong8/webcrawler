"""
Created By    : Lai Hon Foong
Date Creation : 5 Aug 2020 
"""

#internal library
from lib.set_logging import set_logging
from lib.set_chrome import set_chromedriver
from lib.config import set_configinfo
import lib.process_webdriver as process_webdriver

from datetime import datetime
import logging
import pandas as pd

str_websitename_equitiesmalaysia = "https://www.investing.com/equities/malaysia"
str_websitename_investing        = "https://www.investing.com/equities/"

def main():

    #create the chrome driver instance
    obj_chromedriver = set_chromedriver(downloadpath     = configInfo.fp["fp_download"] ,
                                        chromedriverpath = configInfo.fp["fp_chromedrive"])

    #get the lists of company name and hyperlink
    lists_companyname, lists_hyperlink = process_webdriver.get_lists_malaysia_stock(
                                            obj_chromedriver = obj_chromedriver,
                                            str_websitename  = str_websitename_equitiesmalaysia)

    #create dataframe
    data = {"CompanyName"       : lists_companyname,
            "Hyperlink"         : lists_hyperlink
            }
    
    data["DownloadStatus"] = "To_be_Process"
    
    df_stocklist = pd.DataFrame(data)
    df_stocklist.to_csv("MalaysiaStock_MasterLists.csv", index = False)
    
    obj_logger.info("MalaysiaStock_masterlists.csv has been updated.")

if __name__ == "__main__":

    #create the instance confiinfo from the config.ini
    configInfo = set_configinfo()  
    
    #setup logging
    #create the dummy date string for the logger file name
    dummy_date      = datetime.now().strftime("%y%m%d")
    fn_logging      = configInfo.fn["fn_logging"]  + "_" + dummy_date + ".log"
    
    obj_logger      = set_logging(fp       = configInfo.fp["fp_logging"],
                                  fn       = fn_logging,
                                  setlevel =  "INFO")

    #execute the main procedures
    main()


