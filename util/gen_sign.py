"""
本示例仅作为演示签名计算方式使用，推荐使用各语言的 SDK ，因为已经集成了验签规则
"""

# coding: utf-8
import time
import hashlib
import hmac
import requests
import json

def gen_sign(method, url, query_string=None, payload_string=None):
    key = "0522c68728e727baffeadb21685d3d69"      # api_key
    secret = "1d628c468b9f45fd378ceb93c0761639c1b20062581ea3c3112c7eaae375d33a"    # api_secret

    t = time.time()
    m = hashlib.sha512()
    m.update((payload_string or "").encode('utf-8'))
    hashed_payload = m.hexdigest()
    s = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", hashed_payload, t)
    sign = hmac.new(secret.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()
    return {'KEY': key, 'Timestamp': str(t), 'SIGN': sign}

if __name__ == "__main__":
    # host = "https://api.gateio.ws"
    host = "https://fx-api-testnet.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    url = '/futures/usdt/orders'
    query_param = ''

    body = '{"contract":"BTC_USDT","size":6000,"iceberg":0,"price":"0","tif":"ioc","text":"t-my-custom-id"}'
    # `gen_sign` 的实现参考认证一章
    sign_headers = gen_sign('POST', prefix + url, query_param, body)
    headers.update(sign_headers)
    r = requests.request('POST', host + prefix + url, headers=headers, data=body)
    print(r.json())
    # url = '/futures/usdt/positions'
    # query_param = ''
    # # `gen_sign` 的实现参考认证一章
    # sign_headers = gen_sign('GET', prefix + url, query_param)
    # # headers.update(sign_headers)
    # r = requests.request('GET', host + prefix + url, headers=sign_headers)
    # print(r.json())