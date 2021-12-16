from __init__ import *
from config.var import *
from models.models import User, Post
from models.forms import LoginForm, RegistrationForm

# My Package
from my_package.Upload_Git_Package import Gitpath_setting, Update_to_git
from my_package.jstree_process.jstree_process import tree
from my_package.Queue_setting import Queue_setting
from my_package.identity_package.identity import identity_generator
from views.module_here import module_api, module_common
from urls.auth import auth
from urls.shopping import shopping
from urls.ecPay import payment

# var
save = save_var()

# package
Git_func = Update_to_git.git_update()
jstree_process = tree()
CaseNumber = identity_generator()
queue = Queue_setting.deal_queue()
module = module_api()
common = module_common()
# --------------------------------------------------------------

# Blueprint
app.register_blueprint(auth , url_prefix='/auth')
app.register_blueprint(shopping , url_prefix='/shopping')
app.register_blueprint(payment, url_prefix='/payment/')
# --------------------------------------------------------------

@app.route('/', methods=['GET'])
def base():
    return redirect(url_for('auth.login'))

@app.route('/index', methods=['GET'])
@login_required
def index():
    account, data, save.Agent_list = common.module_index(save)
    print("是否有回傳回來? ", save.Agent_list)
    print("當前登入使用者: ", session.get('account'))
    if save.Ram_CaseNumber:
        try:
            common.module_Reset_Work(account, save.Ram_CaseNumber[account])
            save.Ram_CaseNumber = {}
        except:
            common.module_Reset_Work(account)
    return render_template('index.html', server_ip=ip, data=data)


# ----------------------------------------------------------------------------------------------------------------------
###  Api route  ###
@app.route('/TestENV_Api', methods=['GET', 'POST'])
def TestENV_Api():
    account, data = module.module_envapi()
    
    return render_template("./TestENV/TestENV_Api.html", data=data, server_ip=ip, account=account)


@app.route('/FileUpload_Api_GitTree', methods=['GET', 'POST'])
def fileupload_api():
    return render_template('./FileUpload/FileUpload_Api_GitTree.html', server_ip=ip)


@app.route("/FileCatch_Api", methods=["GET", "POST"])
def filecatch_api():
    data = request.get_json()
    file_list = request.files.getlist('myFile')
    module.filecatch_api(save, data, file_list)
    return "OK"


@app.route("/TestENV_Api_4", methods=["GET", "POST"])
def TestENV_Api_4():
    return render_template("./TestENV_4/TestENV_Api_4.html", server_ip=ip)


@app.route('/Vip_History_Page_Api', methods=['GET', 'POST'])
def Vip_History_Page_Api():
    module.module_vip_history_page_api()
    return render_template('test.html', jstree_data=jstree_data, data=JSON)


@app.route("/TestENV_API_9", methods=["GET"])
def TestENV_API_9():
    module.module_envapi_9()
    return render_template("./TestENV_9/TestENV_API_9.html", server_ip=ip)


@app.route("/CheckBoxTree_Api", methods=["GET", "POST"])
def CheckBoxTree_Api():
    CaseNumber = identity_generator()
    JSON, title, data, result_list, User_identity, jstree = module.module_checkboxtree_api(save, CaseNumber)
    print('Check data: ', JSON)
    if User_identity == 'S':
        return render_template("./CheckBoxTree/CheckBoxTree_Api.html", data=eval(JSON), title=title,
                                Mac=data[0][0], Windows=data[1][0], Linux=data[2][0],
                                result_list=result_list, jstree_data=jstree)
    else:
        return render_template("CheckBoxTree_Api_example.html", data=eval(JSON), title=title,
                                Mac=data[0][0],  Windows=data[1][0], Linux=data[2][0],
                                result_list=result_list)

@app.route("/Windows_APICase", methods=["GET", "POST"])
def Windows_APICase():
    print("----------------------------開始工作囉------------------------------")
    data = request.get_json()
    code = module.module_windows_api(save, data)
    print("Status Code: ", code)
    return "SEND REQUEST"


# ----------------------------------------------------------------------------------------------------------------------


###  Check Status  ###
# ----------------------------------------------------------------------------------------------------------------------
@app.route('/check_history_api', methods=['GET'])
def check_history_api():
    return {"Status": os.path.isdir('Vip_Ram_Folder')}
# ----------------------------------------------------------------------------------------------------------------------


###  Catch Agent Response  ###
@app.route("/From_Windows_api", methods=["GET", "POST"])
def from_windows_api():
    global CaseNumber
    # GET and POST
    system = "Windows"
    data = request.get_json()
    module.module_from_windows_api(data, save, CaseNumber)
    return 'Update Completed'


### Common ###
# --------------------------------------------------------------------------------------------------------------------

@app.route("/SaveWork", methods=["GET", "POST"])
def SaveWork():
    global CaseNumber
    print("---------------SaveWork---------------")
    JSON = request.get_json()
    common.module_savework(JSON, CaseNumber)
    return "OK"

@app.route('/UpdateCaseName', methods=["GET", "POST"])
def updatemessage():
    JSON = request.get_json()
    common.module_updatecasenumber(JSON)
    return "Update OK!"

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    CaseNumber = identity_generator()
    common.module_process(data, save, CaseNumber)
    return "Save OK"

@app.route('/Reset_Ram_CaseNumber', methods=['GET', 'POST'])
def Reset_Ram_CaseNumber():
    save.Ram_CaseNumber = {}
    return "OK"

@app.route('/backstage_layer', methods=["POST", "GET"])
def backstage_layer():
    global CaseNumber
    server_ip_socket = ip[:-1]
    data_num, CREATE_TIME, CASE_NUMBER,\
    CASE_CONTENT, WORK_STATUS,\
    SYSTEM, target, CASE_TYPE = common.module_backstage_layer(server_ip_socket, CaseNumber)
    print('*'*6)
    print('target: ', target)
    print('*'*6)
    if data_num == 1:
        return render_template("./BackStage/backstage_layer.html", CT=CREATE_TIME, CN=CASE_NUMBER, CC=CASE_CONTENT, WS=WORK_STATUS,
                                SY=SYSTEM, server_ip_socket=server_ip_socket, server_ip=ip, DA=target, CTY=CASE_TYPE)
    else:
        return render_template("./BackStage/backstage_layer.html", CT=CREATE_TIME, CN=CASE_NUMBER, CC=CASE_CONTENT, WS=WORK_STATUS,
                                SY=SYSTEM, server_ip_socket=server_ip_socket, server_ip=ip, DA=target, CTY=CASE_TYPE)


@app.route("/test", methods=["GET"])
def Token_return():
    response = {"Message":"Server is Work",
                "Token":"123456789"}
    return jsonify(response)

@app.route("/clear", methods=["POST"])
def clear():
    common.module_clear(save)
    return "Clear OK"
# --------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------
@app.route('/video', methods=['GET'])
def display():
    with open('./movie_data/movies.json') as f:
        movies = json.load(f)
        key = []
        for i, n in enumerate(movies['movies']):
            key.append((i, list(n.keys())[0]))
        print(key)
        return render_template('video.html', movies=movies['movies'], key=key)


@app.route('/incrMovie', methods=['GET'])
def incr_movie():
    name = request.args['name']
    print(name)
    with open('./movie_data/movies.json', mode='r') as f:
        movies = json.load(f)
        data = [movie for movie in movies['movies'] if name in movie]
        data[0][name]['count'] += 1
        new = movies
        print(new)
    with open('./movie_data/movies.json', mode='w') as f:
        json.dump(new, f)
    return '1'
# --------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------
### Socketio Connect ###
@socketio.on('connect', namespace='/test')
def test_connect():
    global FirstConnect
    FirstConnect = True
    time.sleep(2.5)
    account = session.get('account')
    # print(account)
    CaseNumber = session.get("CaseNumber")
    if CaseNumber != None:
        sql = f'SELECT `TestCase`, `CaseStatus`, `Completeness` FROM `Schedule_management` WHERE `Account`="{account}" ORDER BY `CreateTime` DESC'
        sql1 = f'SELECT `Completeness` FROM `machine_status` WHERE `CaseNumber`="{CaseNumber}"'
    else:
        sql = f'SELECT `TestCase`, `CaseStatus`, `Completeness` FROM `Schedule_management` WHERE `Account`="{account}" ORDER BY `CreateTime` DESC'
        sql1 = f'SELECT `Completeness` FROM `machine_status`'
    data_num = cursor.execute(sql)
    data = cursor.fetchall()
    # sql
    Case = [n[0] for n in data]
    CaseStatus = [n[1] for n in data]
    Completeness = [n[2] for n in data]

    cursor.execute(sql1)
    data1 = cursor.fetchall()
    data = {
        "Case":Case,
        "CaseStatus":CaseStatus,
        "Completeness":Completeness,
    }
    emit('Back_Data', {'data': data})
    print('Server Connect!!')

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    global Socket_response_time
    print('Server disconnected')

### Socket Update ###
def Catch_news(account, CaseNumber):
    print('Push New to Server')
    if CaseNumber != None:
        sql = f'SELECT `TestCase`, `CaseStatus`, `Completeness` FROM `Schedule_management` WHERE `Account`="{account}" ORDER BY `CreateTime` DESC'
        sql1 = f'SELECT `Completeness` FROM `machine_status` WHERE `CaseNumber`="{CaseNumber}"'
    else:
        sql = f'SELECT `TestCase`, `CaseStatus`, `Completeness` FROM `Schedule_management` WHERE `Account`="{account}" ORDER BY `CreateTime` DESC'
        sql1 = f'SELECT `Completeness` FROM `machine_status`'
    data_num = cursor.execute(sql)
    data = cursor.fetchall()
    # sql
    Case = [n[0] for n in data]
    CaseStatus = [n[1] for n in data]
    Completeness = [int(n[2][:-1]) for n in data]

    cursor.execute(sql1)
    data1 = cursor.fetchall()
    data = {
        "Case":Case,
        "CaseStatus":CaseStatus,
        "Completeness":Completeness,
    }
    socketio.emit('Catch_news', {'data': data}, namespace='/test')
    return "OK"

## Catch command ###
@socketio.on('CatchCommand', namespace='/test')
def get_command(message):
    global FirstConnect
    account = session.get('account')
    CaseNumber = session.get("CaseNumber")
    # print(account, CaseNumber)
    if CaseNumber != None:
        sql = f'SELECT `TestCase`, `CaseStatus`, `Completeness` FROM `Schedule_management` WHERE `Account`="{account}" ORDER BY `CreateTime` DESC'
        sql1 = f'SELECT `Completeness` FROM `machine_status` WHERE `CaseNumber`="{CaseNumber}"'
    else:
        sql = f'SELECT `TestCase`, `CaseStatus`, `Completeness` FROM `Schedule_management` WHERE `Account`="{account}" ORDER BY `CreateTime` DESC'
        sql1 = f'SELECT `Completeness` FROM `machine_status`'
    data_num = cursor.execute(sql)
    data = cursor.fetchall()
    # sql
    Case = [n[0] for n in data]
    CaseStatus = [n[1] for n in data]
    Completeness = [n[2] for n in data]

    cursor.execute(sql1)
    data1 = cursor.fetchall()
    data = {
        "Case":Case,
        "CaseStatus":CaseStatus,
        "Completeness":Completeness,
    }
    socketio.emit('Back_Data', {'data': data})
    return "OK"

# --------------------------------------------------------------------------------------------------------------------


@app.route('/bootstrip/page', methods=['GET'])
def bootstrip():
    return render_template('Bootstrip5.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


###  Blog route  ###
@app.route('/Blog')
def Blog():
    cursor.execute(f'SELECT * FROM `blog_data_post`')
    data = cursor.fetchall()
    return render_template('Blog/post_list.html', data=data, ip=ip)

@app.route('/Blog/<q>')
def Blog_q(q: int):
    if q:
        cursor.execute(f'SELECT * FROM `blog_data_post` WHERE `id`={q}')
        data = cursor.fetchall()
        return render_template('Blog/post_detail.html', data=data[0])


###  Error Page  ###
@app.errorhandler(404)
def not_found(e):
    return render_template('./ErrorPage/Error_Page.html'), 404


@app.errorhandler(500)
def not_found(e):
    return render_template('./ErrorPage/Error_Page.html'), 500


# Stop Case DO This !!
@atexit.register
def rest():
    # sql = f'UPDATE `userdata` SET `Online`="False"'
    # cursor.execute(sql)
    # db.commit()
    print("System End")




def main():
    socketio.run(app, '0.0.0.0', port=port, debug=True)