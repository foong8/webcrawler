"""
Created By    : Lai Hon Foong
Date Creation : 5 Aug 2020 
"""
import sys
import os
import logging
from configparser import ConfigParser

#create the logger
logger = logging.getLogger(__name__)


class ConfigInfo:
    """
    Description:
        Instance object for the ConfigInfo
    
    Property: 
        fn = file name
        fp = folder path
    """
    
    def __init__(self, 
                  fn = None,
                  fp = None):
        self.fn = None
        self.fp = None
        pass 

    @property
    def fn(self):
        return self.__fn

    @fn.setter
    def fn(self, value):
        self.__fn = value

    @property
    def fp(self):
        return self.__fp

    @fp.setter
    def fp(self, value):
        self.__fp = value
        
        
def set_configinfo():
    
    
    """
    Description:
        (1) read the config file
        (2) create the instance for the configInfo
        (3) return instance
    """
    
    #(1) read the config file
    if os.path.isfile("../config.ini"):
        config_object = ConfigParser()
        config_object.read("../config.ini")
    else:
        logger.warning("config.ini is not found!")
        input("Press enter to exit the program....")
    
    #(2) create the instance for the configInfo
    configInfo    = ConfigInfo()
    configInfo.fn = dict(config_object["FILENAME"])
    configInfo.fp = dict(config_object["FOLDERPATH"])       
    configInfo.level = dict(config_object["LOGLEVEL"])
    
    #(3) return 
    return configInfo


