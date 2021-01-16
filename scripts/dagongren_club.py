'''
Author: MaiXiaoMeng
Date: 2021-01-16 11:14:04
LastEditors: MaiXiaoMeng
LastEditTime: 2021-01-16 11:39:27
FilePath: \actions_auto_run\scripts\dagongren_club.py
'''
import math
import random
import requests


class dagongren_club:
    def __init__(self):
        self.base_url = 'https://dagongren.club'
        self.headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/vnd.api+json',
            'Sec-Fetch-Dest': 'empty',
            'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIiLCJqdGkiOiIwYTJjZDNlNTY3NGM1NmViNjA3Zjg3YTE4ODY3NjFjOTQyMjM2YjdjYTFhZjhjMjUyYzhjMjk5OGNiNDQ2OTlmOGFlNzk4ZGNmOWVlOTk2YiIsImlhdCI6MTYwNTk1OTkxMSwibmJmIjoxNjA1OTU5OTExLCJleHAiOjE2MDg1NTE5MTEsInN1YiI6IjcxIiwic2NvcGVzIjpbbnVsbF19.pAefv4DbV7FyDCR0bUoCF8t4fraBLXN6OwpYYNOIIv7-7PSb8oMeiZRoGd1LxrvYrBEKH4hVf4IPtiQrSse_dYJkbeDIeE7sw9q3VWAB4iSBYDqcwVngowWJMv-VT4Cn05WFMuUwaeki29j13wDszRg3RBf3RLnYJCl2McwTp9_eL-3ChpRUPrm15T0nQ3dg4-N9_PPgElftmk_WY8YgJ2S0_RqSCFEVMR-y3aEs0s2uNfF_08_6W87p2d2kz1BdzLNTf1tQ8eEPR9x9n4YVwXKBR06e7zfjNRfTI8ib-uIUgVHDBqX9ob0al_MK_ZHG5hoSAC-ErmYa4BL2W2TCKA',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://dagongren.club/thread/84',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

    def delete_theme_interface_single(self, ID):
        return requests.delete(f'{self.base_url}/api/threads/{ID}', headers=self.headers)

    def create_new_theme_interface(self, data):
        requests.post(
            f'{self.base_url}/api/threads', headers=self.headers, data=data
        )

    def generate_random_gps(base_log=None, base_lat=None, radius=None):
        radius_in_degrees = radius / 111300
        u = float(random.uniform(0.0, 1.0))
        v = float(random.uniform(0.0, 1.0))
        w = radius_in_degrees * math.sqrt(u)
        t = 2 * math.pi * v
        x = w * math.cos(t)
        y = w * math.sin(t)
        longitude = y + base_log
        latitude = x + base_lat
        return longitude, latitude

    def run(self):
        log, lat = self.generate_random_gps(
            base_log=102.7, base_lat=25, radius=100000
        )
        location = ["左心房", "右心房"]
        context = requests.get('https://api.oick.cn/dog/api.php').text[1:-1]
        emoji = [
            ':kelian:', ':haqian:', ':woshou:', ':aixin:', ':zuohengheng:', ':weixiao:', ':jingkong:', ':tiaopi:',
            ':touxiao:', ':youling:', ':caidao:', ':cahan:', ':hecai:', ':keai:', ':ciya:', ':saorao:', ':jingxi:',
            ':ku:', ':piezui:', ':se:', ':xia:', ':yinxian:', ':zhouma:', ':kulou:', ':xu:', ':jingya:', ':doge:',
            ':bizui:', ':yangtuo:', ':shouqiang:', ':baoquan:', ':yun:', ':lanqiu:', ':zhemo:', ':guzhang:', ':shengli:',
            ':zaijian:', ':dabing:', ':deyi:', ':hanxiao:', ':kun:', ':hexie:', ':daku:', ':wozuimei:', ':xiaoku:',
            ':xigua:', ':huaixiao:', ':liulei:', ':lenghan:', ':qiudale:', ':zhayanjian:', ':qiaoda:', ':baojin:', ':OK:',
            ':xiaojiujie:', ':gouyin:', ':youhengheng:', ':tuosai:', ':nanguo:', ':quantou:', ':haixiu:', ':koubi:',
            ':qiang:', ':pijiu:', ':bishi:', ':yiwen:', ':liuhan:', ':wunai:', ':aini:', ':bangbangtang:', ':penxue:',
            ':haobang:', ':qinqin:', ':xiaoyanger:', ':fendou:', ':ganga:', ':shuai:', ':juhua:', ':baiyan:', ':fanu:',
            ':jie:', ':chi:', ':kuaikule:', ':zhuakuang:', ':shui:', ':dan:', ':aoman:', ':fadai:', ':leiben:', ':tu:',
            ':weiqu:', ':xieyanxiao:'
        ]
        data = {
            "data": {
                "type": "threads", "relationships": {
                    "category": {
                        "data": {
                            "type": "categories", "id": "1"}
                    }
                },
                "attributes": {
                    "content": f"{random.choice(emoji)} {context}",
                    "type": "0",
                    "price": 0,
                    "free_words": 0,
                    "attachment_price": 0,
                    "location": random.choice(location),
                    "latitude": lat,
                    "longitude": log,
                    "address": "我住在你心里"
                }
            }
        }
        self.create_new_theme_interface(data)
