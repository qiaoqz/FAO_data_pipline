#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 16:46:33 2018

@author: QiaoQiao
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import re
from datetime import datetime
from bs4 import BeautifulSoup
import os
import time
import random

def FAO_scraping():
    url = "http://www.fao.org/faostat/en/#data/QC"
    #CurrentYear = str(datetime.now())[0:4]
    options = Options()
    options.add_argument("--headless")
    
    profile =  webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList",2)
    # disabling Download Manager window when a download begins
    profile.set_preference("browser.download.manager.showWhenStarting",False)
    profile.set_preference("browser.download.panel.shown", False)
    # popup window at bottom right corner of the screen will not appear once all downloads are finished
    profile.set_preference("browser.download.manager.showAlertOnComplete", False)
    # specify the directory where you want to download the files
    profile.set_preference("browser.download.dir", os.getcwd())
    # the content type/ list of MIME types to save to disk without asking what to use to open the file
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
    
    driver = webdriver.Firefox(firefox_options=options,executable_path=r'/Users/QiaoQiao/Documents/SeleniumProject/lib/geckodriver',firefox_profile = profile)
    driver.get(url)
    delay = 15
    WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.XPATH,"(.//*[normalize-space(text()) and normalize-space(.)='ISO3'])[1]/following::button[1]")))
    # select all the countries
    driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='ISO3'])[1]/following::button[1]").click()
    driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='ISO3'])[1]/following::button[1]").click()
    driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='chevron_right'])[2]/following::button[1]").click()
    driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='CPC'])[1]/following::i[212]").click()
    driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='CPC'])[1]/following::i[215]").click()
    driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='chevron_right'])[4]/following::input[1]").click()
    driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='chevron_right'])[4]/following::input[1]").clear()
    driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='chevron_right'])[4]/following::i[2]").click()
    driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='search'])[1]/following::button[1]").click()

if __name__ == "__main__":
    FAO_scraping()