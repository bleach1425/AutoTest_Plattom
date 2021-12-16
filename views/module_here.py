import sys
sys.path.append('../')
from __init__ import *
from config.var import *
from models.models import User
from models.forms import LoginForm, RegistrationForm

# My Package
from my_package.Upload_Git_Package import Gitpath_setting, Update_to_git
from my_package.jstree_process.jstree_process import tree
from my_package.Queue_setting import Queue_setting
from copy import deepcopy
Git_func = Update_to_git.git_update()
queue = Queue_setting.deal_queue()

# Emergency var
path = ''

class module_common:
    def __init(self):
        pass

    def module_index(self, *param):
        save = param[0]
        account = session.get('account')
        cursor.execute('SELECT * FROM `machine_status`')
        data = cursor.fetchall()
        save.Agent_list = [n[2] for n in data if n[3] == "Offline"]
        return account, data, save.Agent_list

    def module_login(self, *param):
        form = param[0]
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.check_password(form.password.data) and user is not None:
                login_user(user)
                # next = request.args.get('next')
                # print('next: ', next)
                # if next == None or not next[0] == '/':
                next = url_for('index')
                session['account'] = user.username
                return next
                # else:
                #     return []
        else:
            return None

    def module_savework(self, *param):
        '''
        Save casestatus to `schedule_management`
        '''
        # Data
        JSON = param[0]
        CaseNumber = param[1]
        account = session.get('account')
        system = JSON['System']
        status = JSON["Status"]
        casetype = JSON['CaseType']
        CreatTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        WorkStatus = "Doing"
        session['CaseNumber'] = CaseNumber
        session.permanent = True
        # Catch Select
        testcase = [row['text'] for row in JSON['Data']]
        casestatus = "[]"
        if 'FileName' in JSON:
            filename = JSON['FileName']
            sql = f'INSERT INTO `schedule_management`(`CaseNumber`, `CreateTime`, `Account`, `System`, `Casetype`, `TestCase`, `Status`, `CaseStatus`, `WorkStatus`, `Completeness`, `FileName`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (CaseNumber, CreatTime, account, system, casetype, r'{}'.format(testcase), str(status), str(casestatus),str(WorkStatus), '0%', str(filename)))
        else:
            sql = f'INSERT INTO `schedule_management`(`CaseNumber`, `CreateTime`, `Account`, `System`, `Casetype`, `TestCase`, `Status`, `CaseStatus`, `WorkStatus`, `Completeness`, `FileName`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (CaseNumber, CreatTime, account, system, casetype,  r'{}'.format(testcase), str(status), str(casestatus), str(WorkStatus), '0%', ''))
        db_.commit()
        #  Send Data to Ram Folder

    def module_updatecasenumber(self, *param):
        '''
        Update casenumber from `machine_status`
        '''
        JSON = param[0]

        CaseName = JSON['CaseName']
        CaseNumber = JSON['CaseNumber']
        system = JSON['System'] # [0]
        for n in system:
            sql = f'UPDATE `machine_status` SET `CaseName`="{CaseName}",`Status`="Online",  `CaseNumber`="{CaseNumber}" WHERE `System`="{n}"'
            data_num = cursor.execute(sql)
            data = cursor.fetchall()

    def module_process(self, *param):
        '''
        if system busy, add to system_queue
        '''
        data = param[0]
        save = param[1]
        casenumber = param[2]
        testcase = []
        for n in data['Select']:
            try:
                testcase.append(n['original']['text'])
            except:
                testcase.append(n['original'])

        data['Select'] = testcase
        # param
        System = data['System']
        data['CaseNumber'] = casenumber

        if len(System) >=1:
            for system in System[0]:
                save.System_queue.append({system: data})
        else:
            save.System_queue.append({System[0][0]: data})

    def module_clear(self, *param):
        save = param[0]
        sql = ' UPDATE `machine_status` SET `CaseName`="",`Status`="Offline",`Completeness`="100%",`CaseNumber`= "" '
        sql1 = ' DELETE FROM `schedule_management` WHERE `Completeness` != "100%" '
        cursor.execute(sql)
        db_.commit()
        cursor.execute(sql1)
        db_.commit()
        cursor.execute("SELECT * FROM `machine_status`")
        data = cursor.fetchall()
        save.Agent_list = [n[2] for n in data if n[3] == "Offline"]
        account = session.get('account')

    def module_backstage_layer(self, *param):
        server_ip_socket = param[0]
        CaseNumber = param[1]
        target = []
        account = session.get('account')
        if account == None:
            return redirect(url_for("login"))
        time.sleep(1)
        account = session.get('account')
        sql = f"SELECT * FROM `schedule_management` WHERE `Account`='{account}' ORDER BY `CreateTime` DESC LIMIT 50"
        data_num = cursor.execute(sql)
        data = cursor.fetchall()
        if data_num == 1:
            CREATE_TIME = data[0][2]
            CASE_NUMBER = data[0][1]
            CASE_CONTENT = data[0][6]
            CASE_TYPE = data[0][5]
            WORK_STATUS = data[0][-3]
            SYSTEM = data[0][4]
            target = [data[0][2], data[0][1], data[0][4], data[0][5]]
            #
            DA = {
                "Data": target
            }
            return  data_num, CREATE_TIME, CASE_NUMBER,\
                CASE_CONTENT, WORK_STATUS,\
                SYSTEM, target, CASE_TYPE

        elif data_num > 1:
            CREATE_TIME = []
            CASE_NUMBER = []
            CASE_CONTENT = []
            WORK_STATUS = []
            CASE_TYPE = []
            SYSTEM = []
            for i, n in enumerate(data):
                CREATE_TIME.append(n[2])
                CASE_NUMBER.append(n[1])
                CASE_TYPE.append(n[5])
                CASE_CONTENT.append(n[6])
                WORK_STATUS.append(n[-3])
                SYSTEM.append(n[4])
                target.append([n[2], n[1], n[4], n[5]])
            DA = {
                "Data": target
            }
            DA = json.dumps(DA)
            return  data_num, CREATE_TIME, CASE_NUMBER,\
                    CASE_CONTENT, WORK_STATUS,\
                    SYSTEM, target, CASE_TYPE

    def module_Reset_Work(account, *args):
        global ChoiceJob, ApiSaveDict, WebSaveDict
        # Clear Vip ram folder
        casetype = ['Api', 'Web', 'App', 'AI_model']
        try:
            Exist_folder = [n for n in casetype if n in os.listdir(f'../Vip_Ram_Folder/{account}')]
        except FileNotFoundError:
            os.mkdir(f'Vip_Ram_Folder/{account}')
        if not args:
            try:
                for folder in Exist_folder:
                    for n in os.listdir(f'../Vip_Ram_Folder/{account}/{folder}'):
                        try:
                            os.remove(f'../Vip_Ram_Folder/{account}/{folder}/{n}')
                        except PermissionError:
                            pass
            except:
                pass
        else:
            try:
                for folder in Exist_folder:
                    for n in os.listdir(f'../Vip_Ram_Folder/{account}/{folder}'):
                        try:
                            if n == args[0]:
                                shutil.rmtree(f'../Vip_Ram_Folder/{account}/{folder}/{args[0]}')
                        except PermissionError:
                            pass
            except:
                pass
        # Reset All Dict
        ChoiceJob = {}  # vip user save
        ApiSaveDict = {}  # Api normal user save
        WebSaveDict = {}  # Web normal user save
        return "Reset OK"




class module_api:
    def __init__(self):
        pass

    def module_envapi(self, *param):
        global Server_ip
        account = session.get('account')
        # ("------------------------------------------------")
        sql = "SELECT * FROM `machine_status` ORDER BY `machine_status`.`id` ASC"
        cursor.execute(sql)
        data = cursor.fetchall()
        # ("------------------------------------------------")
        Search_identity = "select identity from userdata where Account=%s"
        cursor.execute(Search_identity, (account,))
        identity = cursor.fetchall()[0][0]
        if identity == 'S':
            if not os.path.isdir("Vip_Ram_Folder"):
                os.mkdir("Vip_Ram_Folder")
                if not os.path.isdir(f"Vip_Ram_Folder/{account}"):
                    os.mkdir(f'./Vip_Ram_Folder/{account}')
        # Git pull
        Gitpath_setting.Gitpath("Api")
        return account, data

    def filecatch_api(self, *param):
        global path
        '''
        1. Catch file add to ChoiceJob
        2. Upload to Git
        3. Create Case_Ram file in Vip_Ram_Folder
        '''
        save = param[0]
        data = param[1]
        file_list = param[2]
        # System Time
        Timenow = str(time.strftime("%Y-%m-%d %H.%M.%S", time.localtime()))
        # Catch Data
        testcase = []
        account = session.get('account')
        # Save File
        try:
            filename = [n.filename for n in file_list]
            session['filename'] = filename
            if len(save.ChoiceJob[account]) >= 1:
                for n in save.ChoiceJob[account]:
                    n['filename'] = filename
            else:
                save.ChoiceJob[account]["filename"] = filename
            Git_func.ApiUpload(filename=filename, path=path, file_list=file_list)
            Git_func.Case_Ram(filename=filename, path=path, file_list=file_list, account=account, casetype='Api')
        except:
            pass

        # deal with Data
        if data != None:
            for n in data['Select']:
                try:
                    testcase.append(n['original']['text'])
                except:
                    testcase.append(n['original'])
            # Check and Save to Git
            if len(testcase) > 1:
                path = [n for n in testcase if n != "Main"]
                for i, item in enumerate(testcase):
                    if item != "Main":
                        if account not in save.ChoiceJob:
                            if "_" in item:
                                save.ChoiceJob[account] = [{"job": item}]
                        else:
                            save.ChoiceJob[account].append({"job": item})
            else:
                path = copy.deepcopy(testcase)

    def module_envapi_9(self, *param):
        title = request.args['title']
        session['title'] = title

    def module_vip_history_page_api(self, *param):
        account = session.get('account')
        # account = 'asd'
        identity = 'S'
        casetype = 'api'
        CaseNumber_list = os.listdir(f'Vip_Ram_Folder/{account}/{casetype}')
        # SQL
        cursor.execute('SELECT * FROM `schedule_management` WHERE `FileName`!="" ORDER BY `CreateTime` DESC')
        data = cursor.fetchall()
        # Var
        jstree_data = []
        CT = []
        CN = []
        FN = []
        for row in data:
            for casenumber in CaseNumber_list:
                if casenumber == row[1]:
                    CN.append(row[1])
                    CT.append(row[5])
                    FN.append(os.listdir(f'./Vip_Ram_Folder/{account}/{casetype}/{casenumber}'))
                    tree = jstree_process.Vip_history_yaml_process(row[5], row[1], [n for n in eval(row[-1]) if n.split('.')[1] == 'yaml'][0], account)
                    jstree_data.append(tree)
        cursor.execute("SELECT `Status` FROM `machine_status`")
        Status = cursor.fetchall()
        JSON = {
            "Data": Status,
            "CaseType": CT,
            "CaseNumber": CN,
            "CaseName": "TestPlan",
            "FileName": FN,
            "Account": account,
            "identity": identity
        }

    def module_checkboxtree_api(self, *param):
        # Var
        save = param[0]
        CaseNumber = param[1]
        ApiSaveDict = save.ApiSaveDict
        casetype = 'Api'
        account = session.get('account')

        # In order not to delete the case by mistake save access the case number to Ram_CaseNumber dict
        save.Ram_CaseNumber[account] = CaseNumber
        # SQL Take User_identity
        Search_identity = f'SELECT `identity` FROM `userdata` WHERE `Account`="{account}"'
        cursor.execute(Search_identity)
        identity_data = cursor.fetchall()
        try:
            User_identity = identity_data[0][0]
        except:
            return redirect(url_for('base'))
        # Var
        System_list = []
        Filename_list = []
        result_list = []
        # SQL
        Completeness = 0
        sql = "SELECT `Status` FROM `machine_status`"
        data_num = cursor.execute(sql)
        data = cursor.fetchall()

        casetype = "Api"
        # identity
        if User_identity == "S":
            # Vip history file save
            if len(os.listdir(f'./Vip_Ram_Folder/{account}/{casetype}')) >= 0:
                os.mkdir(f'./Vip_Ram_Folder/{account}/{casetype}/{CaseNumber}')
                for file in os.listdir(f'./Vip_Ram_Folder/{account}/{casetype}'):
                    if os.path.isdir(f"./Vip_Ram_Folder/{account}/{casetype}/{file}"):
                        pass
                    else:
                        shutil.move(f"./Vip_Ram_Folder/{account}/{casetype}/" + file, f'./Vip_Ram_Folder/{account}/{casetype}/{CaseNumber}')
            try:
                yamlname = [n for n in save.ChoiceJob[account][0]['filename'] if '.yaml' in n][0]
                for i, num in enumerate(save.ChoiceJob[account]):
                    System = num['job'].split('_')[0]
                    System_list.append(System)
                    Job = num['job'].split('_')[1]
                    filename = num['filename']
                    Filename_list.append(filename)
                title = session.get('title')
                JSON = {
                    "Data": data,
                    "CaseType": casetype,
                    "CaseName": title,
                    "CaseNumber": CaseNumber,
                    "System": System_list,
                    "FileName": Filename_list[0],
                    "Account": account,
                    "identity": User_identity
                }

                for n in System_list:
                    result = queue.Dispatch_task(save.Agent_list, n, save.System_queue)
                    result_list.append(result)

                try:
                    jstree = tree.Process_yaml_api(casetype, System_list[0], yamlname)
                except:
                    return redirect(url_for('index'))
                JSON = json.dumps(JSON)

            except:
                System = [ApiSaveDict['System']]
                title = ApiSaveDict['Title']
                JSON = {
                    "Data": data,
                    "CaseType": casetype,
                    "CaseName": title,
                    "CaseNumber": CaseNumber,
                    "System": [System],
                    "Account": account
                }
                result_list = []
                for n in System:
                    result = queue.Dispatch_task(save.Agent_list, n, save.System_queue)
                    result_list.append(result)
            JSON = json.dumps(JSON)
            return JSON, title, data, result_list, User_identity, jstree
        else:
            System = [ApiSaveDict['System']]
            title = ApiSaveDict['Title']
            JSON = {
                "Data": data,
                "CaseType": casetype,
                "CaseName": title,
                "CaseNumber": CaseNumber,
                "System": [System],
                "Account": account
            }
            result_list=[]
            for n in range(len(System)):
                result = queue.Dispatch_task(save.Agent_list, System, save.System_queue)
                result_list.append(result)
            JSON = json.dumps(JSON)
            jstree = None
            return JSON, title, data, result_list, User_identity, jstree

    def module_windows_api(self, *param):
        save = param[0]
        data = param[1]
        testcase = []
        for n in data['Select']:
            try:
                testcase.append(n['original']['text'])
            except:
                testcase.append(n['original'])
        save.Agent_Work_List["Windows_APICase"] = len(testcase)
        r = requests.post(Windows_Api_agent, json=data)
        print("Send result: ", r.status_code)
        return r.status_code

    def module_from_windows_api(self, *param):
        system = 'Windows'
        data = param[0]
        save = param[1]
        CaseNumber = param[2]
        account = data['account']
        if data['job'] == "Info":
            save.num += (2 * data['Runtime'])
            if account not in save.Work_list:
                save.Work_list[account] = []
                save.Work_list[account].append({"Windows_ApiCase": CaseNumber})
            else:
                save.Work_list[account].append({"Windows_ApiCase": CaseNumber})
        if data['job'] == "Finish":
            Final_Completeness = "100%"
            updata = data['data']
            # Update Item Status
            sql = f'UPDATE `schedule_management` SET `CaseStatus` = "{updata}", `WorkStatus`="FINISH", `Completeness`="{Final_Completeness}" WHERE `CaseNumber` = "{CaseNumber}" AND `System` = "{system}"'
            cursor.execute(sql)
            db_.commit()
            # Update Completeness
            sql1 = f'UPDATE `machine_status` SET `Completeness`="{Final_Completeness}",`CaseName`="", `Status`="Offline", `CaseNumber`="" WHERE `System` = "{system}"'
            cursor.execute(sql1)
            print("最後的SQL: ", sql)
            print("最後的SQL1: ", sql1)
            db_.commit()
            # reset
            save.ChoiceJob['Api_System'] = ""
            save.ChoiceJob['Api_Job'] = ""
            save.ApiSaveDict['System'] = ""
            save.ApiSaveDict['Title'] = ""
            print("-----------Reset----------")
            delete = [i for (i, n) in enumerate(save.Work_list[account]) if 'Windows_ApiCase' in n][0]
            print("delete: ", delete)
            print('Work_list: ', save.Work_list)
            save.Work_list[account].pop(delete)
            save.num = 0
            return "FINISH"
        try:
            schedule = 100 / save.num
        except:
            if ZeroDivisionError:
                print("Pass ZeroDivisionError")
                print("Set schedule = 0")
                schedule = 0

        if save.Windows_Api_Completeness >= 99:
            print("進入最後的判斷:--------------------------------------")
            Final_Completeness = "100%"
            updata = data['data']
            # Update Item Status
            sql = f'UPDATE `schedule_management` SET `CaseStatus` = "{updata}", `WorkStatus`="FINISH", `Completeness`="{Final_Completeness}" WHERE `CaseNumber` = "{CaseNumber}" AND `System` = "{system}"'
            cursor.execute(sql)
            db_.commit()
            # Update Completeness
            sql1 = f'UPDATE `machine_status` SET `Completeness`="{Final_Completeness}",`CaseName`="", `Status`="Offline", `CaseNumber`="" WHERE `CaseNumber` = "{CaseNumber}" AND `System` = "{system}"'
            cursor.execute(sql1)
            print("最後的SQL: ", sql)
            print("最後的SQL1: ", sql1)
            db_.commit()
            save.Windows_Api_Completeness = 0
            save.num = 0
            return "FINISH"
        else:
            New_CaseNumber = [n for n in save.Work_list[account] if 'Windows_ApiCase' in n][0]['Windows_ApiCase']
            save.Windows_Api_Completeness += schedule
            Final_Completeness = str(round(save.Windows_Api_Completeness)) + "%"
            updata = data['data']
            # Update Item Status
            sql = f'UPDATE `schedule_management` SET `CaseStatus` = "{updata}", `Completeness`="{Final_Completeness}" WHERE `CaseNumber` = "{New_CaseNumber}" AND `System` = "{system}"'
            cursor.execute(sql)
            db_.commit()

            # Update Compeleteness
            sql1 = f'UPDATE `machine_status` SET `Completeness` = "{Final_Completeness}", `Status`="Online" WHERE `CaseNumber` = "{New_CaseNumber}" AND `System` = "{system}"'
            print("Windows schedule_management: ", sql)
            print("Windows machine_status更新狀態: ", sql1)
            cursor.execute(sql1)
            # print(sql1)
            db_.commit()
            return "OK"


