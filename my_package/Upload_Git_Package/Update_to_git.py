import os
import shutil
from datetime import datetime

main_path = os.getcwd()


def check_exist(url):
    os.chdir('C:/Users/EF-QA-11/PycharmProjects/NoAutoGUI/TestCase_ver1.0')
    check = lambda x: os.path.exists(x)
    print("file exist? ", check(url))
    if check(url):
        os.system("git rm " + url)
    else:
        pass

def after_check_exis_upload():
    # print("local route: ", os.getcwd())
    os.system("git status")
    # print("*" * 10)
    os.system('git commit -m "Upload file"')
    os.system("git push")
    # print("*" * 10)
    os.chdir(main_path)

class git_update():
    def __init__(self):
        self.name = "git upload"
        self.main_path = os.getcwd()
    def WebUpload(self, filename, path, file_list):
        if len(path) > 1:
            for i, system in enumerate(path):
                for index, file in enumerate(file_list):
                    file.seek(0)
                    if system.split("_")[0] == "Windows":
                        check_exist(f"./Web/Windows/{filename[index]}")
                        after_check_exis_upload()
                        print('Save file: ', f"./TestCase_ver1.0/Web/Windows/{filename[index]}")
                        file.save(f"./TestCase_ver1.0/Web/Windows/{filename[index]}")
                        file.seek(0)
                        os.chdir(self.main_path + "/TestCase_ver1.0/Web/Windows")
                        os.system(f"git add {filename[index]}")
                        print(f"git add {filename[index]}")
                        os.chdir(self.main_path)
                    elif system.split("_")[0] == "Linux":
                        check_exist(f"./Web/Linux/{filename[index]}")
                        after_check_exis_upload()
                        file.save(f"./TestCase_ver1.0/Web/Linux/{filename[index]}")
                        file.seek(0)
                        os.chdir("TestCase_ver1.0/Web/Linux")
                        os.system(f'git add {filename[index]}')
                        os.chdir(self.main_path)
                    elif system.split("_")[0] == "Mac":
                        check_exist(f"./Web/Mac/{filename[index]}")
                        after_check_exis_upload()
                        file.save(f"./TestCase_ver1.0/Web/Mac/{filename[index]}")
                        file.seek(0)
                        os.chdir(self.main_path + "/TestCase_ver1.0/Web/Mac")
                        os.system(f'git add {filename[index]}')
                        os.chdir(self.main_path)
        else:
            print("file_list", file_list, len(file_list))
            for index, file in enumerate(file_list):
                print("File: ", file)
                System = path[0].split('_')[0]
                print("System:", System)
                if System == "Windows":
                    check_exist(f"./Web/Windows/{filename[index]}")
                    after_check_exis_upload()
                    print("Save File: ", f"./TestCase_ver1.0/Web/Windows/{filename[index]}")
                    file.save(f"./TestCase_ver1.0/Web/Windows/{filename[index]}")
                    file.seek(0)
                    os.chdir(self.main_path + "/TestCase_ver1.0/Web/Windows")
                    print(f"git add {filename[index]}")
                    os.system(f"git add {filename[index]}")
                    os.chdir(self.main_path)
                elif System == "Linux":
                    check_exist(f"./Web/Linux/{filename[index]}")
                    after_check_exis_upload()
                    file.save(f"./TestCase_ver1.0/Web/Linux/{filename[index]}")
                    file.seek(0)
                    os.chdir(self.main_path + "/TestCase_ver1.0/Web/Linux")
                    print(f"git add {filename[index]}")
                    os.system(f'git add {filename[index]}')
                    os.chdir(self.main_path)
                elif System == "Mac":
                    check_exist(f"./Web/Mac/{filename[index]}")
                    after_check_exis_upload()
                    file.save(f"./TestCase_ver1.0/Web/Mac/{filename[index]}")
                    file.seek(0)
                    os.chdir(self.main_path + "/TestCase_ver1.0/Web/Mac")
                    print(f"git add {filename[index]}")
                    os.system(f'git add {filename[index]}')
                    os.system("git commit -m 'Upload TestCase'")
                    os.chdir(self.main_path)
        print("----------------------------------------")
        os.chdir(self.main_path + "/TestCase_ver1.0/Web")
        os.system('git status')
        os.system('git commit -m "Upload TestCase"')
        os.system("git push")
        os.chdir(self.main_path)
        print("----------------------------------------")

    def ApiUpload(self, filename, path, file_list):
        print('-' * 6)
        print("path: ", path)
        if len(path) > 1:
            print("file_list", file_list)
            for i, system in enumerate(path):
                for index, file in enumerate(file_list):
                    if system.split("_")[0] == "Windows":
                        check_exist(f"./Api/Windows/{filename[index]}")
                        after_check_exis_upload()
                        file.save(f"./TestCase_ver1.0/Api/Windows/{filename[index]}")
                        file.seek(0)
                        os.chdir(self.main_path + "/TestCase_ver1.0/Api/Windows")
                        os.system(f'git add {filename[index]}')
                        os.chdir(self.main_path)
                    elif system.split("_")[0] == "Linux":
                        check_exist(f"./Api/Linux/{filename[index]}")
                        after_check_exis_upload()
                        file.save(f"./TestCase_ver1.0/Api/Linux/{filename[index]}")
                        file.seek(0)
                        os.chdir("TestCase_ver1.0/Api/Linux")
                        os.system(f'git add {filename[index]}')
                        os.chdir(self.main_path)
                    elif system.split("_")[0] == "Mac":
                        check_exist(f"./Api/Mac/{filename[index]}")
                        after_check_exis_upload()
                        file.save(f"./TestCase_ver1.0/Api/Mac/{filename[index]}")
                        file.seek(0)
                        os.chdir(self.main_path + "/TestCase_ver1.0/Api/Mac")
                        os.system(f'git add {filename[index]}')
                        os.chdir(self.main_path)
        else:
            for index, file in enumerate(file_list):
                System = path[0].split('_')[0]
                if System == "Windows":
                    check_exist(f"./Api/Windows/{filename[index]}")
                    after_check_exis_upload()
                    file.save(f"./TestCase_ver1.0/Api/Windows/{filename[index]}")
                    file.seek(0)
                    os.chdir(self.main_path + "/TestCase_ver1.0/Api/Windows")
                    os.system(f'git add {filename[index]}')
                    os.chdir(self.main_path)
                elif System == "Linux":
                    check_exist(f"./Api/Linux/{filename[index]}")
                    after_check_exis_upload()
                    file.save(f"./TestCase_ver1.0/Api/Linux/{filename[index]}")
                    file.seek(0)
                    os.chdir(self.main_path + "/TestCase_ver1.0/Api/Linux")
                    os.system(f'git add {filename[index]}')
                    os.chdir(self.main_path)
                elif System == "Mac":
                    check_exist(f"./Api/Mac/{filename[index]}")
                    after_check_exis_upload()
                    file.save(f"./TestCase_ver1.0/Api/Mac/{filename[index]}")
                    file.seek(0)
                    os.chdir(self.main_path + "/TestCase_ver1.0/Api/Mac")
                    print(f'git add {filename[index]}')
                    os.system(f'git add {filename[index]}')
                    os.system("git commit -m 'Upload TestCase'")
                    os.chdir(self.main_path)

        print("----------------------------------")
        os.chdir(self.main_path + "/TestCase_ver1.0/Api")
        os.system('git status')
        os.system('git commit -m "Upload TestCase"')
        os.system("git push")
        print("-----------------------------------")
        os.chdir(self.main_path)
        print('-' * 6)
        return "END"

    def AppUpload(self, filename, path, file_list):
        self.main_path = os.getcwd()
        print("path: ", path)
        if len(path) > 1:
            print('-------------------------------')
            print('path: ', path , len(path))
            print("file_list: ", file_list)
            print('-------------------------------')
            for i, system in enumerate(path):
                for index, file in enumerate(file_list):
                    if system.split("_")[0] == "Android":
                        check_exist(f'./App/{system.split("_")[0]}/{system.split("_")[1]}/{filename[index]}')
                        after_check_exis_upload()
                        file.save(f'./TestCase_ver1.0/App/{system.split("_")[0]}/{system.split("_")[1]}/{filename[index]}')
                        file.seek(0)
                        os.chdir(self.main_path + f'/TestCase_ver1.0/App/Android/' + {system.split("_")[1]})
                        os.system(f'git add {filename[index]}')
                        os.chdir(self.main_path)
                    elif system.split("_")[0] == "IOS":
                        check_exist(f'./TestCase_ver1.0/App/{system.split("_")[0]}/{system.split("_")[1]}/{filename[index]}')
                        after_check_exis_upload()
                        file.save(f'./TestCase_ver1.0/App/{system.split("_")[0]}/{system.split("_")[1]}/{filename[index]}')
                        file.seek(0)
                        os.chdir(self.main_path + f'/TestCase_ver1.0/App/IOS/' + {system.split("_")[1]})
                        os.system(f'git add {filename[index]}')
                        os.chdir(self.main_path)
        else:
            print("-----", filename)
            for index, file in enumerate(file_list):
                System = path[0].split('_')[0]
                folder = path[0].split('_')[1]
                if System == "Android":
                    check_exist(f"./TestCase_ver1.0/App/Android/{folder}/{filename[index]}")
                    after_check_exis_upload()
                    file.save(f"./TestCase_ver1.0/App/Android/{folder}/{filename[index]}")
                    file.seek(0)
                    os.chdir(self.main_path + f"/TestCase_ver1.0/App/Android/{folder}")
                    os.system(f'git add {filename[index]}')
                    os.chdir(self.main_path)
                elif System == "IOS":
                    check_exist(f"./TestCase_ver1.0/App/IOS/{path[0].split('_')[1]}/{filename[index]}")
                    after_check_exis_upload()
                    file.save(f"./TestCase_ver1.0/App/IOS/{path[0].split('_')[1]}/{filename[index]}")
                    file.seek(0)
                    os.chdir(self.main_path + f"/TestCase_ver1.0/App/IOS/{folder}")
                    os.system(f'git add {filename[index]}')
                    os.chdir(self.main_path)

        print("----------------------------------")
        os.chdir(self.main_path + "/TestCase_ver1.0/Api")
        os.system('git status')
        os.system('git commit -m "Upload TestCase"')
        os.system("git push")
        print("-----------------------------------")
        os.chdir(self.main_path)
        return "END"

    def Yaml_Save(self, Timenow,  filename, file_list):
        yaml_path = './Server_history_files'
        if len(file_list) > 1:
            for i, file in enumerate(file_list):
                if filename[i][-4:] == 'yaml':
                    print(yaml_path + '/' + Timenow + filename[i])
                    file.save(yaml_path + '/' + Timenow + " " + filename[i])
                    file.seek(0)
                    return "Save OK"
                else:
                    pass
        else:
            file = file_list[0]
            file.save(yaml_path + '/' + Timenow + " " +filename)
            return "Save OK"

    def Case_Ram(self, filename, path, file_list, account, casetype):
        print("path:", path)
        print("file_list: ", file_list)
        print("filename: ", filename)
        try:
            os.mkdir(f'./Vip_Ram_Folder/{account}')
            print(f"mkdir ./Vip_Ram_Folder/{account}")
        except FileExistsError:
            print("Folder Exists")
        try:
            os.mkdir(f'./Vip_Ram_Folder/{account}/{casetype}')
            print(f"mkdir ./Vip_Ram_Folder/{account}/{casetype}")
        except FileExistsError:
            print("Folder Exists")
        for i, file in enumerate(file_list):
            file.save(f'./Vip_Ram_Folder/{account}/{casetype}/{filename[i]}')
            file.seek(0)
        return "OK"
