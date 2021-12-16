from flask import Flask, request, render_template,\
                  redirect, url_for, send_file
from selenium import webdriver
import os, io
import MySQLdb
import yaml
import requests
import pyautogui
import time
import shutil
import threading
import subprocess


# Setting
app = Flask(__name__)
# git_path = os.getcwd() + "/Api/Api"
filename = ""
imagename = ""
main_path = os.path.join(os.path.dirname(os.getcwd()))

def driver(account):
    os.system(f"start python Windows_WebCase_ver1.0.py {account}")
    return "OK"

def target_path(CaseType, System):
    git_path = main_path + f"/{CaseType}/{CaseType}/{System}"
    return git_path

def App_target_path(CaseType, System, worktype):
    git_path = main_path + f"/{CaseType}/{CaseType}/{System}/{worktype}"
    return git_path

@app.route("/", methods=["GET", "POST"])
def index():
    return "Server is Work"
@app.route("/WebCase", methods=["POST"])
def WebCase():
    # data
    os.chdir(main_path)
    data = request.get_json()
    CaseNumber = data['CaseNumber']
    if "FileName" not in data:
        print("No FileName")
        account = data['Account']
        # Git
        git_path = target_path("Web", "Windows")
        if os.path.exists('Web'):
            os.system('rd /s /q Web')
        os.system('git clone https://github.com/bleach1425/TestCase_ver1.0.git Web/')
        os.chdir(git_path)
        os.system("git pull")
        # Get Post
        print("---------------------------")
        print("driver start")
        p = subprocess.Popen(f'start python Web_example.py {account} {CaseNumber}', shell=Trueㄑ)
        p.communicate()
        p.wait()
        os.chdir(main_path)
        time.sleep(5)
        return "OK"
    else:
        print("++++++++++++++++++++++++++++++++++++++++++")
        account = data['Account']
        filename = ''
        imagename = ''
        for file in data['FileName']:
            if file.split('.')[1] == 'yaml':
                filename = file
                print("yaml filename", filename)
            else:
                imagename = file
                print("imagename", imagename)
        # # Git
        git_path = target_path("Web", "Windows")
        if os.path.exists('./Web'):
            os.system('rd /s /q Web')
        os.system('git clone https://github.com/bleach1425/TestCase_ver1.0.git Web/')
        os.chdir(git_path)
        os.system("git pull")
        # # Get Post
        print('--------------------------------')
        print("driver start")
        os.system(f'start python Windows_WebCase_ver1.0.py {account} {filename} {CaseNumber} &')
        print("driver end")
        print('--------------------------------')
        os.chdir(main_path)
        return "OK"

@app.route("/APICase", methods=['GET', 'POST'])
def APICase():
    os.chdir(main_path)
    if os.path.exists('Api'):
        os.system('rd /s /q Api')
        time.sleep(3)
    data = request.get_json()
    if request.method == "GET":
        return "Error"
    elif request.method == "POST":
        account = data['Account']
        # Git
        git_path = target_path("Api", "Windows")
        print(os.path.exists('Api'))
        os.system('git clone https://github.com/bleach1425/TestCase_ver1.0.git Api/')
        os.chdir(git_path)
        os.system("git pull")
        CaseNumber = data['CaseNumber']
        # Get Post
        if "FileName" in data:
            print('Have FileName')
            filename = ''
            imagename = ''
            print(data['FileName'], type(data['FileName']))
            for file in data['FileName']:
                if file.split('.')[1] == 'yaml':
                    filename = file
                    print("yaml filename", filename)
                else:
                    imagename = file
                    print("imagename", imagename)
            if 'imagename' != '':
                time.sleep(5)
                print('*'*6)
                print("local: ", os.getcwd())
                print(f"start python [Clear]_APITestCase_Windows.py {account} {filename} {imagename} {CaseNumber} &")
                os.system(f"start python [Clear]_APITestCase_Windows.py {account} {filename} {imagename} {CaseNumber} &")
                print('*' * 6)
                time.sleep(2)
                os.chdir(main_path)
                time.sleep(5)
                return "OK"
            else:
                print("-------------------------image not in local------------------------------")
                # os.system(f"start python APITestCase_Windows.py {account} {filename} {CaseNumber} &")
                print('*' * 6)
                os.system(f"start python [Clear]_APITestCase_Windows.py {account} {filename} {imagename} {CaseNumber} &")
                print('*' * 6)
                time.sleep(2)
                print("---FileName---", data['FileName'])
                os.chdir(main_path)
                return "OK"
        else:
            print("Don't have FileName, Do Example")
            filename = "Example.yaml"
            imagename = "test.dcm"
            time.sleep(5)
            os.system(f"start python Api_Example.py {CaseNumber} &")
            time.sleep(2)
            os.chdir(main_path)
            time.sleep(5)
            return "OK"

@app.route("/App_Test", methods=['GET'])
def App_Test():
    os.chdir(main_path)
    os.system('python ./Android_Phone_TestCode/App_test.py')
    return "Start App WebTest"

@app.route("/Android_Browser", methods=['POST'])
def Android_Browser():
    os.chdir(main_path)
    if request.method == "GET":
        return "Error"
    elif request.method == "POST":
        data = request.get_json()
        print("/Android_Browser Get Data: ", data)
        account = data['Account']
        # Git
        git_path = App_target_path("App", "Android", "Browser")
        if os.path.exists('App'):
            os.system('rd /s /q App')
        os.system('git clone https://github.com/bleach1425/TestCase_ver1.0.git App/')
        os.chdir(git_path)
        os.system("git pull")
        print("Check route: ", os.getcwd())
        CaseNumber = data['CaseNumber']
        # Get Post
        print('Have FileName')
        filename = ''
        imagename = ''
        print(data['FileName'], type(data['FileName']))
        yamlname = [n for n in data['FileName'] if "yaml" in n][0]
        print("--------------------------------------------------------------------")
        os.system(f"start python Android_WebTest_yaml_version.py {account} {CaseNumber} {yamlname} &")
        print("--------------------------------------------------------------------")
        os.chdir(main_path)
        return "OK"

@app.route("/Android_App", methods=['POST'])
def Android_App():
    os.chdir(main_path)
    if request.method == "GET":
        return "Error"
    elif request.method == "POST":
        data = request.get_json()
        print("/Android_Browser Get Data: ", data)
        account = data['Account']
        # Git
        git_path = App_target_path("App", "Android", "App")
        if os.path.exists('App'):
            os.system('rd /s /q App')
        os.system('git clone https://github.com/bleach1425/TestCase_ver1.0.git App/')
        os.chdir(git_path)
        os.system("git pull")
        print("Check route: ", os.getcwd())
        CaseNumber = data['CaseNumber']
        # Get Post
        print('Have FileName')
        filename = ''
        imagename = ''
        print(data['FileName'], type(data['FileName']))
        yamlname = [n for n in data['FileName'] if "yaml" in n][0]
        print("--------------------------------------------------------------------")
        os.system(f"start python Android_AppTest_yaml_version.py {account} {CaseNumber} {yamlname} &")
        print("--------------------------------------------------------------------")
        os.chdir(main_path)
        return "OK"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5666, debug=True, threaded=True)

