"""
Created By    : Lai Hon Foong
Date Creation : 31 Aug 2020 
"""

import sys
import os
import logging

logger = logging.getLogger(__name__)

from selenium import webdriver

def set_phantomjsdriver(phantomjsdriverpath = None):
    
        # (1) set up PhantomJS
        driver = webdriver.PhantomJS(phantomjsdriverpath)
        return driver


