'''
Author: MaiXiaoMeng
Date: 2021-01-16 11:14:04
LastEditors: MaiXiaoMeng
LastEditTime: 2021-01-16 11:41:00
FilePath: \actions_auto_run\scripts\tieba_baidu_com.py
'''
# -*- coding:utf-8 -*-
import os
from os import error
import requests
import hashlib
import time
import copy
import logging

try:
    import tools.utils as tools
except:
    import sys
    sys.path.append('./')
    import tools.utils as tools


class tieba_baidu_com:
    def __init__(self):
        self.session = requests.session()
        self.name = 'tieba.baidu.com'
        self.date = time.strftime("%Y-%m-%d", time.localtime())
        self.log_head = f'[{self.date}][{self.name}] '
        self.bduss = tools.get_environment_variables('TIEBA_BAIDU_BDUSS')
        self.LIKIE_URL = "http://c.tieba.baidu.com/c/f/forum/like"
        self.TBS_URL = "http://tieba.baidu.com/dc/common/tbs"
        self.SIGN_URL = "http://c.tieba.baidu.com/c/c/forum/sign"
        self.COOKIE = "Cookie"
        self.BDUSS = "BDUSS"
        self.EQUAL = r'='
        self.EMPTY_STR = r''
        self.TBS = 'tbs'
        self.PAGE_NO = 'page_no'
        self.ONE = '1'
        self.TIMESTAMP = "timestamp"
        self.DATA = 'data'
        self.FID = 'fid'
        self.SIGN_KEY = 'tiebaclient!!!'
        self.UTF8 = "utf-8"
        self.SIGN = "sign"
        self.KW = "kw"

        self.HEADERS = {
            'Host': 'tieba.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        }
        self.SIGN_DATA = {
            '_client_type': '2',
            '_client_version': '9.7.8.0',
            '_phone_imei': '000000000000000',
            'model': 'MI+5',
            "net_type": "1",
        }

    def get_tbs(self):
        headers = copy.copy(self.HEADERS)
        headers.update({self.COOKIE:  self.EMPTY_STR.join(
            [self.BDUSS, self.EQUAL, self.bduss])})
        try:
            tbs = self.session.get(
                url=self.TBS_URL, headers=headers, timeout=5).json()[self.TBS]
        except Exception as error:
            tools.send_message(self.log_head + '获取tbs出错')
            tools.send_message(self.log_head + '重新获取tbs开始')
            tbs = self.session.get(
                url=self.TBS_URL, headers=headers, timeout=5).json()[self.TBS]
        tools.send_message(self.log_head + f'获取TBS:{tbs}')
        return tbs

    def get_favorite(self):
        i = 1
        data = {
            'BDUSS': self.bduss,
            '_client_type': '2',
            '_client_id': 'wappc_1534235498291_488',
            '_client_version': '9.7.8.0',
            '_phone_imei': '000000000000000',
            'from': '1008621y',
            'page_no': '1',
            'page_size': '200',
            'model': 'MI+5',
            'net_type': '1',
            'timestamp': str(int(time.time())),
            'vcode_tag': '11',
        }
        res = self.session.post(
            url=self.LIKIE_URL, data=self.encodeData(data), timeout=5).json()

        returnData = {}
        returnData = res
        if 'forum_list' not in returnData:
            returnData['forum_list'] = []
        if res['forum_list'] == []:
            return {'gconforum': [], 'non-gconforum': []}
        if 'non-gconforum' not in returnData['forum_list']:
            returnData['forum_list']['non-gconforum'] = []
        if 'gconforum' not in returnData['forum_list']:
            returnData['forum_list']['gconforum'] = []
        while 'has_more' in res and res['has_more'] == '1':
            i = i + 1
            data = {
                'BDUSS': self.bduss,
                '_client_type': '2',
                '_client_id': 'wappc_1534235498291_488',
                '_client_version': '9.7.8.0',
                '_phone_imei': '000000000000000',
                'from': '1008621y',
                'page_no': str(i),
                'page_size': '200',
                'model': 'MI+5',
                'net_type': '1',
                'timestamp': str(int(time.time())),
                'vcode_tag': '11',
            }
            data = self.encodeData(data)
            try:
                res = self.session.post(
                    url=self.LIKIE_URL, data=data, timeout=5).json()
            except Exception as error:
                tools.send_message(self.log_head + '获取关注的贴吧出错')
                continue
            if 'forum_list' not in res:
                continue
            if 'non-gconforum' in res['forum_list']:
                returnData['forum_list']['non-gconforum'].append(
                    res['forum_list']['non-gconforum'])
            if 'gconforum' in res['forum_list']:
                returnData['forum_list']['gconforum'].append(
                    res['forum_list']['gconforum'])

        t = []
        for i in returnData['forum_list']['non-gconforum']:
            if isinstance(i, list):
                for j in i:
                    if isinstance(j, list):
                        for k in j:
                            t.append(k)
                    else:
                        t.append(j)
            else:
                t.append(i)

        for i in returnData['forum_list']['gconforum']:
            if isinstance(i, list):
                for j in i:
                    if isinstance(j, list):
                        for k in j:
                            t.append(k)
                    else:
                        t.append(j)
            else:
                t.append(i)
        tools.send_message(self.log_head + f'获取关注的贴吧: {len(t)} 个')
        return t

    def client_sign(self, bduss, tbs, fid, kw):
        # tools.send_message(self.log_head + f'开始签到贴吧:{kw}')
        data = copy.copy(self.SIGN_DATA)
        data.update(
            {
                self.BDUSS: bduss,
                self.FID: fid,
                self.KW: kw,
                self.TBS: tbs,
                self.TIMESTAMP: str(int(time.time()))
            }
        )
        data = self.encodeData(data)
        res = self.session.post(url=self.SIGN_URL, data=data, timeout=5).json()
        return res

    def encodeData(self, data):
        s = self.EMPTY_STR
        keys = data.keys()
        for i in sorted(keys):
            s += i + self.EQUAL + str(data[i])
        sign = hashlib.md5(
            (s + self.SIGN_KEY).encode(self.UTF8)).hexdigest().upper()
        data.update({self.SIGN: str(sign)})
        return data

    def main(self):
        tbs = self.get_tbs()
        favorites = self.get_favorite()
        for j in favorites:
            self.client_sign(tbs, tbs, j["id"], j["name"])
        tools.send_message(self.log_head + '签到结束')

    def run(self):
        try:
            self.main()
        except Exception as error:
            message_context = f'运行异常,脚本又挂掉啦~'
            tools.send_message(self.log_head + message_context)
            print(error)
