"""
Created By    : Lai Hon Foong
Date Creation : 5 Aug 2020 
"""

#internal library
from lib.set_logging import set_logging
from lib.set_chrome import set_chromedriver
from config import set_configinfo
import lib.process_webdriver as process_webdriver

from datetime import datetime
import logging
import pandas as pd
import os


str_websitename_equitiesmalaysia = "https://www.investing.com/equities/malaysia"

def main():

    #create the chrome driver instance
    obj_chromedriver = set_chromedriver(fp_download = configInfo.fp["fp_his_download"] ,
                                        fp_driver   = configInfo.fp["fp_chromedrive"])

    #get the lists of company name and hyperlink
    lists_companyname, lists_hyperlink = process_webdriver.get_lists_malaysia_stock(
                                            obj_chromedriver = obj_chromedriver,
                                            str_websitename  = str_websitename_equitiesmalaysia)

    #create dataframe
    data = {"CompanyName"       : lists_companyname,
            "Hyperlink"         : lists_hyperlink}

    #add new columns with default value
    data["DownloadStatus"] = "To_be_Process"
    data["DownloadErrorFrequency"] = 1

    #conver to pandas dataframe
    df_stocklist = pd.DataFrame(data)
    df_stocklist.to_csv(os.path.join(configInfo.fp["fp_masterlist"], "MalaysiaStock_MasterLists.csv"), index = False)

    #logging
    obj_logger.info("MalaysiaStock_masterlists.csv has been updated.")

if __name__ == "__main__":

    #create the instance confiinfo from the config.ini
    configInfo = set_configinfo()  

    #setup logging
    #create the dummy date string for the logger file name
    dummy_date      = datetime.now().strftime("%y%m%d")
    fn_logging      = configInfo.fn["fn_log_createupdatemasterlist"]  + "_" + dummy_date + ".log"

    obj_logger      = set_logging(fp       = configInfo.fp["fp_log_file"],
                                  fn       = fn_logging,
                                  setlevel = configInfo.level["level"])

    #execute the main procedures
    main()


