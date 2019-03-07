#!/usr/bin/python
# -*- coding: UTF-8 -*-
# from websocket_server import WebsocketServer
from common.websocket_server import WebsocketServer
from socketserver import BaseRequestHandler, ThreadingTCPServer
import time
from common import config
import json
import requests
import os, sys
import threading
import asyncio
""" 
summary
百家乐服务端
接收荷官发送数据，并post至服务器
返回结果转发至玩家端
"""

config_file = 'config\Baccarat_V1.ini'
dealerSocket_List = []  # 荷官
payerSocket_List = []  # 玩家
BUF_SIZE = 1024
console_log = 1


# 发送数据到玩家端 server
class send_Thread(threading.Thread):
    def __init__(self, socket, data):
        threading.Thread.__init__(self)
        self.socket = socket
        self.data = data

    def run(self):
        try:
            print(self.data.decode('utf-8'))
            self.socket.send(self.data)
        except:
            try:
                print("payer remove~")
                payerSocket_List.remove(self.socket)
            except:
                print("发送失败~")
                pass


# 连接socket
class ServerHandler(BaseRequestHandler):
    def handle(self):
        address, pid = self.client_address
        payerSocket_List.append(self.request)
        if console_log == 1:
            print('玩家服务端：%s 已连接!' % address)
        while True:
            data = self.request.recv(BUF_SIZE)
            if len(data) > 0:
                cur_thread = threading.current_thread()

                # 打印
                if console_log == 1:
                    print(time.strftime("[Payer Server Accept] %Y-%m-%d %H:%M:%S  ", time.localtime()) + data.decode(
                        'utf-8'))
                self.request.send(data)
                # print(data.decode('utf-8'))
                # 发送到web
            # self.send_web(data)
            # #写入文件
            # self.write_file(data)
            else:
                if console_log == 1:
                    print('玩家服务端：%s 已关闭!' % address)
                break

        # 发送至玩家服务端
        def send_client(self, data):
            # self.write_file(data)
            # 线程发送
            for s in payerSocket_List:
                send_Thread(s, data).start()


class Start_Thread(threading.Thread):
    def __init__(self, addr, handler):
        threading.Thread.__init__(self)
        self.addr = addr
        self.handler = handler

    def run(self):
        if console_log == 1:
            print("玩家服务端等待连接...%s" % (self.addr[1]))
        global server
        server = ThreadingTCPServer(self.addr, self.handler)
        server.serve_forever()

async def Start_TCPServer(addr, handler):
    global server
    server = await  ThreadingTCPServer(addr, handler)
    await  server.serve_forever()

def write_file(name, data):
    localtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    file = 'log/' + name + '_' + localtime + '.txt'
    with open(file, 'a+') as f:
        f.write(data.decode('utf-8') + '\n')


# 加入
def new_client(client, server):
    dealerSocket_List.append(client)

    if console_log == 1:
        print('荷官端：(%d) 已连接!' % client['id'])
    server.send_message_to_all("welcome")


# 断开连接
def client_left(client, server):
    dealerSocket_List.remove(client)
    if console_log == 1:
        print("荷官端连接：(%d) 已断开" % client['id'])


# 收到消息
def message_received(client, server, message):
    print(message)
    if len(message) > 200:
        message = message[:200] + '..'
    if console_log == 1:
        print("收到荷官端消息:", message)
    server.send_message_to_all(message)
    send_web(message)


# POST WEB
def send_web(data):
    con = config.Config(config_file)
    domain = con.get('API', 'DOMAIN')
    url = con.get('API', 'URL')

    send_data = {
        'table_id': 5,
        'out': 'ss',
    }
    print("----------------")
    res = requests.post(domain + url, data=send_data)
    print(res.content.decode('utf-8'))
    if res.status_code == 200:
        send_client(res.content);
        if console_log == 1:
            print(time.strftime("[Web] %Y-%m-%d %H:%M:%S  ", time.localtime()) + res.content.decode('utf-8'))
    else:
        # pass
        # print(res.status_code)
        print('http error')


def send_client(data):
    # 线程发送
    for s in payerSocket_List:
        send_Thread(s, data).start()


# 计数
def get_count():
    while True:
        time.sleep(5)
        count = len(dealerSocket_List)
        pcount = len(payerSocket_List)
        if console_log == 1:
            print("荷官连接数：(%d)" % count)
            print("玩家服务器连接数：(%d)" % pcount)

# 程序入口
def main():
    # read config
    con = config.Config(config_file)
    HOST = con.get('DEALER_SERVER', 'HOST')
    PORT = int(con.get('DEALER_SERVER', 'PORT'))
    console_log = int(con.get('SERVER', 'CONSOLE_LOG'))

    server_host = con.get('SERVER', 'HOST')
    server_post = int(con.get('SERVER', 'PORT'))

    # 玩家服务端连接
    s1 = Start_Thread((server_host, server_post), ServerHandler)
    s1.start()

    # 统计
    t2 = threading.Thread(target=get_count)
    t2.start()

    webserver = WebsocketServer(PORT, HOST)
    webserver.set_fn_new_client(new_client)
    webserver.set_fn_client_left(client_left)
    webserver.set_fn_message_received(message_received)
    webserver.run_forever()


if __name__ == '__main__':
    # 创建LOG文件夹
    path = "log"
    if not os.path.exists(path):
        os.mkdir(path, 777)

    # 开始
    #main()
    asyncio.run(main())
