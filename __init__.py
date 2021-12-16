from flask import Flask, render_template, redirect, request, make_response,\
                  url_for, flash, abort, session, flash, jsonify, Blueprint
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_socketio import SocketIO, emit
from flask_testing import TestCase
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask import current_app
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime
import os
import MySQLdb
import socket
import json
import shutil
import atexit
import time
import requests
import redis
import importlib

# Redis
# r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Base
basedir = os.getcwd() + "/"

# database
db_ = MySQLdb.connect(
    host='localhost',
    user='rubio',
    password='0000',
    db='plattom_data',
    charset='utf8'
    )

cursor = db_.cursor()


# Login
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# app config
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://rubio:0000@192.168.5.181:3306/mtv_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)
csrf = CSRFProtect()

# Logging setting
handler = TimedRotatingFileHandler(
    'flask.log', when='D', interval=1, backupCount=15,
    encoding='UTF-8', delay=False, utc=True)
# server see config
# logging.basicConfig(format='[%(asctime)s] [%(filename)s:%(lineno)d] - %(message)s')
# flask.log see config
formatter = logging.Formatter(
        '[%(asctime)s] [%(filename)s:%(lineno)d] - %(message)s')
app.logger.addHandler(handler)
handler.setFormatter(formatter)
# Socket
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")


# Server_ip
port = 5000
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    result = "http://" + ip + ":"+ str(port) +"/"
    s.close()
    return result
ip = get_ip()


# App Agent
Agent_Android_Browser = "http://192.168.5.181:5666/Android_Browser"
Agent_Android_App = "http://192.168.5.181:5666/Android_App"
Agent_IOS_Browser = "http://192.168.5.110:5557/IOS_Browser"
Agent_IOS_App = "http://192.168.5.110:5557/IOS_App"

# Web Agent
Linux_Web_agent = "http://192.168.5.191:5556/WebCase"
Windows_Web_agent = "http://192.168.5.181:5666/WebCase"
Mac_Web_agent = "http://192.168.5.110:5557/WebCase"

# API Agent
Linux_Api_agent = "http://192.168.5.191:5556/APICase"
Windows_Api_agent = "http://192.168.5.181:5666/APICase"
Mac_Api_agent = "http://192.168.5.110:5557/APICase"

# Video Player
# (---------------------------------------------------------------------------------------)
movies_dir = os.listdir('./static/movies')
if not os.path.isfile('movie_data/movies.json'):
    with open('./movie_data/movies.json', mode='w', encoding='utf-8') as f:
        json_dict = {"movies": []}
        for file in movies_dir:
            dict_ = {file: {'title': file.split('.')[0], 'count': 0} }
            json_dict['movies'].append(dict_)
        json.dump(json_dict, f)

# Check
check = []
with open('./movie_data/movies.json', mode='r') as f:
    movies = json.load(f)
    # Make check list
    for movie in movies['movies']:
        check.append(list(movie.keys())[0])
    if len(set(movies_dir)) > len(set(check)):
        print('Add new File')
        x = set(movies_dir) - set(check)
        Lack = ''.join(x)
        if Lack:
            movies['movies'].append({Lack: {"title": Lack.split('.')[0], "count": 0}})
            with open('./movie_data/movies.json', mode='w') as nf:
                json.dump(movies, nf)
        else:
            print("No change")
    elif len(set(movies_dir)) < len(set(check)):
        print('Delete File')
        x = set(check) - set(movies_dir)
        Lack = ''.join(x)
        r = [movie for movie in movies['movies'] if Lack == list(movie.keys())[0]][0]
        delete_index = movies['movies'].index(r)
        movies['movies'].pop(delete_index)
        with open('./movie_data/movies.json', mode='w') as nf:
            json.dump(movies, nf)
    else:
        print('same')
# (---------------------------------------------------------------------------------------)

pay_type_transform = {"After": "貨到付款", "Crash": "信用卡付款", "Store": "超商付款"}
send_type_transform = {"7-11": "7-11取貨", "Family": "全家取貨", "Home":"宅配到家"}
