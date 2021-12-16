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
path = os.getcwd()
# git_path = os.getcwd() + "/Api/Api"
filename = ""
imagename = ""
main_path = os.getcwd()

def driver(account):
    os.system(f"start python Windows_WebCase_ver1.0.py {account}")
    return "OK"

def target_path(CaseType, System):
    git_path = os.getcwd() + f"/{CaseType}/{CaseType}/{System}"
    return git_path

@app.route("/", methods=["GET", "POST"])
def index():
    return "Server is Work"

@app.route("/WebCase", methods=["POST"])
def WebCase():
    global main_path
    # data
    os.chdir(path)
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
        p = subprocess.Popen(f'start python Web_example.py {account} {CaseNumber}', shell=True)
        p.communicate()
        p.wait()
        print("driver end")
        print("---------------------------")
        os.chdir(path)
        time.sleep(5)
        return "OK"
        # return redirect(url_for('DeleteFile', dirpath='Web', file=data['FileName'], system="Windows"))
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
        # p = subprocess.Popen(f'start python Windows_WebCase_ver1.0.py {account} {filename} {CaseNumber} &', shell=True)
        # p.communicate()
        # p.wait()
        print("driver end")
        print('--------------------------------')
        os.chdir(path)
        return "OK"
        # return redirect(url_for('DeleteFile', dirpath='Web', file=data['FileName'], system="Windows"))

@app.route("/APICase", methods=['GET', 'POST'])
def APICase():
    data = request.get_json()
    if request.method == "GET":
        return "Error"
    elif request.method == "POST":
        account = data['Account']
        # Git
        git_path = target_path("Api", "Windows")
        if os.path.exists('Api'):
            os.system('rd /s /q Api')
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
                # APITestCase_Windows.py
                os.system(f"start python APITestCase_Windows.py {account} {filename} {imagename} {CaseNumber} &")
                time.sleep(2)
                print("Delete File~~~")
                print("---FileName---", data['FileName'])
                # DeleteFile11('Api', data['FileName'])
                os.chdir(path)
                time.sleep(5)
                return "OK"
                # return redirect(url_for('DeleteFile', dirpath='Api', file=data['FileName'], system="Windows"))
            else:
                print("-------------------------image not in local------------------------------")
                os.system(f"start python APITestCase_Windows.py {account} {filename} {CaseNumber} &")
                time.sleep(2)
                print("Delete File~~~")
                print("---FileName---", data['FileName'])
                # DeleteFile11('Api', data['FileName'])
                os.chdir(path)
                return "OK"
                # time.sleep(5)
                # return redirect(url_for('DeleteFile', dirpath='Api', file=filename, system="Windows"))
        else:
            print("Don't have FileName, Do Example")
            filename = "Example.yaml"
            imagename = "test.dcm"
            time.sleep(5)
            os.system(f"start python APITestCase_Windows.py {account} {filename} {imagename} {CaseNumber} &")
            time.sleep(2)
            print("Delete File~~~")
            os.chdir(path)
            time.sleep(5)
            return "OK"

@app.route("/history_case", methods=['GET', "POST"])
def history_case():
    if request.method == "GET":
        return "Error"
    elif request.method == "POST":
        ###   Check identity if S Go Vip_file folder.., N Go Normal_file folder ..   ###
        identity = "Vip"
        # Git
        os.system('git clone https://github.com/bleach1425/TestCase_ver1.0.git History/')
        os.chdir(f'./History/{identity}')
        os.system("git pull")
        #
    return "OK"

@app.route("/App_Test", methods=['GET'])
def App_Test():
    os.system('python ./Android_Phone_TestCode/App_test.py')
    return "Start App WebTest"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5666, debug=True, threaded=True)