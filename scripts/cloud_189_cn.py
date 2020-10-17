import base64
import hashlib
import re
import time

import requests
import rsa

try:
    import tools.utils as tools
except:
    import sys
    sys.path.append('./')
    import tools.utils as tools


class cloud_189_cn:
    def __init__(self):
        self.session = requests.session()
        self.name = 'cloud_189_cn'
        self.date = time.strftime("%Y-%m-%d", time.localtime())
        self.log_head = f'[{self.date}][{self.name}] '
        self.email = tools.get_environment_variables('CLOUD_189_EMAIL')
        self.password = tools.get_environment_variables('CLOUD_189_PASSWORD')
        self.BI_RM = list("0123456789abcdefghijklmnopqrstuvwxyz")
        self.b64map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    def int2char(self, a):
        return self.BI_RM[a]

    def b64tohex(self, a):
        d = ""
        e = 0
        c = 0
        for i in range(len(a)):
            if list(a)[i] != "=":
                v = self.b64map.index(list(a)[i])
                if 0 == e:
                    e = 1
                    d += self.int2char(v >> 2)
                    c = 3 & v
                elif 1 == e:
                    e = 2
                    d += self.int2char(c << 2 | v >> 4)
                    c = 15 & v
                elif 2 == e:
                    e = 3
                    d += self.int2char(c)
                    d += self.int2char(v >> 2)
                    c = 3 & v
                else:
                    e = 0
                    d += self.int2char(c << 2 | v >> 4)
                    d += self.int2char(15 & v)
        if e == 1:
            d += self.int2char(c << 2)
        return d

    def rsa_encode(self, j_rsakey, string):
        rsa_key = f"-----BEGIN PUBLIC KEY-----\n{j_rsakey}\n-----END PUBLIC KEY-----"
        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(rsa_key.encode())
        result = self.b64tohex(
            (base64.b64encode(rsa.encrypt(f'{string}'.encode(), pubkey))).decode())
        return result

    def calculate_md5_sign(self, params):
        return hashlib.md5('&'.join(sorted(params.split('&'))).encode('utf-8')).hexdigest()

    def login(self):
        url = "https://cloud.189.cn/udb/udb_login.jsp?pageId=1&redirectURL=/main.action"
        response = self.session.get(url)
        captcha_token = re.findall(
            r"captchaToken' value='(.+?)'", response.text)[0]
        lt = re.findall(r'lt = "(.+?)"', response.text)[0]
        return_url = re.findall(r"returnUrl = '(.+?)'", response.text)[0]
        param_id = re.findall(r'paramId = "(.+?)"', response.text)[0]
        j_rsakey = re.findall(
            r'j_rsaKey" value="(\S+)"', response.text, re.M)[0]
        self.session.headers.update({"lt": lt})

        url = "https://open.e.189.cn/api/logbox/oauth2/loginSubmit.do"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/76.0',
            'Referer': 'https://open.e.189.cn/',
        }
        data = {
            "appKey": "cloud",
            "accountType": '01',
            "userName": f"{{RSA}}{self.rsa_encode(j_rsakey, self.email)}",
            "password": f"{{RSA}}{self.rsa_encode(j_rsakey, self.password)}",
            "validateCode": "",
            "captchaToken": captcha_token,
            "returnUrl": return_url,
            "mailSuffix": "@189.cn",
            "paramId": param_id
        }
        response = self.session.post(
            url, data=data, headers=headers, timeout=10)
        if(response.json()['result'] == 0):
            redirect_url = response.json()['toUrl']
            self.session.get(redirect_url)
            message_context = f'帐号登录成功'
            tools.send_message(self.log_head + message_context)
            return True
        else:
            message_context = f'帐号登录失败'
            tools.send_message(self.log_head + message_context)
            return False

    def main(self):
        if self.login():
            rand = str(round(time.time()*1000))
            surl = f'https://api.cloud.189.cn/mkt/userSign.action?rand={rand}&clientType=TELEANDROID&version=8.6.3&model=SM-G930K'
            url = f'https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN&activityId=ACT_SIGNIN'
            url2 = f'https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN_PHOTOS&activityId=ACT_SIGNIN'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G930K Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 Ecloud/8.6.3 Android/22 clientId/355325117317828 clientModel/SM-G930K imsi/460071114317824 clientChannelId/qq proVersion/1.0.6',
                "Referer": "https://m.cloud.189.cn/zhuanti/2016/sign/index.jsp?albumBackupOpened=1",
                "Host": "m.cloud.189.cn",
                "Accept-Encoding": "gzip, deflate",
            }
            response = self.session.get(surl, headers=headers)
            netdiskBonus = response.json()['netdiskBonus']
            if(response.json()['isSign'] == "false"):
                message_context = f'未签到，签到获得{netdiskBonus}M空间'
            else:
                message_context = f'已签到，签到获得{netdiskBonus}M空间'
            tools.send_message(self.log_head + message_context)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G930K Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 Ecloud/8.6.3 Android/22 clientId/355325117317828 clientModel/SM-G930K imsi/460071114317824 clientChannelId/qq proVersion/1.0.6',
                "Referer": "https://m.cloud.189.cn/zhuanti/2016/sign/index.jsp?albumBackupOpened=1",
                "Host": "m.cloud.189.cn",
                "Accept-Encoding": "gzip, deflate",
            }
            response = self.session.get(url, headers=headers)
            if ("errorCode" in response.text):
                if(response.json()['errorCode'] == "User_Not_Chance"):
                    message_context = f'第一次抽奖次数不足'
                else:
                    message_context = f'第一次抽奖失败'
            else:
                description = response.json()['description']
                message_context = f'第一次抽奖抽奖获得{description}'
            tools.send_message(self.log_head + message_context)

            response = self.session.get(url2, headers=headers)
            if ("errorCode" in response.text):
                if(response.json()['errorCode'] == "User_Not_Chance"):
                    message_context = f'第二次抽奖次数不足'
                else:
                    message_context = f'第二次抽奖失败'
            else:
                description = response.json()['description']
                message_context = f'第二次抽奖抽奖获得{description}'
            tools.send_message(self.log_head + message_context)

    def run(self):
        try:
            self.main()
        except Exception as error:
            message_context = f'运行异常,脚本又挂掉啦~'
            tools.send_message(self.log_head + message_context)
            print(error)


if __name__ == "__main__":
    cloud_189_cn().run()
