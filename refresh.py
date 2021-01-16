'''
Author: MaiXiaoMeng
Date: 2021-01-16 11:14:04
LastEditors: MaiXiaoMeng
LastEditTime: 2021-01-16 11:27:11
FilePath: \actions_auto_run\refresh.py
'''
import os

SCRIPTS_BASE_DIR = './scripts/'

if __name__ == '__main__':
    for scripts in os.listdir(SCRIPTS_BASE_DIR):
        os.system(f'python ./scripts/{scripts}')
