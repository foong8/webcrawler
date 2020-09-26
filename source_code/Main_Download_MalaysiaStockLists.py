"""
Created By    : Lai Hon Foong
Date Creation : 5 Aug 2020 
"""

#internal library
from lib.config import set_configinfo
from lib.set_logging import set_logging
from lib.cls_dataframe import SubclassedDataFrame
import lib.process_webdriver as process_webdriver
import os

import pandas as pd

str_websitename_equitiesmalaysia = "https://www.investing.com/equities/malaysia"
str_websitename_investing        = "https://www.investing.com"

def main():

    #setup configinfo
    configInfo      = set_configinfo()

    #setup logging
    obj_logger      = set_logging(fp       = configInfo.fp["fp_log_file"],
                                  fn       = configInfo.fn["fn_log_downloadmalaysiastocklist"],
                                  setlevel = configInfo.level["level"])

    #load MalaysiaStocklist
    #process with existing list or half way list
    df_processing = SubclassedDataFrame(
                        pd.read_csv(os.path.join(configInfo.fp["fp_masterlist"], "MalaysiaStock_MasterLists.csv")))

    df_processing = df_processing.run_multiprocessing(int_parts = 4,
                                                      str_funcname = process_webdriver.download_the_data,
                                                      configInfo = configInfo)

    df_processing = df_processing.rephrase_columns_based_json(configInfo.tablelookup["cols_processing"])
    df_processing.to_csv(os.path.join(configInfo.fp["fp_masterlist"], "Process_MalaysiaStock_MasterLists.csv"), index = False)

if __name__ == "__main__":

    #execute the main procedures
    main()
