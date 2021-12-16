from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from datetime import datetime
import time
import pyautogui

# Var
def get_time():
    Timenow = str(datetime.now().strftime("%Y-%m-%d %H%M%S"))
    return Timenow
# Log = []

def swipe_down(driver, x, y, start_y=0.25, stop_y=0.75, duration=1300):
    x1 = int(x * 0.5)
    y1 = int(y * start_y)
    x2 = int(x * 0.5)
    y2 = int(y * stop_y)
    # print x1,y1,x2,y2
    driver.swipe(300, 1000, 300, 300, duration)
    return "OK"

def swipe_up(driver, x, y, start_y=0.25, stop_y=0.75, duration=1300):
    x1 = int(x * 0.5)
    y1 = int(y * start_y)
    x2 = int(x * 0.5)
    y2 = int(y * stop_y)
    driver.swipe(300, 1000, 300, 300, duration)
    return "OK"

def Log_func(Log, *args):
    # global Log
    try:
        Final_Log = args[0] + ': ' + f"(status: {args[1]}, message: {args[2]}, drivertime: {args[3]})" + '\n'
    except:
        Final_Log = args[0] + ': ' + f"(status: {args[1]}, message: {args[2]}" + '\n'
    Log.append(Final_Log)

def take_log():
    global Log
    return Log

def Error_Screen_shot(WorkName, Timenow):
    try:
        img = pyautogui.screenshot(region=[0,0,1920,1080])
        filename = str(Timenow + " - " + WorkName)
        print("Error_Screen_shot: ", filename)
        img.save(f'../../../Log/Web/Error_Screen_Shot/App_WebCase_Error_Image/{filename}.png')
        return "File Save OK"
    except FileNotFoundError:
        print("Check Log Folder position")
        return "Error Image Save OK"

# App Feature
class appium_function():
    # PLATFORM_NAME, SYSTEM_VERSION, DEVICES_NAME, APPACTIVITY, noReset
    def __init__(self, Android_Version, browserName, udid):
        self.name = "appium_function"

        desired_caps = {
            "platformName": "Android",
            "platformVersion": Android_Version,
            "browserName": browserName,
            "udid": udid,
            "autoGrantPermissions": False
        }
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        driver.implicitly_wait(5)
        self.Log = []
        self.driver = driver

    def driver(self):
        return self.driver

    def url(self, url):
        try:
            st = time.time()
            self.driver.get(url)
            et = time.time()
            DriverTime = round(et - st, 4)
            Timenow = get_time()
            Log_func(self.Log, Timenow, "INFO", f"Go url ok", DriverTime)
            return {"Status": "Correct", "Message": "Get Url OK"}
        except:
            DriverTime = round(et - st, 4)
            Timenow = get_time()
            Log_func(self.Log, Timenow, "ERROR", "Go url Error", DriverTime)
            Error_Screen_shot("Go_url", Timenow)
            return {"Status": "Error", "Message": "Get Url Error"}
    # Find Element
    def find_id(self, *args):
        # 0: target 1: worktype 2: send value
        st = time.time()
        if args[0] == "click":
            try:
                self.driver.find_element_by_id(args[1]).click()
                et = time.time()
                DriverTime = round(et - st, 4)
                Timenow = get_time()
                Log_func(self.Log, Timenow, "INFO", "Find_ID click ok", DriverTime)
                return {"Status": "Correct", "Message": "Find_ID click ok"}
            except:
                et = time.time()
                DriverTime = round(et - st, 4)
                Timenow = get_time()
                Log_func(self.Log, Timenow, "ERROR", "Find_ID click error", DriverTime)
                Error_Screen_shot("Find_ID_Click", Timenow)
                return {"Status": "Error", "Message": "Find_ID Click Error"}
        elif args[0] == 'send_keys':
            try:
                self.driver.find_element_by_id(args[1]).send_keys(args[2])
                et = time.time()
                DriverTime = round(et - st, 4)
                Timenow = get_time()
                Log_func(self.Log, Timenow, "INFO", "Find_ID Send_key ok", DriverTime)
                return {"Status": "Correct", "Message": "Find_ID send_keys ok"}
            except:
                DriverTime = round(et - st, 4)
                Timenow = get_time()
                Log_func(self.Log, Timenow, "ERROR", "Message Send_keys Error", DriverTime)
                Error_Screen_shot("Find_ID_Send_keys", Timenow)
                return {"Status": "Error", "Message": "Send_keys Error"}
    def find_xpath(self, *args):
        # 0: target 1: worktype 2: send value
        st = time.time()
        if args[0] == "click":
            try:
                self.driver.find_element_by_xpath(args[1]).click()
                et = time.time()
                DriverTime = round(et - st, 4)
                Timenow = get_time()
                Log_func(self.Log, Timenow, "INFO", "Find_Xpath Click OK", DriverTime)
                return {"Status": "Correct", "Message": "Find_Xpath click ok"}
            except:
                et = time.time()
                DriverTime = round(et - st, 4)
                Timenow = get_time()
                Log_func(self.Log, Timenow, "ERROR", "Find_Xpath Click Error", DriverTime)
                Error_Screen_shot("Find_Xpath_Click", Timenow)
                return {"Status": "Error", "Message": "Find_XPATH Click Error"}
        elif args[0] == 'send_keys':
            try:
                self.driver.find_element_by_xpath(args[1]).send_keys(args[2])
                et = time.time()
                DriverTime = round(et - st, 4)
                Timenow = get_time()
                Log_func(self.Log, Timenow, "INFO", "Find_Xpath Send_keys OK", DriverTime)
                return {"Status": "Correct", "Message": "Find_Xpath Send_keys ok"}
            except:
                et = time.time()
                DriverTime = round(et - st, 4)
                Timenow = get_time()
                Log_func(self.Log, Timenow, "ERROR", "FIND_Xpath Send_keys Error", DriverTime)
                Error_Screen_shot("Find_Xpath_Send_keys", Timenow)
                return {"Status": "Error", "Message": "Find_XPATH Send_keys Error"}

    def find_accessibility_id(self, *args):
        # 0: target 1: worktype 2: send value
        st = time.time()
        if args[0] == "click":
            try:
                self.driver.find_element_by_accessibility_id(args[1]).click()
                et = time.time()
                DriverTime = round(et - st, 4)
                Timenow = get_time()
                Log_func(self.Log, Timenow, "INFO", "Find_accessibility_id Click OK", DriverTime)
                return {"Status": "Correct", "Message": "Find_accessibility_id Click ok"}
            except:
                et = time.time()
                DriverTime = round(et - st, 4)
                Timenow = get_time()
                Log_func(self.Log, Timenow, "ERROR", "Find_accessibility_id Click Error", DriverTime)
                Error_Screen_shot("Find_accessibility_id_Click", Timenow)
                return {"Status": "Error", "Message": "Find_accessibility_id Click Error"}
        elif args[0] == 'send_keys':
            try:
                self.driver.find_element_by_accessibility_id(args[1]).send_keys(args[2])
                et = time.time()
                DriverTime = round(et - st, 4)
                Timenow = get_time()
                Log_func(self.Log, Timenow, "ERROR", "Find_accessibility_id Send_keys OK", DriverTime)
                return {"Status": "Correct", "Message": "Find_accessibility_id Send_keys ok"}
            except:
                et = time.time()
                DriverTime = round(et - st, 4)
                Timenow = get_time()
                Log_func(self.Log, Timenow, "ERROR", "Find_accessibility_id Send_keys Error", DriverTime)
                Error_Screen_shot("Find_accessibility_id_Send_keys", Timenow)
                return {"Status": "Error", "Message": "Find_accessibility_id Send_keys Error"}

    def find_css(self, *args):
        # 0: target 1: worktype 2: send value
        st = time.time()
        if args[0] == "click":
            try:
                self.driver.find_elements_by_css_selector(args[1]).click()
                et = time.time()
                DriverTime = round(et - st, 4)
                Timenow = get_time()
                Log_func(self.Log, Timenow, "INFO", "Find_css Click OK", DriverTime )
                return {"Status": "Correct", "Message": "Find_css Click ok"}
            except:
                et = time.time()
                DriverTime = round(et - st, 4)
                Timenow = get_time()
                Log_func(self.Log, Timenow, "ERROR", "Find_css Error", DriverTime)
                Error_Screen_shot("Find_css_Click", Timenow)
                return {"Status": "Error", "Message": "Find_css Click Error"}

        elif args[0] == 'send_keys':
            try:
                self.driver.find_elements_by_css_selector(args[1]).send_keys(args[2])
                et = time.time()
                DriverTime = round(et - st, 4)
                return {"Status": "Correct", "Message": "Find_css Send_keys ok"}
            except:
                et = time.time()
                DriverTime = round(et - st, 4)
                Timenow = get_time()
                Log_func(self.Log, Timenow, "ERROR", "Find_css Error", DriverTime)
                Error_Screen_shot("Find_css_Send_keys", Timenow)
                return {"Status": "Error", "Message": "Find_css Send_keys Error"}

    def find_link_text(self, *args):
        # 0: target 1: worktype 2: send value
        st = time.time()
        if args[0] == "click":
            try:
                self.driver.find_element_by_link_text((args[1])).click()
                et = time.time()
                DriverTime = round(et - st, 4)
                Timenow = get_time()
                Log_func(self.Log, Timenow, "INFO", "Find_link_text Click OK", DriverTime)
                return {"Status": "Correct", "Message": "Find_link_text Click ok"}
            except:
                et = time.time()
                DriverTime = round(et - st, 4)
                Log_func(self.Log, Timenow, "ERROR", "Find_css Error", DriverTime)
                Error_Screen_shot("Find_link_text_Click", Timenow)
                return {"Status": "Error", "Message": "Find_css Click Error"}
        elif args[0] == 'send_keys':
            try:
                st = time.time()
                self.driver.find_element_by_link_text((args[1])).send_keys(args[2])
                et = time.time()
                DriverTime = round(et - st, 4)
                Timenow = get_time()
                Log_func(self.Log, Timenow, "INFO", "Find_link_text Send_keys OK", DriverTime)
                return {"Status": "Correct", "Message": "Find_link_text Send_keys ok"}
            except:
                et = time.time()
                DriverTime = round(et - st, 4)
                Timenow = get_time()
                Log_func(self.Log, Timenow, "ERROR", "Find_link_text Send_keys", DriverTime)
                Error_Screen_shot("Find_link_text_send_keys", Timenow)
                return {"Status": "Error", "Message": "Find_link_text Send_keys Error"}

    def delete_cookie(self):
        self.driver.delete_all_cookies()
        return

    # Touch Screen
    def click_Work(self, x, y):
        st = time.time()
        try:
            TouchAction(self.driver).tap(x=x, y=y).perform()
            et = time.time()
            DriverTime = round(et - st, 4)
            Timenow = get_time()
            Log_func(Timenow, "INFO", "Click Work OK", DriverTime)
            return {"Status": "Correct", "Message": "Find_link_text Send_keys ok"}
        except:
            et = time.time()
            DriverTime = round(et - st, 4)
            Timenow = get_time()
            Log_func(Timenow, "ERROR", "Click Work Error")
            Error_Screen_shot("Click_Work", Timenow)
            return {"Status": "Error", "Message": "Find_link_text Send_keys Error"}

    def scroll_down(self):
        st = time.time()
        try:
            swipe_down()
            et = time.time()
            DriverTime = round(et - st, 4)
            Timenow = get_time()
            Log_func(Timenow, "INFO", "Scroll_Down OK", DriverTime)
            return {"Status": "Correct", "Message": "Scroll_Down ok"}
        except:
            et = time.time()
            DriverTime = round(et - st, 4)
            Log_func(Timenow, "ERROR", "Scroll_Down OK", DriverTime)
            Error_Screen_shot("Scroll_Down", Timenow)
            return {"Status": "Error", "Message": "Scroll_Down Error"}
    def scroll_up(self, driver, x ,y):
        st = time.time()
        try:
            swipe_up(driver, x, y)
            et = time.time()
            DriverTime = round(et - st, 4)
            Timenow = get_time()
            Log_func(Timenow, "INFO", "Scroll_Up OK", DriverTime)
            return {"Status": "Correct", "Message": "Scroll_Up ok"}
        except:
            et = time.time()
            DriverTime = round(et - st, 4)
            Timenow = get_time()
            Log_func(Timenow, "ERROR", "Scroll_Up OK", DriverTime)
            Error_Screen_shot("Scroll_Up", Timenow)
            return {"Status": "Error", "Message": "Scroll_Up Error"}

    def control_number(self, number):
        self.driver.keyevent(int(number))
        return "OK"
