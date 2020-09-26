"""
Created By    : Lai Hon Foong
Date Creation : 5 Aug 2020 
"""

import logging
import os
import sys
from datetime import datetime


#logging level dict
#https://docs.python.org/3/library/logging.html#levels
dict_setlevel = {"CRITICAL" : 50,
                "ERROR"    : 40,
                "WARNING"  : 30,
                "INFO"     : 20,
                "DEBUG"    : 10}
#create the dummy date string for the logger file name

def set_logging(fp      : "folder path for log file" = None,
                fn      : "file name for log file"   = None,
                setlevel: "logging setlevel"         = "Info"):
    
    """
    Description:
        (1) get the logging setlevel (by default is info)
        (2) create the root logger
        (3) create the handler
        (4) configure the Formatter
        (5) add handler to the root logger
        (6) return the logger
    """

    #(1) get the logging setlevel (by default is info)
    int_setlevel = dict_setlevel.get(setlevel.upper(), "20")
    
    #(2) create the root logger
    logger = logging.getLogger()
    logger.setLevel(int_setlevel)

    str_date = datetime.now().strftime("%y%m%d")
    fn       = fn  + "_" + str_date + ".log"

    #(3) create the handler
    fh = logging.FileHandler(os.path.join(fp, fn))
    ch = logging.StreamHandler(sys.stdout)

    #(4) configure the Formatter
    #refer to LogReocrd Attributes (https://docs.python.org/3/library/logging.html#logrecord-attributes)
    formatter = logging.Formatter("[%(filename)s:%(lineno)s - %(funcName)20s() ] %(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    #(5) add handler to the root logger
    #to avoid duplicated handler
    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)

    #(6) return the logger
    return logger



