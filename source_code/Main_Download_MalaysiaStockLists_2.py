"""
Created By    : Lai Hon Foong
Date Creation : 5 Aug 2020 
"""

#internal library
from lib.set_logging import set_logging
from lib.set_webdriver import set_chromedriver
from lib.set_webdriver import set_firefoxdriver
from config import set_configinfo
import lib.process_webdriver as process_webdriver


from datetime import datetime
import logging
import pandas as pd
import os
import threading


str_websitename_equitiesmalaysia = "https://www.investing.com/equities/malaysia"
str_websitename_investing        = "https://www.investing.com"


from multiprocessing import Pool


def main():

    #load MalaysiaStocklist
    #process with existing list or half way list
    data = pd.read_csv(os.path.join(configInfo.fp["fp_masterlist"], "MalaysiaStock_MasterLists.csv"))
    
    
    data = data.values.tolist()
    print(data)
    # #create the chrome driver instance
    # obj_driver = set_chromedriver(fp_download     = configInfo.fp["fp_his_download"] ,
    #                               fp_driver = configInfo.fp["fp_chromedriver"])
    
    
    
    
    # p = Pool(10)
    # p.map(process_webdriver.download_the_data, (obj_driver,
    #                                             str_websitename_investing + data["Hyperlink"],
    #                                             data["CompanyName"],
    #                                             configInfo.fp["fp_his_download"]))
    # p.terminate()
    # p.join()
    
    
    
    
    # # loop for all the row
    # for index, row in data.iterrows():
        
        # #download the data
        # is_download_success = process_webdriver.download_the_data(
        #                         obj_driver = obj_driver,
        #                         str_stockURL     = str_websitename_investing + row["Hyperlink"],
        #                         str_companyname  = row["CompanyName"],
        #                         fp_his_download  = configInfo.fp["fp_his_download"])

        # #if downlaod the data sccuess
        # if is_download_success:
        #     row["DownloadStatus"] = "Download_Success"
        # else:
        #     row["DownloadErrorFrequency"] =row["DownloadErrorFrequency"] + 1



    #close the chrome
    # obj_driver.close()

if __name__ == "__main__":

    #create the instance confiinfo from the config.ini
    configInfo      = set_configinfo()  

    #setup logging
    #create the dummy date string for the logger file name
    dummy_date      = datetime.now().strftime("%y%m%d")
    fn_logging      = configInfo.fn["fn_log_downloadmalaysiastocklist"]  + "_" + dummy_date + ".log"

    obj_logger      = set_logging(fp       = configInfo.fp["fp_log_file"],
                                  fn       = fn_logging,
                                  setlevel = configInfo.level["level"])

    #execute the main procedures
    main()