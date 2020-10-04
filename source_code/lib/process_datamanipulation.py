from shutil import copyfile

import logging
import pandas as pd
import os
import numpy as np


logger = logging.getLogger(__name__)


def _convert_volume_unit(value):
    
    "all the volume unit must be in Million"
    
    if "M" in value:
        value = str(value[:-1])
    elif "K" in value:
        value = value[:-1]
        value = float(value) / 1000
        value = str(value)
    elif "B" in value:
        value = value[:-1]
        value = float(value) * 1000
        value = str(value)
    
    return value


def _load_into_existing_database(df_temp = None,
                                 fn_his_download = None,
                                 fn_database = None):
    
    if os.path.isfile(fn_database):
        df_existing = pd.read_csv(fn_database)
        df_existing = df_existing.append(df_temp, ignore_index = True).drop_duplicates(subset = "Date")
        df_existing.to_csv(fn_database, index = False)
    else:
        copyfile(fn_his_download, fn_database)


def append_data(list_values      = None,
                dict_configInfo  = None,
                output           = None):
    
    fp_his_download = dict_configInfo.fp["fp_his_download"]
    fp_database = dict_configInfo.fp["fp_database"]
    
    #loop the list_value
    for list_value in list_values:
        
        #get the file full path name
        str_companyname = list_value[0]
        fn_his_download = os.path.join(fp_his_download, str_companyname + ".csv")
        fn_database     = os.path.join(fp_database, str_companyname + ".csv")
        
        #skip if the status is not downlaod succesful
        if list_value[2] != "Download Sucessful":
            list_value[4] = "Skipped"
            continue
        else:
            # clear up on the volume column
            df_temp = pd.read_csv(fn_his_download)
            df_temp["Vol."] = df_temp["Vol."].apply(_convert_volume_unit)
            
            # append to the existing file if any
            _load_into_existing_database(df_temp, fn_his_download, fn_database)
            list_value[4] = "Append Successfully"
    
    if output is None:
        return list_values
    else:
        output.put(pd.DataFrame(list_values))

def volume_spike_indicator(list_values      = None,
                           dict_configInfo  = None,
                           output           = None):
    
    fp_database = dict_configInfo.fp["fp_database"]

    #loop the list_value
    for list_value in list_values:
        str_companyname = list_value[0]
        fn_database     = os.path.join(fp_database, str_companyname + ".csv")
        
        if list_value[4] != "Append Successfully":
            continue
        else:
            df_temp = pd.read_csv(fn_database)
            int_rows, int_cols = df_temp.shape
        
            if int_rows < 10:
                list_value[5] = "Less than 10 Rows"
                continue
            else:
                df_temp["Vol."] = df_temp["Vol."].astype(float)
                df_temp["Volume Moving Average"] = df_temp.iloc[:,5].rolling(window = 10).mean()
                df_temp["Volume Moving Average"] = df_temp["Volume Moving Average"].astype(float)
                df_temp["Volume Spike"] = np.where(df_temp["Vol."] >= df_temp["Volume Moving Average"], "Y", "N")
                df_temp.to_csv(fn_database)
                
                #update the master list
                if df_temp.iloc[-1, df_temp.columns.get_loc("Volume Spike")] == "Y":
                    list_value[6] = "Y"
                else:
                    list_value[6] = "N"
                
                list_value[5] = "Calculcated Done"
                
    if output is None:
        return list_values
    else:
        output.put(pd.DataFrame(list_values))
