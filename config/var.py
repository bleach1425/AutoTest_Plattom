from random import Random

class save_var:
    def __init__(self):
        #　dict
        self.ChoiceJob = {}
        self.Ram_CaseNumber = {}
        self.Agent_Work_List = {}
        self.Agent_list = {}
        self.ApiSaveDict = {}
        self.Work_list = {}
        # list
        self.System_queue = []
        self.Agent_List = []
        # num
        self.num = 0
        # (-------------------------)
        self.Linux_Completeness = 0
        self.Windows_Completeness = 0
        self.Mac_Completeness = 0
        self.Completeness = 0
        # (-------------------------)
        self.Linux_Api_Completeness = 0
        self.Linux_Web_Completeness = 0
        self.Windows_Api_Completeness = 0
        self.Windows_Web_Completeness = 0
        self.Mac_Api_Completeness = 0
        self.Mac_Web_Completeness = 0
        # (-------------------------)
        self.Android_Browser_Completeness = 0
        self.Android_App_Completeness = 0
        self.IOS_Browser_Completeness = 0
        self.IOS_App_Completeness = 0
        # (-------------------------)
        # Booling
        self.CheckApiCase = False
    def reset(self):
        self.ChoiceJob['Api_System'] = ""
        self.ChoiceJob['Api_Job'] = ""
        self.ApiSaveDict['System'] = ""
        self.ApiSaveDict['Title'] = ""
