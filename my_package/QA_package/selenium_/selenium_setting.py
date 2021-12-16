from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui
import os

class func():
    def __init__(self):
        pass
    def func_selenium_setting(self):
        options = Options()
        options.add_argument("--disable-notifications")
        chrome = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
        return chrome


