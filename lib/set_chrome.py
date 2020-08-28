"""
Created By    : Lai Hon Foong
Date Creation : 5 Aug 2020 
"""

import sys
import os
import logging

logger = logging.getLogger(__name__)

from selenium import webdriver

def set_chromedriver(downloadpath = None,
                     chromedriverpath = None):
    """
    Description:
        With downloadpath
        (1) set up chrome options
        (2) change the download directory
        (3) Set up driver
        (4) Return chrome driver object
    
        or 
        Without downloadpath
        (3) Set up driver
        (4) Return chrome driver object
    """
    
    if downloadpath is not None:
        
        # (1) set up chrome options
        chromeOptions = webdriver.ChromeOptions()
        
        # (2) change the download directory
        prefs = {"download.default_directory" : downloadpath}
        chromeOptions.add_experimental_option("prefs",prefs)
        
        # (3) set up driver
        driver = webdriver.Chrome(chromedriverpath, options = chromeOptions)
        
        # (4) return driver
        return driver
    
    else:
        
        # set up driver
        driver = webdriver.Chrome(chromedriverpath)
        
        # return driver
        return driver

