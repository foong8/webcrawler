"""
Created By    : Lai Hon Foong
Date Creation : 5 Aug 2020 
"""

import sys
import os
import logging

logger = logging.getLogger(__name__)

from selenium import webdriver

from selenium.webdriver.chrome.options import Options 


def set_chromedriver(fp_download = None,
                     fp_driver   = None):

    if fp_download is not None:
        
        # (1) set up chrome options
        chromeOptions = webdriver.ChromeOptions()
        
        # (2) change the download directory
        prefs = {"download.default_directory" : fp_download}
        chromeOptions.add_experimental_option("prefs",prefs)
        
        # (3) set up driver
        driver = webdriver.Chrome(executable_path = fp_driver, chrome_options = chromeOptions)

    else:

        driver_option = Options()
        driver_option.add_argument("--headless")
        driver_option.add_argument("--proxy-server='direct://'");
        driver_option.add_argument("--proxy-bypass-list=*")
        driver_option.add_argument("--proxy-server=");
        driver_option.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        driver = webdriver.Chrome(executable_path = fp_driver, 
                                  chrome_options = driver_option)

    # return driver
    return driver

def set_firefoxdriver(fp_driver = None):
        
    driver = webdriver.Firefox(executable_path = fp_driver)
    return driver

def set_phantomjsdriver(fp_driver = None):

    driver = webdriver.PhantomJS(fp_driver)
    return driver


