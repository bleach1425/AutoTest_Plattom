from __init__ import *
from flask import Blueprint
from flask_cors import cross_origin
from views.func_shopping import Work

shopping = Blueprint('shopping', __name__)
carts_list = []

@shopping.route('/menu', methods=['GET', 'POST'])
def menu():
    return render_template('menu.html')

@shopping.route('/index', methods=['GET'])
@login_required
def index():
    global data, carts_list
    user = session.get('account')
    print("user: ", user)
    # First step search user history
    sql = "select username from carts where username=%s"
    num = cursor.execute(sql, (user,))
    print("資料庫查詢資料", num)

    if not num:
        # first use add user and carts
        print("首次使用, 新建會員")
        sql_insert = "insert into carts(username, carts_data) values(%s, %s)"
        cursor.execute(sql_insert, (user, "[]"))
        carts_list = []
        db_.commit()

    else:
        print("舊用戶")
        sql_search = "select carts_data from carts where username=%s"
        cursor.execute(sql_search, (user,))
        carts_list = cursor.fetchall()[0][0]
        carts_list = eval(carts_list)
        if carts_list:
            parse = []
            parse.append(carts_list)
            carts_list = parse
            print("history carts_list: ", carts_list)
        else:
            print("history carts_list: ", carts_list)

    if 'sorted_by' in request.args and 'sorted' in request.args and 'min' in request.args and 'max' in request.args:
        sorted_by = request.args['sorted_by']
        sorted_ = request.args['sorted']
        min_ = request.args['min']
        max_ = request.args['max']
        do = Work(cursor, sorted_by, sorted_, min_, max_)
        data = do.min_max_after_judge()
        mode = '1'
        return render_template('/Shopping/main/index.html', commodity= data, ip=ip, mode=mode)

    elif 'sorted_by' in request.args and 'sorted' in request.args:
        sorted_by = request.args['sorted_by']
        sorted_ = request.args['sorted']
        do = Work(cursor, sorted_by, sorted_, '', '')
        data = do.judge_columns()
        mode = ''
        return render_template('/Shopping/main/index.html', commodity= data, ip=ip, mode=mode)

    elif 'min' in request.args and 'max' in request.args:
        min_ = request.args['min']
        max_ = request.args['max']
        do = Work(cursor, '', '', min_, max_)
        data = do.min_max_search()
        mode = '1'
        return render_template('/Shopping/main/index.html', commodity= data, ip=ip, mode=mode)

    else:
        cursor.execute('SELECT * FROM `commodity`')
        data = cursor.fetchall()
        mode = ''
        return render_template('/Shopping/main/index.html', commodity= data, ip=ip, mode=mode)



@shopping.route('/carts', methods=['GET', 'POST'])
@login_required
@cross_origin()
def carts():
    global carts_list
    user = session.get('account')
    print("user: ", user)
    if request.method == 'POST':
        data = request.get_json()
        print("carts_list: ", carts_list, type(carts_list))
        if carts_list:
            # LOCAL block
            for carts_item in carts_list:
                if user in carts_item:
                    carts_item[user].append(data)
                    print("當前購物車: ", carts_list)
                    # SQL block
                    sql_update = "update carts set carts_data=%s where username=%s"
                    print(sql_update % (carts_list, user))
                    cursor.execute(sql_update, (carts_list, user))
                    db_.commit()
                    return "OK"
        else:
            # LOCAL block
            carts_list.append({user:[data]})
            print("當前購物車: ", carts_list)

            # SQL block
            sql_update = "update carts set carts_data=%s where username=%s"
            print(sql_update % (carts_list, user))
            cursor.execute(sql_update, (carts_list, user))
            db_.commit()
            return 'OK'
    else:
        table_list = []
        count_price = 0
        for _ in carts_list:
            if user in _:
                for i, item in enumerate(_[user]):
                    row = list(item.values())
                    count_price += int(row[1]) * int(row[2])
                    row.insert(0, i+1)
                    row.insert(4, '')
                    table_list.append(row)
        print("Final: ", table_list)
        if carts_list:
            # 購物車有商品
            return render_template('./Shopping/main/carts.html', ip=ip, carts_list=table_list, count_price=count_price)
        else:
            # 購物車無商品
            return render_template('./Shopping/main/carts.html', ip=ip, carts_list=table_list)


@shopping.route('/checkout', methods=['GET', 'POST'])
@login_required
@cross_origin()
def checkout():
    global carts_list
    table_list = []
    columns_list = ["姓名", "電話", "城市", "地址", "區域", "郵遞區號"]
    id_list = ["name", "cellphone", "city", "address", "area", "postal code"]
    count_price = 0
    # user = session.get('account')
    # print("user: ", user)
    user = 'asd'
    # user information block
    sql_select = "select * from user_information where user=%s"
    cursor.execute(sql_select, (user,))
    user_infer = list(cursor.fetchall()[0])[2:]
    print('user_infer: ', user_infer)
    # table information block
    for _ in carts_list:
        if user in _:
            for i, item in enumerate(_[user]):
                row = list(item.values())
                count_price += int(row[1]) * int(row[2])
                row.insert(0, i+1)
                row.insert(4, '')
                table_list.append(row)
    print("Final: ", table_list)
    mix = list(zip(id_list, user_infer))
    table_dict = dict(zip(columns_list, mix))
    if carts_list:
        # 購物車有商品
        print('1')
        return render_template('./Shopping/main/checkout.html', ip=ip, carts_list=table_list, count_price=count_price, user_columns=columns_list,
                                user_infer=user_infer, table_dict=table_dict, username=user)
    else:
        # 購物車無商品
        print('2')
        return render_template('./Shopping/main/checkout.html', ip=ip, carts_list=table_list)


@shopping.route('/delete_carts', methods=['POST'])
def delete_carts():
    global carts_list
    user = session.get('account')
    print("user: ", user)
    # user = 'asd'
    data = request.get_json()
    # LOCAL
    for row in carts_list:
        if user in row:
            row[user].pop(int(data['remove_index'])-1)
    # SQL
    sql_update = "update carts set carts_data=%s where username=%s"
    cursor.execute(sql_update, (carts_list, user))
    db_.commit()
    return 'OK'


@shopping.route('/create_order', methods=['POST'])
def create_order():
    # SQL Check ID
    num = cursor.execute('select * from commodity_order')
    datetime_dt = datetime.today()
    created_time = datetime_dt.strftime("%Y/%m/%d %H:%M:%S")
    print('*' * 10)
    print('carts_list: ', carts_list)
    print('Create_time: ', created_time)
    print('User Data: ')
    for row in request.form:
        print(row,": ",  dict(request.form)[row])
    Order = {}
    Order['UserName'] = request.form.get('user')
    Order['CreateTime'] = created_time
    Order['OrderName'] = 'Order ' + str(num+1)
    Order['OrderPrice'] = request.form.get('total_price')
    Order['SendType'] = request.form.get('send_type')
    Order['SendPosition'] = request.form.get('address')
    Order['PayType'] = request.form.get('pay_type')
    print('*' * 10)
    temp = ('insert into commodity_order(UserName,OrderName,CreateTime,OrderPrice,SendType,SendPosition,PayType) values(%s, %s, %s, %s, %s, %s, %s)')
    cursor.execute(temp, (Order['UserName'], Order['OrderName'], Order['CreateTime'], Order['OrderPrice'], send_type_transform[Order['SendType']], Order['SendPosition'], pay_type_transform[Order['PayType']]))
    db_.commit()
    return render_template('./Shopping/main/finish.html')


@shopping.route('/finish', methods=["POST"])
def finish():
    return render_template('./Shopping/main/finish.html')


@shopping.route('/order', methods=['GET', 'POST'])
def order():
    Comfirm_order_list = []
    sql = "select * from commodity_order"
    order_num = cursor.execute(sql)
    order_list = cursor.fetchall()
    for n in order_list:
        Comfirm_order_list.append(list(n[2:][:-1]))

    if order_num:
        # 有訂單
        print('1')
        return render_template('./Shopping/main/order.html', ip=ip, order_list=Comfirm_order_list)
    else:
        # 無訂單
        print('2')
        return render_template('./Shopping/main/order.html', ip=ip, order_list=Comfirm_order_list)