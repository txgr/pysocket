#!/usr/bin/python
# -*- coding: UTF-8 -*-
from socketserver import BaseRequestHandler, ThreadingTCPServer
import threading
import time
from common import config
import json
import requests
import os, sys
# from websocket_server import WebsocketServer
from common.websocket_server import WebsocketServer

# import redis

BUF_SIZE = 2048
HEARTBEAT = 5
socket_list = []
socket_html5 = ''
client_socket = ''
webSocket_List = []
start_port = 50000
config_file = 'config/server_news_v2.ini'
"""
控牌端服务器
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
    print(client)
    print(server)
    if len(message) > 200:
        message = message[:200] + '..'
    print("收到Web:", message)


# 计数
def get_count():
    while True:
        time.sleep(5)
        count = len(webSocket_List)
        print("当前Web连接数：(%d)" % count)


def start_websocket():
    con = config.Config(config_file)
    host = con.get('WEB_SOCKET', 'HOST')
    port = int(con.get('WEB_SOCKET', 'PORT'))
    # print(port)
    # # 统计
    t = threading.Thread(target=get_count)
    t.start()

    global webserver
    webserver = WebsocketServer(port, host)
    webserver.set_fn_new_client(new_client)
    webserver.set_fn_client_left(client_left)
    webserver.set_fn_message_received(message_received)
    webserver.run_forever()


# 连接socket
class ServerHandler(BaseRequestHandler):
    def handle(self):
        address, pid = self.client_address
        print('控牌：%s 已连接!' % address)
        server_port = self.request.getsockname()[1]
        print(server_port)
        while True:
            data = self.request.recv(BUF_SIZE)
            if len(data) > 0:
                cur_thread = threading.current_thread()

                # 打印
                print(time.strftime("[Accept] %Y-%m-%d %H:%M:%S  ", time.localtime()) + data.decode('utf-8'))
                # print(data.decode('utf-8'))
                # 发送到web
                self.send_web(data, server_port)
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
    def send_web(self, data, server_port):
        from common import config
        config = config.Config(config_file)
        url = config.get('WEB_URL', 'URL')
        url += "resultByBjz.php?act=com"
        table_id = int(server_port) - start_port
        str = self.dealStr(data)
        if str:
            send_data = {
                'table_id': table_id + 1,
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

    # 发送至 WEB
    def send_client(self, data):
        webserver.send_message_to_all(data)
        # self.write_file(data)
        # 进程发送
        # for s in socket_list:
        #     send_Thread(s, data).start()


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


class Start_Thread(threading.Thread):
    def __init__(self, addr, handler):
        threading.Thread.__init__(self)
        self.addr = addr
        self.handler = handler

    def run(self):
        print("等待连接...%s" % (self.addr[1]))
        server = ThreadingTCPServer(self.addr, self.handler)
        server.serve_forever()


def initTable():
    from common import config
    config = config.Config(config_file)
    url = config.get('WEB_URL', 'URL')
    url += "socketApi.php?act=tables"
    res = requests.get(url)
    if res.status_code == 200:
        return json.loads(res.content)
    else:
        return False


# 程序入口
def main():
    # read config
    con = config.Config(config_file)
    HOST = con.get('CONTROL', 'IP')
    PORT = int(con.get('CONTROL', 'PORT'))

    # 开始端口 控牌端
    start_port = int(con.get('CONTROL', 'START_PORT'))

    table = initTable()

    # 监听websocket
    t1 = threading.Thread(target=start_websocket)
    t1.start()

    # 控牌端服务
    for p in table:
        addr = (HOST, (int(p) + start_port))
        s = Start_Thread(addr, ServerHandler)
        s.start()

    # 主线程
    # s2 = Start_Thread(adr, ServerHandler)
    # s2.start()


if __name__ == '__main__':
    # 创建LOG文件夹
    path = "log"
    if not os.path.exists(path):
        os.mkdir(path, 777)

    # try:
    #     red = redis.Redis(host='216.118.245.238', port=6379, decode_responses=True, encoding='utf-8',password=654321)
    #     red.set('name', '中国')
    #     tt = red.get('name')
    #     print(tt)
    # except redis.ConnectionError as e:
    #     print(e)

    # 开始
    main()
