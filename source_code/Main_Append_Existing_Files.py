"""
Created By    : Lai Hon Foong
Date Creation : 5 Aug 2020 
"""

from lib.config import set_configinfo
from lib.set_logging import set_logging
from lib.cls_dataframe import SubclassedDataFrame
from lib.process_datamanipulation import append_data

import pandas as pd
import os 

fn_process_malaysiastockmasterlist = "Process_MalaysiaStock_MasterLists.csv"

def main():

    #setup configinfo
    configInfo      = set_configinfo()

    #setup logging
    obj_logger      = set_logging(fp       = configInfo.fp["fp_log_file"],
                                  fn       = configInfo.fn["fn_log_appendexistingfiles"],
                                  setlevel = configInfo.level["level"])

    #load MalaysiaStocklist
    #process with existing list or half way list
    df_processing = SubclassedDataFrame(
                        pd.read_csv(os.path.join(configInfo.fp["fp_masterlist"], fn_process_malaysiastockmasterlist)))

    #multiprocess to append the data
    df_processing = df_processing.run_multiprocessing(int_parts = 1,
                                                      str_funcname = append_data,
                                                      configInfo = configInfo)

    #get the column name
    df_processing = df_processing.rephrase_columns_based_json(configInfo.tablelookup["cols_processing"])
    df_processing.to_csv(os.path.join(configInfo.fp["fp_masterlist"], "Process_MalaysiaStock_MasterLists.csv"), index = False)

    obj_logger.info("Appned Done")

if __name__ == "__main__":
    main()