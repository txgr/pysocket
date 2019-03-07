#!/usr/bin/python
# -*- coding: UTF-8 -*-
import threading
from common import config
from websocket_server import WebsocketServer
import time
import socket
import os,sys
BUF_SIZE = 1024
webSocket_List = []

server_socket = ''
config_file = 'config\serverhtml5_client.ini'

"""
webserver 
"""


# 加入
def new_client(client, server):
    webSocket_List.append(client)

    print("有人上线了~")
    server.send_message_to_all("welcome~!")


# 断开连接
def client_left(client, server):
    webSocket_List.remove(client)
    print("web连接：(%d) 已断开" % client['id'])


# 收到消息
def message_received(client, server, message):
    print(message)
    if len(message) > 200:
        message = message[:200] + '..'
    print("收到Web:", message)


# 计数
def get_count():
    while True:
        time.sleep(5)
        count = len(webSocket_List)
        print("当前Web连接数：(%d)" % count)


# 开始
def start_websocket():
    con = config.Config(config_file)
    HOST = con.get('HTML5_SOCKET', 'HOST')
    PORT = int(con.get('HTML5_SOCKET', 'PORT'))

    # 统计
    t2 = threading.Thread(target=get_count)
    t2.start()

    global webserver
    webserver = WebsocketServer(PORT, HOST)
    webserver.set_fn_new_client(new_client)
    webserver.set_fn_client_left(client_left)
    webserver.set_fn_message_received(message_received)
    webserver.run_forever()


def connect_server(host, port):
    server_socket = doConnect(host, port)

    while True:
        try:
            data = server_socket.recv(1024)
            if len(data) > 0:
                print(time.strftime("[Accept] %Y-%m-%d %H:%M:%S  ", time.localtime()) + data.decode('utf-8'))
                # print(data)
                # 群发
                global webserver
                webserver.send_message_to_all(data)
        except:
            time.sleep(5)
            server_socket = doConnect(host, port)


def doConnect(host, port):
    print('正在重新连接服务器......')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except:
        pass
    return sock


def main():
    con = config.Config(config_file)
    host = con.get('RECEIVE', 'HOST')
    port = con.get('RECEIVE', 'PORT')

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

    # 接收发牌数据
    main()
