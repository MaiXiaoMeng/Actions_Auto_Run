import os
import demjson
import requests


def get_environment_variables(variable_name):
    try:
        return demjson.decode(os.environ['VARIABLE_JSON'])[variable_name]
    except Exception as error:
        with open('variables.json', 'r', encoding='utf-8') as file_object:
            return demjson.decode(file_object.read())[variable_name]


def send_message(context):
    print(context)
    server_qmsg_url = f'https://qmsg.zendee.cn/send/{get_environment_variables("SERVER_QMSG_SCKEY")}'
    server_chan_url = f'https://sc.ftqq.com/{get_environment_variables("SERVER_CHAN_SCKEY")}.send'

    if get_environment_variables('SERVER_QMSG'):
        params = {
            'msg': context
        }
        requests.get(server_qmsg_url, params=params)

    if get_environment_variables('SERVER_CHAN'):
        params = {
            'text': context,
            'desp': context
        }
        requests.get(server_chan_url, params=params)

    with open('log.txt', mode='a+', newline='\n', encoding='UTF-8')as file:
        file.write(context + '\n')
