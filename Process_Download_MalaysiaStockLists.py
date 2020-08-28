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
    
    #load MalaysiaStocklist
    #loop the row
        #open the link
        #extract the dota from table
        #save to in cvs file
    
    pass




if __name__ == "__main__":

    #create the instance confiinfo from the config.ini
    configInfo      = set_configinfo()  

    #setup logging
    #create the dummy date string for the logger file name
    dummy_date      = datetime.now().strftime("%y%m%d")
    fn_logging      = configInfo.fn["fn_logging"]  + "_" + dummy_date + ".log"

    obj_logger      = set_logging(fp       = configInfo.fp["fp_logging"],
                                  fn       = fn_logging,
                                  setlevel =  "INFO")

    #execute the main procedures
    main()