"""
Created By    : Lai Hon Foong
Date Creation : 5 Aug 2020 
"""

# internal library
from lib.set_logging import set_logging
from lib.config import set_configinfo
from lib.cls_dataframe import SubclassedDataFrame
import lib.process_webdriver as process_webdriver
import os

str_websitename_equitiesmalaysia = "https://www.investing.com/equities/malaysia"


def main():

    # setup config info
    configInfo = set_configinfo()

    # setup logging
    obj_logger = set_logging(fp=configInfo.fp["fp_log_file"],
                             fn=configInfo.fn["fn_log_createupdatemasterlist"],
                             setlevel=configInfo.level["level"])

    # create a class to create the dataframe
    df_processing = SubclassedDataFrame.initial_df_based_json(configInfo.tablelookup["cols_processing"])
    
    # get the lists of company name and hyperlink
    df_processing = process_webdriver.get_full_lists_of_malaysia_stocks(
                                                dict_configInfo=configInfo.fp,
                                                df_dataframe=df_processing,
                                                str_websitename=str_websitename_equitiesmalaysia)

    # rename the columns
    df_processing = df_processing.rephrase_columns_based_json(configInfo.tablelookup["cols_processing"])

    # save the df to csv file
    df_processing.to_csv(os.path.join(configInfo.fp["fp_masterlist"], "MalaysiaStock_MasterLists.csv"),
                         index=False)

    obj_logger.info("MalaysiaStock_masterlists.csv has been updated.")


if __name__ == "__main__":

    # execute the main procedures
    main()
