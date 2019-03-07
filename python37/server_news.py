#!/usr/bin/python
# -*- coding: UTF-8 -*-
from socketserver import BaseRequestHandler, ThreadingTCPServer
import threading
import time
from common import config
import json
import requests
import os, sys

BUF_SIZE = 2048
HEARTBEAT = 5
socket_list = []
socket_html5 = ''
client_socket = ''
start_port = 0
total_port = 0
config_file = 'config/server_news.ini'
"""
控牌端服务器
"""


# 发送数据到false server
class send_Thread(threading.Thread):
    def __init__(self, socket, data):
        threading.Thread.__init__(self)
        self.socket = socket
        self.data = data

    def run(self):
        try:
            self.socket.send(self.data)
        except:
            try:
                socket_list.remove(self.socket)
            except:
                pass


# 接受webserver连接
class Html5Handler(BaseRequestHandler):
    def handle(self):
        address, pid = self.client_address
        socket_list.append(self.request)
        while True:
            data = self.request.recv(BUF_SIZE)
            if len(data) > 0:
                # 打印
                print(time.strftime("[Send] %Y-%m-%d %H:%M:%S :", time.localtime()) + data.decode('utf-8'))
                # print(data.decode('utf-8'))
            else:
                print('close')
                break


# 连接socket
class ServerHandler(BaseRequestHandler):
    def handle(self):
        address, pid = self.client_address
        print('控牌：%s 已连接!' % address)
        while True:
            data = self.request.recv(BUF_SIZE)
            print(data)
            if len(data) > 0:
                cur_thread = threading.current_thread()

                # 打印
                #print(time.strftime("[Accept] %Y-%m-%d %H:%M:%S  ", time.localtime()) + data.decode('utf-8'))
                # print(data.decode('utf-8'))
                # 发送到web
               # self.send_web(data)
                # #写入文件
                # self.write_file(data)
            else:
                print('close')
                break

    # 写入文件
    def write_file(self, data):
        localtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        file = 'log/' + localtime + '.txt'
        with open(file, 'a+') as f:
            f.write(data.decode('utf-8') + '\n')

    # POST WEB
    def send_web(self, data):
        from common import config
        config = config.Config(config_file)
        url = config.get('WEB', 'URL')

        str = self.dealStr(data)
        if str:
            send_data = {
                'table_id': 5,
                'out': str,
            }
            print(url)
            print(send_data)
            res = requests.post(url, data=send_data)
            if res.status_code == 200:
                str = res.content.decode('utf-8').split('|')
                print(time.strftime("[Web] %Y-%m-%d %H:%M:%S  ", time.localtime()) + res.content.decode('utf-8'))

                # print(str)
                self.send_client(res.content)
                # self.startCommand(res.content)
            else:
                # pass
                # print(res.status_code)
                print('http error')

    def dealStr(self, data):
        str = data.decode('utf-8').split(',')
        # 取第三个, 号后的内容
        if (str[0] != 'LON') and (len(str) > 3):
            str1 = ','.join(str[4:])
            str1 = str1[:-1]
            return str1

    # 解析网站返回内容
    def startCommand(self, data):
        print(json.loads(data))

    # 发送flash
    def send_client(self, data):
        # self.write_file(data)
        # 进程发送
        for s in socket_list:
            send_Thread(s, data).start()


class Start_Thread(threading.Thread):
    def __init__(self, addr, handler):
        threading.Thread.__init__(self)
        self.addr = addr
        self.handler = handler

    def run(self):
        print("等待连接...%s" % (self.addr[1]))
        server = ThreadingTCPServer(self.addr, self.handler)
        server.serve_forever()


# 程序入口
def main():
    # read config
    con = config.Config(config_file)
    HOST = con.get('CONTROL', 'IP')
    PORT = int(con.get('CONTROL', 'PORT'))

    HEARTBEAT = int(con.get('SERVER', 'HEARTBEAT'))

    # get lot code
    # deal = dealdata.dealdata()
    # tables = deal.get_lotcode()
    tables = [5]

    # 连接html5服务
    server_host = con.get('SERVER', 'HOST')
    server_port = int(con.get('SERVER', 'PORT'))

    # acdr
    adr = (HOST, PORT)
    addr = (server_host, server_port)

    # 主线程
    #s1 = Start_Thread(addr, Html5Handler)
    s2 = Start_Thread(adr, ServerHandler)

    #s1.start()
    s2.start()


if __name__ == '__main__':
    # 创建LOG文件夹
    path = "log"
    if not os.path.exists(path):
        os.mkdir(path, 777)

    # 开始
    main()
