'''
Author: MaiXiaoMeng
Date: 2020-10-17 12:49:57
LastEditors: MaiXiaoMeng
LastEditTime: 2020-11-21 21:29:11
FilePath: \亚马逊后台数据整理汇总e:\Android\Projects\Python\actions_auto_run\refresh.py
'''
from scripts.tieba_baidu_com import tieba_baidu_com
from scripts.cloud_189_cn import cloud_189_cn
from scripts.www_mikugal_com import www_mikugal_com
from scripts.dagongren_club import dagongren_club

if __name__ == '__main__':
    www_mikugal_com().run()
    cloud_189_cn().run()
    tieba_baidu_com().run()
    dagongren_club().run()
