#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Haiyi
@email: yyy99910@gmail.com
@wechart: yyy99966
@github: https://github.com/efens222

"""
import util.future_api
# from  exchangeConnection.huobi.util import *
# import exchangeConnection.huobi.huobiService
# import exchangeConnection.huobi.huobiService913
import util.future_api as uf_api
import time
import requests
import util.accountConfig as acfg
import json
import util.helper as uh

# 包装一个不同市场的统一接口 方便同一调用



class Market:
    acc_id = None
    acc_info = {}

    def __init__(self, market_name="huobi"):
        self.market_name = market_name

        if self.market_name == "huobi":
            #           base_cur, quote_cur = symbol.split("_")
            prefix = "/api/v4"
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

            url = '/futures/usdt/accounts'
            query_param = ''
            # `gen_sign` 的实现参考认证一章
            sign_headers = uf_api.gen_sign('GET', prefix + url, query_param)
            headers.update(sign_headers)
            r = requests.request('GET', acfg.gateApi + prefix + url, headers=headers)
            # print(r.json())
            # bitex_acc = exchangeConnection.huobi.huobiService913.get_accounts()
            #            print(bitex_acc)
            if r.status_code < 300:
                Market.acc_id = r.json().get("user")
                Market.acc_info = r.json()
                # print(Market.acc_id)
                # return acc_id
        # else:
        #     return None

    def update_marketInfo(self):
        acc_obj = Market()
        return acc_obj.acc_info

    # =============================================================================
    # get accounts
    # =============================================================================
    def get_accountInfo(self, market_name="huobi"):

        print(self.acc_info)
        # self.acc_id=self.acc_info["user"]
        # print(self.acc_id)
        return self.acc_id

    # =============================================================================
    #
    # =============================================================================
    def account_available(self, settle='USDT', symbol=None):
        """
        获取某个currency的可用量
        :param settle:
        :param symbol:
        :return:
        """
        r = self.update_marketInfo()
        if self.market_name == "huobi":
            acc_available = r['available']
            return float(acc_available)
        else:
            return None

    # =============================================================================
    #
    # =============================================================================
    def account_frozen(self, cur_name, symbol=None):
        """
        获取某个currency的可用量
        :param cur_name:
        :param symbol:
        :return:
        """
        if self.market_name == "huobi":
            #            base_cur, quote_cur = symbol.split("_")
            bitex_acc = exchangeConnection.huobi.huobiService913.get_balance()
            #            print(bitex_acc)
            now_list = uh.find_currency(bitex_acc.get("data").get("list"), cur_name)
            return uh.downRound(float(now_list[1].get("balance")), 8)  # 取冻结的余额
        else:
            return None

    # =============================================================================
    #   get lastest market close
    # =============================================================================
    def get_market_close(self, contract="BTC_USDT"):
        """
        获取市场盘口信息
        :param base_cur:
        :param quote_cur:
        :return:
        """
        # symbol=base_cur+quotes_cur
        prefix = "/api/v4"
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

        url = '/futures/usdt/trades'
        query_param = 'contract=' + contract + '&limit=3'
        r = requests.request('GET', acfg.gateApi + prefix + url + "?" + query_param, headers=headers)
        print(r.json())

        #        print(symbol)

        if r.status_code < 300:
            close = r.json()[0]['price']
            # lastorder = result['tick']['data'][0]['price']
            return close
        else:
            return 0

    def open_long(self, symbol, price, amount):
        '''
        long-limit
        '''
        print("long", symbol, price, amount)
        if self.market_name == "huobi":
            #            base_cur, quote_cur = symbol.split("_")
            return util.future_api.openOrder(symbol, amount, price, 0)
        else:
            return None

    def open_short(self, symbol, amount, price):
        # short-limit
        # print("short", symbol, price, amount)
        if self.market_name == "huobi":
            return util.future_api.openOrder(symbol, -amount, price, 0)

        else:
            return None

    def open_long_market(self, symbol, amount):
        """
        市价买
        :param symbol: 货币对的名称
        :param amount: 买的总价
        :return:
        """
        # print("long_market:", symbol, amount)
        if self.market_name == "huobi":
            return util.future_api.openOrder(symbol, amount, 0.0, 0)
        else:
            return None

    def open_short_market(self, symbol, amount):
        """
        市价卖
        :param symbol: 货币对的名称
        :param amount: 卖的数量
        :return:
        """
        # print("short_market:", symbol, amount)
        if self.market_name == "huobi":
            return util.future_api.openOrder(symbol, -amount, 0.0, 0)
        else:
            return None

    # =============================================================================
    #   close operation long
    # =============================================================================
    def close_long(self, symbol, amount=0.0, price=0.0, type=1):
        """
        市价卖
        :param symbol: 货币对的名称
        :param amount: 卖的数量
        :return:
        """
        # print("short_market:", symbol, amount)
        if self.market_name == "huobi":
            return util.future_api.openOrder(symbol, -amount, price, type)
        else:
            return None

    # =============================================================================
    #   close operation
    # =============================================================================
    def close_short(self, symbol, amount=0.0, price=0.0, type=1):
        """
        市价卖 price=0.0
        :param price:
        :param symbol: 货币对的名称
        :param amount: 卖的数量
        :return:
        """
        # print("short_market:", symbol, amount)
        if self.market_name == "huobi":
            return util.future_api.openOrder(symbol, amount, price, type)
        else:
            return None

    """===========================================================================
    # close_all_order
    
    """

    def close_all_order(self, symbol=None):
        if symbol is not None:
            return util.future_api.closeOrder(symbol)
        else:
            return None

    # =============================================================================
    #       get orderlist
    # =============================================================================
    def get_last_order_price(self, symbol):
        # print(orders_list('eoseth','filled'))
        if self.market_name == "huobi":
            r=uf_api.get_mytrades(symbol,1)
            print(r)
            if r is not None:
                lastorder = r['price']
                amount = r['size']
                if amount>0:_type=1
                else:
                    _type =-1
                return lastorder, amount, _type
            else:return -1, 0, 0
            # n = 0
            # d2 = uh.get_today()
            # d1 = uh.get_start_day(d2)
            # while (n < 5):
            #     n = n + 1
            #     #                d1_str=time.strftime("%Y-%m-%d", d1)
            #     #                d2_str=time.strftime("%Y-%m-%d", d2)
            #     #                result=exchangeConnection.huobi.huobiService913.orders_list(symbol,states,None,d1,d2)
            #     result = self.get_orders_history(symbol)
            #     print(result)
            #     return
            #     if result.get("status") == "ok":
            #         if result.get('data') != []:
            #             #               lastorder = result.get('data')[0].get('price')
            #             lastorder = result['data'][0]['price']
            #             amount = result['data'][0]['filled-amount']
            #             _type = result['data'][0]['type']
            #             return lastorder, amount, _type
            #         else:
            #             print(d1)
            #             d2 = uh.get_start_day(d1)
            #             d1 = uh.get_start_day(d2)
            #     else:
            #         return -1, 0, 0
            # else:
            #     return -1, 0, 0
        else:
            return 0, 0, 0

    # =============================================================================
    #         get order history
    # =============================================================================
    def get_orders_history(self,symbol='ETH_USDT'):
        # if self.market_name == "huobi":
            #            n=0
            #            d2=uh.get_today()
            #            d1=uh.get_start_day(d2)
            #            while(n<30):
            #                n=n+1
            #                d1_str=time.strftime("%Y-%m-%d", d1)
            #                d2_str=time.strftime("%Y-%m-%d", d2)
            #            result=exchangeConnection.huobi.huobiService913.orders_list(symbol,states,None,d1,d2)
        result = util.future_api.get_closed_posHistories(symbol)
        #result = {'time': 1663654338, 'pnl': '-167.0362105', 'side': 'short', 'contract': 'ETH_USDT', 'text': 'api'}
        if result is not None:
            if True:
                #                    order_list=['']*10
                #               lastorder = result.get('data')[0].get('price')
                cols_list = [''] * 4
                cols_list[0] = uh.time_to_timestr(result[0]['time'])
                cols_list[1] = result[0]['pnl']

                cols_list[2] = result[0]['side']
                cols_list[3] = result[0]['contract']
                # cols_list[4] = result['data'][0]['price']
                # cols_list[5] = result['data'][0]['field-amount']
                # cols_list[6] = result['data'][0]['field-cash-amount']
                # cols_list[7] = result['data'][0]['field-fees']
                # cols_list[8] = result['data'][0]['source']
                # cols_list[9] = result['data'][0]['state']
                # cols_list[10] = result['data'][0]['account-id']
                return cols_list
            else:
                #                    print(d1)
                #                    d2=uh.get_start_day(d1)
                #                    d1=uh.get_start_day(d2)
                #                        continue
                return 0, 0, 0
        else:
            return -1, 0, 0


    # =============================================================================
    #
    # =============================================================================
    def get_orderid(self, clienorderid):
        if self.market_name == "huobi":
            result = exchangeConnection.huobi.huobiService913.get_orderid(clienorderid)
            #            print(result)
            return result

    # =============================================================================
    #
    # =============================================================================
    def order_normal(self, order_result):
        """
        是否成功下单
        :param order_result: 下单返回结果
        :return:
        """
        if self.market_name == "huobi":
            #            base_cur, quote_cur = symbol.split("_")
            if order_result.status_code < 400:
                return True
            else:
                return False

    def get_order_processed_amount(self, order_result, symbol=None):
        # print("get_order_processed_amount:", order_result, symbol)
        if self.market_name == "huobi":
            pass
        else:
            return None

    def cancel_order(self, order_result, symbol=None):
        if self.market_name == "huobi":
            #            base_cur, quote_cur = symbol.split("_")
            #            if quote_cur == "usdt":
            #                if base_cur == "eth":
            #                    return exchangeConnection.bitex.bitexService.BitexServiceAPIKey(key_index="USDT_1")\
            #                        .cancel_order(str(order_result.get("data")))  # {'status': 'ok', 'data': '2705970'}
            #                elif base_cur == "etc":
            #                    return exchangeConnection.bitex.bitexService.BitexServiceAPIKey(key_index="USDT_1")\
            #                        .cancel_order(str(order_result.get("data")))  # {'status': 'ok', 'data': '2705970'}
            #                elif base_cur == "btc":
            return exchangeConnection.huobi.huobiService913.cancel_order(
                order_result.get("data"))  # {'status': 'ok', 'data': '2705970'}
        #                elif base_cur == "ltc":
        #                    return exchangeConnection.huobi.huobiService.cancelOrder(
        #                        2, order_result.get("id"), "usdt", "cancel_order")
        #            elif quote_cur == "btc":
        #                if base_cur == "ltc" or base_cur == "eth" or base_cur =="etc":
        #                    return exchangeConnection.pro.proService.ProServiceAPIKey(key_index="USDT_1").cancel_order(
        #                           order_result.get("data"))
        else:
            return None

    def get_order_status(self, order_result, symbol):
        # print("get_order_status:", order_result, symbol)
        if self.market_name == "huobi":
            #            base_cur, quote_cur = symbol.split("_")
            result = exchangeConnection.huobi.huobiService913.order_info(order_result.get("data"))
            return result.get('data').get("state")
        else:
            return None

    # def get_symbols(self, symbol=''):
    #     if self.market_name == "huobi":
    #         #            base_cur, quote_cur = symbol.split("_")
    #         result = huobi.acc_info.get('contract')
    #         return list1
    #     else:
    #         return None

    def get_total_assets(self):
        if self.market_name == "huobi":
            #            base_cur, quote_cur = symbol.split("_")
            r = self.update_marketInfo()
            acc_total_assets = r.get('total')  # 账户总资产，total = position_margin + order_margin + available
            return (acc_total_assets)
        else:
            return None

    def market_detail(self,quote_cur , base_cur):
        prefix = "/api/v4"
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

        url = '/futures/usdt/order_book'
        symbol = quote_cur.upper() + '_' + base_cur.upper()
        print(symbol)
        query_param = 'contract=' + symbol+'&limit=1'
        r = requests.request('GET', acfg.gateApi + prefix + url + "?" + query_param, headers=headers)
        print(r.json())
        return r.json()


# test
if __name__ == "__main__":
    huobi = Market()
    print(huobi.acc_id)
    print(huobi.acc_info)
    a=huobi.get_accountInfo()
    print(a)
    b = huobi.account_available()
    print(b)
    c = huobi.get_market_close()
    print(c)
    d=huobi.market_detail('eth','usdt')
    print('d=',d)
    # huobi.open_short_market('ETH_USDT', 1)
    # huobi.close_short('ETH_USDT', 0.1, 0.0, 1)
    # print(huobi.close_all_order('ETH_USDT'))
    ##        print huobi.(get_symbols())
    ##    print(huobi.get_accounts())
    print(huobi.get_total_assets())
    print(huobi.get_orders_history())
    huobi.get_last_order_price()
#     print(huobi.get_orderid(62657991295))
