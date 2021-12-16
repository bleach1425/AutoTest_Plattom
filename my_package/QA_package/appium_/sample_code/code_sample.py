from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

class appium_setting():
    def __init__(self):
        """:parameter
        can input parameter to setting desired_caps
        """
        pass
        desired_caps = {
            "platformName": "Android",
            "platformVersion": "11",
            "browserName": "Chrome",
            "autoGrantPermissions": False
        }
        self.chrome = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.chrome.implicitly_wait(5)
    def start(self):
        """
        module log
        """
        # Browser
        self.chrome.get("url")
        # Click
        TouchAction(self.driver).tap(x=1, y=1).perform()
        # App
        self.chrome.find_element_by_xpath('測試').click()
        self.chrome.find_element_by_link_text('測試').click()
        self.chrome.find_element_by_id('測試').click()
        self.chrome.find_element_by_ac('測試').click()
        self.chrome.find_element_by_accessibility_id('測試').click()
        return