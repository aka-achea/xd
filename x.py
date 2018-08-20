#!/usr/bin/python
#coding:utf-8

import os  ,time
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  

web = 'https://www.xiami.com/album/2103925313?spm=0.0.0.0.bT0jrT'
# web = 'E:\\11.html'

chrome_options = Options()  
# chrome_options.add_argument("headless") 
# chrome_options.add_argument("no-sandbox") 
# chrome_options.add_argument('user-data-dir="E:\\xm"')  
# cpath = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
# chrome_options.binary_location = cpath    
chrome_drive = "D:\\doc\\OneDrive\\script\\xd\\chromedriver.exe"

browser_arg = [" --log-path=e:\chrome.log"," --verbose"]

browser = webdriver.Chrome( executable_path=chrome_drive,
    service_args=[browser_arg[0]])
    # chrome_options=chrome_options)  
browser.get(web)  
time.sleep(2)
# print(browser)

source = browser.page_source
print(source)

# time.sleep(2)
# content = browser.find_elements_by_class_name('chkbox')

# for i in content:
#     print(i)
#     print(i.get_attribute('innerHTML'))

browser.close()
browser.quit()

