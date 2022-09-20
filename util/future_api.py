"""
本示例仅作为演示签名计算方式使用，包含合约API/V4版本的基本功能:
开仓,平仓,仓位判断,仓位模式设定与获取
"""
"""
Created on Wed Sep 10 2022

@author: Haiyi
@email: yyy99910@gmail.com
@wechart: yyy99966
@github: https://github.com/efens222

"""

# coding: utf-8
import time
import hashlib
import hmac
import requests
import json
import util.accountConfig as config
import util.exceptions

host = "https://fx-api-testnet.gateio.ws"


def gen_sign(method, url, query_string=None, payload_string=None):
    key = config.access_key  # ""      # api_key
    secret = config.secret_key  # ""    # api_secret

    t = time.time()
    m = hashlib.sha512()
    m.update((payload_string or "").encode('utf-8'))
    hashed_payload = m.hexdigest()
    s = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", hashed_payload, t)
    sign = hmac.new(secret.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()
    return {'KEY': key, 'Timestamp': str(t), 'SIGN': sign}


def openOrder(contract="BTC_USDT", lots=0.01, price=0.0, type=0):
    host = "https://fx-api-testnet.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    url = '/futures/usdt/orders'
    query_param = ''
    size = lots
    if contract == "BTC_USDT":    size = lots * 10000
    if contract == "ETH_USDT":    size = lots * 100
    if price == 0.0:
        tif = "ioc"
    else:
        tif = None

    body = '{"contract":"' + contract + '","size":"' + str(int(size)) + '","iceberg":0,"price":"' + str(
        price) + '","tif":"' + tif + '"}'
    print(body)
    # `gen_sign` 的实现参考认证一章
    sign_headers = gen_sign('POST', prefix + url, query_param, body)
    headers.update(sign_headers)
    r = requests.request('POST', host + prefix + url, headers=headers, data=body)
    print(r.json())
    print(r.status_code)
    if r.status_code >= 400:
        return print("%s开仓失败", r.json()['contract'])
    else:
        if type == 0:
            print("%s %s开仓完成" % (r.json()['contract'], r.json()['size']))
        else:
            print("%s %s平仓完成" % (r.json()['contract'], r.json()['size']))
        return r.json()


#####

""""

"""


def closeOrder(contract="BTC_USDT", auto_size=None):
    host = "https://fx-api-testnet.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    url = '/futures/usdt/orders'
    query_param = ''
    # size=lots
    # if contract=="BTC_USDT":    size=lots*10000
    # if contract == "ETH_USDT":    size = lots * 100
    # if price==0:tif="ioc"
    # else: tif=None
    if auto_size is not None:
        body = '{"contract":"' + contract + '","size":"0","price":0,"close":true,"tif":"ioc","reduce_only":true,"auto_size":"' + auto_size + '"}'
    else:
        body = '{"contract":"' + contract + '","size":"0","price":0,"close":true,"tif":"ioc","reduce_only":true}'

    print(body)
    # `gen_sign` 的实现参考认证一章
    sign_headers = gen_sign('POST', prefix + url, query_param, body)
    headers.update(sign_headers)
    r = requests.request('POST', host + prefix + url, headers=headers, data=body)
    print(r.json())
    print(r.status_code)
    if r.status_code >= 400:
        return print("平仓失败", r.json()['contract'])
    else:
        print("平仓完成", r.json()['contract'], r.json()['size'])
        return r.json()
    # return r.json()
    # pass


###########################################################################

###########################################################################
def set_pos_mode(dual_mode='false'):
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    url = '/futures/usdt/dual_mode'
    query_param = 'dual_mode=' + dual_mode
    print(query_param)
    # `gen_sign` 的实现参考认证一章
    sign_headers = gen_sign('POST', prefix + url, query_param)
    headers.update(sign_headers)
    r = requests.request('POST', host + prefix + url + "?" + query_param, headers=headers)
    print(r.json())
    print(r.status_code)
    msg = str(r.status_code) + ' ' + str(r.json())
    if r.status_code != 200:
        return msg
    else:
        return r.json()


"""
"""


def get_pos_mode(symbol='BTC_USDT'):
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    url = '/futures/usdt/positions/' + symbol
    query_param = ''
    # `gen_sign` 的实现参考认证一章
    sign_headers = gen_sign('GET', prefix + url, query_param)
    headers.update(sign_headers)
    r = requests.request('GET', host + prefix + url, headers=headers)
    print(r.json())
    print(r.status_code)
    # json_str = json.dumps(r[0])
    # print(json_str)
    msg = str(r.status_code) + ' ' + str(r.json())
    if r.status_code != 200:
        print(msg)
        return 0
    else:
        if r.json()['mode'] == 'single':
            print('sigle')
            return 1
        else:
            print('dua')
            return 2


"""
    
"""


def get_tradeInfo(contract='BTC_USDT'):
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    url = '/futures/usdt/trades'
    query_param = 'contract=BTC_USDT'
    r = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers)
    print(r.json())


"""

"""


def get_position(symbol='BTC_USDT'):
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    url = '/futures/usdt/positions/' + symbol
    query_param = ''
    # `gen_sign` 的实现参考认证一章
    sign_headers = gen_sign('GET', prefix + url, query_param)
    headers.update(sign_headers)
    r = requests.request('GET', host + prefix + url, headers=headers)
    print(r.json())
    print(r.status_code)
    # json_str = json.dumps(r[0])
    # print(json_str)
    msg = str(r.status_code) + ' ' + str(r.json())
    if r.status_code != 200:
        return msg
    else:
        return json_operation(r.json())


'''

'''


def json_operation(data=None):
    # 写入 JSON 数据
    with open('../log/data.json', 'w') as f:
        json.dump(data, f)

    # # 读取数据
    # with open('../log/data.json', 'r') as f:
    #     data = json.load(f)
    print(data['size'])
    return data['size']


#####################################################################
#####################################################################
if __name__ == "__main__":
    # get_tradeInfo()
    set_pos_mode("false")
    symbol = 'ETH_USDT'
    pos = float(get_position(symbol))
    if pos == 0:
        openOrder("ETH_USDT", -0.1)
    elif get_pos_mode(symbol) == 1:  # single postion
        close = True
        closeOrder('ETH_USDT')
        # dua_mode postion
    else:
        if pos < 0:
            closeOrder('ETH_USDT', "close_short")
        else:
            closeOrder('ETH_USDT', "close_long")
    # json_operation(data)
    # host = "https://api.gateio.ws"
    # get_pos_mode()
    # url = '/futures/usdt/positions'
    # query_param = ''
    # # `gen_sign` 的实现参考认证一章
    # sign_headers = gen_sign('GET', prefix + url, query_param)
    # # headers.update(sign_headers)
    # r = requests.request('GET', host + prefix + url, headers=sign_headers)
    #
    # openOrder("ETH_USDT",-0.1)
    # closeOrder('ETH_USDT', "close_short")
    # closeOrder('BTC_USDT', "close_long")

    # print(r.json())
