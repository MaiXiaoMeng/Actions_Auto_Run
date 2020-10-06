# coding=utf-8
import os
import time

import demjson
import requests


def get_environment_variables(variable_name):
    try:
        return os.environ[variable_name]
    except Exception as ERROR:
        with open('variables.json', 'r', encoding='utf-8') as file_object:
            return demjson.decode(file_object.read())[variable_name]


def send_message(context):
    print(context)
    with open('log.txt', mode='a+', newline='\n')as file:
        file.write(context + '\n')


class www_mkgal_com:
    def __init__(self):
        self.session = requests.session()
        self.name = 'www.mkgal.com'
        self.sign_token = None
        self.date = time.strftime("%Y-%m-%d", time.localtime())
        self.log_head = f'[{self.date}][{self.name}] '
        self.email = MKGAL_EMAIL
        self.password = MKGAL_PASSWORD

    def get_mkgal_sign(self):
        url = 'https://www.mkgal.com/sign'
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://www.mkgal.com',
            'Sec-Fetch-Dest': 'empty',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://www.mkgal.com/',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'}
        data = {
            'email': self.email,
            'password': self.password}
        response = self.session.post(url=url, headers=headers, data=data)
        response_json = response.json()['obj']
        message_context = f'用户名:{response_json["nickname"]} 当前金币:{response_json["jf"]} + {response_json["qs"]}'
        send_message(self.log_head + message_context)
        self.sign_token = response_json["token"]

    def get_mkgal_addJf(self):
        url = 'https://www.mkgal.com/addJf'
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'X-Auth-Token': self.sign_token,
            'Sec-Fetch-Dest': 'empty',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://www.mkgal.com/',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'}
        response = self.session.get(url=url, headers=headers).json()
        if response['code'] == 0:
            message_context = f'每日签到成功'
        else:
            message_context = f'每日签到失败'
        send_message(self.log_head + message_context)

    def run(self):
        self.get_mkgal_sign()
        self.get_mkgal_addJf()


if __name__ == '__main__':
    MKGAL_EMAIL = get_environment_variables('MKGAL_EMAIL')
    MKGAL_PASSWORD = get_environment_variables('MKGAL_PASSWORD')
    www_mkgal_com().run()
