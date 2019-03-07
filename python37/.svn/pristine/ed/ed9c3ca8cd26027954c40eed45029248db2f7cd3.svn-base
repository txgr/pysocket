#!/usr/bin/python
# -*- coding: UTF-8 -*-
import threading
from common import config
from websocket_server import WebsocketServer
import time
import socket
import os, sys
import requests
import json

BUF_SIZE = 1024
webSocket_List = []
SLEEP = 5
console_log = 1

# 桌号
table = 0

dealer_socket = None
config_file = 'config\Payer_Server_V1.ini'

""" 
summary
玩家服务端
接收荷官服务端发送的数据，群发至玩家终端
并接受玩家终端操作数据，发送到荷官服务端
返回结果转发至玩家端
"""


# 加入
def new_client(client, server):
    webSocket_List.append(client)
    if console_log == 1:
        print('玩家：(%d) 已连接!' % client['id'])
    server.send_message_to_all("welcome")


# 断开连接
def client_left(client, server):
    webSocket_List.remove(client)
    if console_log == 1:
        print("玩家：(%d) 已关闭" % client['id'])


# 收到消息
def message_received(client, server, message):
    print(message)
    if len(message) > 200:
        message = message[:200] + '..'
    if console_log == 1:
        print("收到玩家:", message)


# 计数
def get_count():
    while True:
        time.sleep(5)
        count = len(webSocket_List)
        if console_log == 1:
            print("当前玩家连接数：(%d)" % count)


# 开始
def start_websocket():
    con = config.Config(config_file)
    HOST = con.get('HTML5_SOCKET', 'HOST')
    PORT = int(con.get('HTML5_SOCKET', 'PORT'))
    POS = int(con.get('HTML5_SOCKET', 'POS'))
    PORT += POS

    # 统计
    t2 = threading.Thread(target=get_count)
    t2.start()

    global webserver
    webserver = WebsocketServer(PORT, HOST)
    webserver.set_fn_new_client(new_client)
    webserver.set_fn_client_left(client_left)
    webserver.set_fn_message_received(message_received)
    webserver.run_forever()


# 连接荷官服务器
def connect_server(host, port):
    dealer_socket = doConnect(host, port)

    while True:
        try:
            data = dealer_socket.recv(1024)
            if len(data) > 0:
                if console_log == 1:
                    print(time.strftime("[Dealer Server Accept] %Y-%m-%d %H:%M:%S  ", time.localtime()) + data.decode(
                        'utf-8'))

                # send_dealer_server(data)
                # 群发
                global webserver
                webserver.send_message_to_all(data)
        except:
            time.sleep(SLEEP)
            dealer_socket = doConnect(host, port)


def doConnect(host, port):
    if console_log == 1:
        print('正在连接荷官服务器:', host, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        # 连接成功发送桌号
        data = {
            'table': table,
            'command': 'login'
        }
        json_str = json.dumps(data)
        sock.send(json_str)
        if console_log == 1:
            print('荷官服务器连接成功:', host, port)
    except:
        pass
    return sock


# 发送数据至荷官服务器
def send_dealer_server(data):
    try:
        dealer_socket.send(data)
    except:
        pass


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
    print(domain + url)
    print(res.content.decode('utf-8'))
    if res.status_code == 200:
        if console_log == 1:
            print(time.strftime("[Web] %Y-%m-%d %H:%M:%S  ", time.localtime()) + res.content.decode('utf-8'))
    else:
        # pass
        # print(res.status_code)
        print('http error')


# 日志
def write_file(name, data):
    localtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    file = 'log/' + name + '_' + localtime + '.txt'
    with open(file, 'a+') as f:
        f.write(data.decode('utf-8') + '\n')


# 连接荷官服务器
def main():
    con = config.Config(config_file)
    host = con.get('BACCARAT_SERVER', 'HOST')
    port = con.get('BACCARAT_SERVER', 'PORT')
    SLEEP = int(con.get('BACCARAT_SERVER', 'SLEEP'))
    table = con.get('BACCARAT_SERVER', 'TABLE')
    console_log = int(con.get('SERVER', 'CONSOLE_LOG'))

    t1 = threading.Thread(target=connect_server, args=(host, int(port)))
    t1.start()


if __name__ == '__main__':
    # 创建LOG文件夹
    path = "log"
    if not os.path.exists(path):
        os.mkdir(path, 777)

    # 监听web
    t1 = threading.Thread(target=start_websocket)
    t1.start()

    # 连接荷官服务器
    main()
