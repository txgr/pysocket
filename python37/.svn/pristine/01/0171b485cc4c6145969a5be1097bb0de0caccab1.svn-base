#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import time
import requests
import json

class dealdata():
    # 写入文件
    def write_file(self, data):
        localtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        file = 'log/' + localtime + '.txt'
        with open(file, 'a+') as f:
            f.write(data + '\n')


    # POST WEB
    def send_web(self, data):
        from common import config
        config = config.Config()
        url = config.get('WEB', 'URL')
        send_data = {
            'table_id': 22222,
            'out': data.decode('utf-8'),
        }
        r = requests.post(url, data=send_data)
        if r.status_code == 200:
            self.startCommand(r.content)
        else:
            print('错误代码：' + r.status_code)


    # 解析网站返回内容
    def startCommand(self, data):
        print(json.loads(data))


    #
    # def send_client(self, data):
    #     import client
    #     client = client()
    #     client.connect()
    #     client.send(data)


    # 返回桌号
    def get_lotcode(self):
        from common import config
        config = config.Config()
        code = config.get('WEB', 'LOTCODE')
        url = config.get('WEB', 'LOTCODE_URL')

        send_data = {
            'lotcode': code
        }
        r = requests.post(url, data=send_data)

        if r.status_code == 200:
            tables = json.loads(r.content)
            return tables
        else:
            print('获取桌号失败,错误代码：' + r.status_code)

if __name__ == '__main__':
    pass
    # config = config.Config()
    # HOST = config.get('CONTROL','IP')
    # PORT = int(config.get('CONTROL','PROT'))
    # print(HOST)
    # d = dealdata()
    # d.write_file("中国")