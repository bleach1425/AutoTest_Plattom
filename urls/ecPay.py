import sys
sys.path.append('..')
from __init__ import *


# Setting
payment = Blueprint('payment', __name__)
filename = os.getcwd()
spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk", filename + "\\sdk\\ecpay_payment_sdk.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Params:
    def __init__(self):
        web_type = 'test'
        if web_type == 'offical':
            # 正式環境
            self.params = {
                'MerchantID': 'ID隱藏',
                'HashKey': 'Key 隱藏',
                'HashIV': 'IV 隱藏',
                'action_url':
                'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5'
            }
        else:
            # 測試環境
            self.params = {
                'MerchantID':
                '2000132',
                'HashKey':
                '5294y06JbISpM5x9',
                'HashIV':
                'v77hoKGq4kWxNNIS',
                'action_url':
                'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'
            }
    @classmethod
    def get_params(cls):
        return cls().params

    # 驗證綠界傳送的檢查碼 check_mac_value 值是否正確
    @classmethod
    def get_mac_value(cls, get_request_form):

        params = dict(get_request_form)
        if params.get('CheckMacValue'):
            params.pop('CheckMacValue')

        ordered_params = collections.OrderedDict(
            sorted(params.items(), key=lambda k: k[0].lower()))

        HahKy = cls().params['HashKey']
        HashIV = cls().params['HashIV']

        encoding_lst = []
        encoding_lst.append('HashKey=%s&' % HahKy)
        encoding_lst.append(''.join([
            '{}={}&'.format(key, value)
            for key, value in ordered_params.items()
        ]))
        encoding_lst.append('HashIV=%s' % HashIV)

        safe_characters = '-_.!*()'

        encoding_str = ''.join(encoding_lst)
        encoding_str = quote_plus(str(encoding_str),
                                  safe=safe_characters).lower()

        check_mac_value = ''
        check_mac_value = hashlib.sha256(
            encoding_str.encode('utf-8')).hexdigest().upper()

        return check_mac_value


# 建立訂單後跳轉至 ECpay 頁面
@payment.route('/to_ecpay', methods=['POST'])
def ecpay():
    # 商品資料
    commodity = request.get_json()
    print('commodity: ', commodity)
    # 取得使用者ID並搜尋資訊
    user = session.get('account')
    print('user: ', user)
    # user = 'asd'
    cursor.execute("SELECT * FROM `user_information` WHERE `user`='%s'" % user)
    data = cursor.fetchall()
    print('data: ', data)
    # 從 session 中取得 uid
    # uid = session.get('uid')
    uid = '02'
    host_name = request.host_url

    # 取得 POST 的收件人資訊
    # --- My version ---
    trade_name = data[0][2]
    trade_phone = data[0][3]
    county = data[0][4]
    district = data[0][5]
    zipcode = data[0][6]
    address = data[0][7]
    
    # --- Ori version ---
    # trade_name = request.values['name']
    # trade_phone = request.values['phone']
    # county = request.values['county']
    # district = request.values['district']
    # zipcode = request.values['zipcode']
    # address = request.values['address']

    # 利用 uid 查詢資料庫，購物車商品 & 價錢
    # carts = sql.AddToCar.query.filter_by(uid=uid, state='Y')
    total_product_price = 0
    total_product_name = ''

    # for cart in carts:
    #     real
    #     price = cart.product.price
    #     quan = cart.quantity
    #     product_name = cart.product.name
        # -------------------------------
    '''fake data'''
    print(commodity)
    for cart in commodity:
        price = int(cart[2])
        quan = int(cart[3])
        product_name = cart[1]
        total_product_price += price * quan
        total_product_name += product_name + '#'
    # -------------------------------
    # total_product_price += price * quan
    # total_product_name += product_name + '#'

    # 建立交易編號 tid
    date = time.time()
    tid = str(date) + 'Uid' + str(uid)
    status = '未刷卡'

    # 新增 Transaction 訂單資料
    with open('transaction.json', mode='a+') as f:
        Transaction = {
            "uid": uid,
            "tid": tid,
            "trade_name": trade_name,
            "trade_phone": trade_phone,
            "address": address,
            "total_product_price": total_product_price,
            "status": status,
            "county": county,
            "district": district,
            "zipcode": zipcode
        }
        json.dump(Transaction, f)
    # T = sql.Transaction(uid, tid, trade_name, trade_phone, address,
    #                     total_product_price, status, county, district, zipcode)
    # db.session.add(T)
    # db.session.commit()

    params = Params.get_params()

    # 設定傳送給綠界參數
    order_params = {
        'MerchantTradeNo': datetime.now().strftime("NO%Y%m%d%H%M%S"),
        'StoreID': '',
        'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        'PaymentType': 'aio',
        'TotalAmount': total_product_price,
        'TradeDesc': 'ToolsFactory',
        'ItemName': total_product_name,
        'ReturnURL': host_name + 'payment/receive_result',
        'ChoosePayment': 'Credit',
        'ClientBackURL': host_name + 'payment/trad_result',
        'Remark': '交易備註',
        'ChooseSubPayment': '',
        'OrderResultURL': host_name + 'payment/trad_result',
        'NeedExtraPaidInfo': 'Y',
        'DeviceSource': '',
        'IgnorePayment': '',
        'PlatformID': '',
        'InvoiceMark': 'N',
        'CustomField1': str(tid),
        'CustomField2': '',
        'CustomField3': '',
        'CustomField4': '',
        'EncryptType': 1,
    }

    extend_params_1 = {
        'BindingCard': 0,
        'MerchantMemberID': '',
    }

    extend_params_2 = {
        'Redeem': 'N',
        'UnionPay': 0,
    }

    inv_params = {
        # 'RelateNumber': 'Tea0001', # 特店自訂編號
        # 'CustomerID': 'TEA_0000001', # 客戶編號
        # 'CustomerIdentifier': '53348111', # 統一編號
        # 'CustomerName': '客戶名稱',
        # 'CustomerAddr': '客戶地址',
        # 'CustomerPhone': '0912345678', # 客戶手機號碼
        # 'CustomerEmail': 'abc@ecpay.com.tw',
        # 'ClearanceMark': '2', # 通關方式
        # 'TaxType': '1', # 課稅類別
        # 'CarruerType': '', # 載具類別
        # 'CarruerNum': '', # 載具編號
        # 'Donation': '1', # 捐贈註記
        # 'LoveCode': '168001', # 捐贈碼
        # 'Print': '1',
        # 'InvoiceItemName': '測試商品1|測試商品2',
        # 'InvoiceItemCount': '2|3',
        # 'InvoiceItemWord': '個|包',
        # 'InvoiceItemPrice': '35|10',
        # 'InvoiceItemTaxType': '1|1',
        # 'InvoiceRemark': '測試商品1的說明|測試商品2的說明',
        # 'DelayDay': '0', # 延遲天數
        # 'InvType': '07', # 字軌類別
    }

    ecpay_payment_sdk = module.ECPayPaymentSdk(MerchantID=params['MerchantID'],
                                               HashKey=params['HashKey'],
                                               HashIV=params['HashIV'])

    # 合併延伸參數
    order_params.update(extend_params_1)
    order_params.update(extend_params_2)

    # 合併發票參數
    order_params.update(inv_params)

    try:
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)

        # 產生 html 的 form 格式
        action_url = params['action_url']
        html = ecpay_payment_sdk.gen_html_post_form(action_url,final_order_params)
        print('html: ', html)
        return {"page": html}

    except Exception as error:
        print('An exception happened: ' + str(error))


# ReturnURL: 綠界 Server 端回傳 (POST)
@csrf.exempt
@payment.route('/receive_result', methods=['POST'])
def end_return():
    result = request.form['RtnMsg']
    tid = request.form['CustomField1']
    # trade_detail = sql.Transaction.query.filter_by(tid=tid).first()
    trade_detail = {"status":"asd"}
    trade_detail.get('status') == '交易成功 sever post'
    # db.session.add(trade_detail)
    # db.session.commit()

    return '1|OK'



# OrderResultURL: 綠界 Client 端 (POST)
@csrf.exempt
@payment.route('/trad_result', methods=['GET', 'POST'])
def end_page():

    if request.method == 'GET':
        return redirect(url_for('index'))

    if request.method == 'POST':
        # 暫時不隻到參數 先PASS
        # check_mac_value = Params.get_mac_value(request.form)
        # if request.form['CheckMacValue'] != check_mac_value:
        #     return '請聯繫管理員'

        # 接收 ECpay 刷卡回傳資訊
        result = request.form['RtnMsg']
        tid = request.form['CustomField1']
        # trade_detail = sql.Transaction.query.filter_by(tid=tid).first()
        # 取得交易使用者資訊
        '''fake'''
        trade_detail = {
            'uid': '01',
            'name': '咚咚',
            'phone': '0958654321',
            'county': '台中',
            'district': '南屯區',
            'zipcode': '40841',
            'trade_address': '台中市南屯區咚咚路152號'
        }
        # uid = trade_detail.uid
        '''fake'''
        uid = trade_detail.get('uid')
        trade_client_detail = {
            'name': trade_detail.get('trade_name'),
            'phone': trade_detail.get('trade_phone'),
            'county': trade_detail.get('trade_county'),
            'district': trade_detail.get('trade_district'),
            'zipcode': trade_detail.get('trade_zipcode'),
            'trade_address': trade_detail.get('trade_address')
        }
        # trade_client_detail = {
        #     'name': trade_detail.trade_name,
        #     'phone': trade_detail.trade_phone,
        #     'county': trade_detail.trade_county,
        #     'district': trade_detail.trade_district,
        #     'zipcode': trade_detail.trade_zipcode,
        #     'trade_address': trade_detail.trade_address
        # }

        # 判斷成功
        if result == 'Succeeded':
            # trade_detail.status = '待處理'
            trade_detail['status'] = '待處理'
            commit_list = []

            # 移除 AddToCar (狀態：Y 修改成 N)
            # carts = sql.AddToCar.query.filter_by(uid=uid, state='Y')
            # for cart in carts:
            '''fake data'''
            price = 50
            quan = 5
            product_name = 'high quality sock'
                # price = cart.product.price
                # quan = cart.quantity
                # cart.state = 'N'
                # 新增 Transaction_detail 訂單細項資料
            # Td = sql.Transaction_detail(tid, cart.product.pid, quan, price)
            # commit_list.append(Td)
            # commit_list.append(cart)

            # db.session.add_all(commit_list)
            # db.session.commit()

            # 讀取訂單細項資料
            # trade_detail_items = sql.Transaction_detail.query.filter_by(
            #     tid=tid)

            return render_template('/payment/trade_success.html',
                                   shopping_list= trade_detail, # trade_detail_items
                                   total=trade_detail.total_value)

        # 判斷失敗
        else:
            # carts = sql.AddToCar.query.filter_by(uid=uid, state='Y')
            # trade_detail = sql.Transaction.query.filter_by(tid=tid).first()

            return render_template('/payment/trade_fail.html',
                                   shopping_list=carts,
                                   total=trade_detail.total_value,
                                   trade_client_detail=trade_client_detail)




@payment.route('/payment_page', methods=['GET', 'POST'])
def payment_page():
    html = request.form['html']
    return make_response(html, 200)