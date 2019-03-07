#!/usr/bin/python
# -*- coding: UTF-8 -*-
from common import config
# from websocket_server import WebsocketServer
import time
import threading
import os, sys
from common import chathandler
from common.websocket_server import WebsocketServer
import requests

webSocket_List = []
illegal_Name = []
accept_Name = []
config_file = 'config\chatroom.ini'
import json


# 禁言 10分钟，1小时，12小时，1天，自定义
# 屏弊此人发言
# 踢人
# 查看最后发言时间
# 设为特别关注
# 修改群名片
# 查看此人名片
# 发给指定人(其它人可见，不可见）
# 设置管理员
# 等级，头像


# 加入
def new_client(client, server):
    pass


# 断开连接
def client_left(client, server):
    for cli in webSocket_List:
        if cli['client'] == client:
            webSocket_List.remove(cli)
            print("web连接：(%d) 已断开" % client['id'])
            break

#给指定用户发消息
def send_message_client(client,server,message):
    for cli in webSocket_List:
        if cli['client'] == client:
            server.send_message(client,message)
            break

# 收到消息
def message_received(client, server, message):
    try:
        msg = json.loads(message)
        type = msg.get('type', "None")
        if type == 'Login':
            # 登录
            login(client, server, msg)
        elif type == 'Say':
            # 发言
            say(client, server, msg)
        elif type == 'Banned':
            # 禁言
            banned(client, server, msg)
        elif type == 'Shield':
            # 屏弊
            shield(client, server, msg)
        elif type == 'Last':
            # 最后发言
            last(client, server, msg)
        elif type == 'Focus':
            # 关注
            focus(client, server, msg)
        elif type == 'Details':
            # 查看此人名片
            details(client, server, msg)
        elif type == 'Set':
            # 设置
            set(client, server, msg)
        elif type == 'Avatar':
            # 设置头像
            avatar(client, server, msg)
        elif type == 'None':
            # 其它数据
            pass
        else:
            pass
    except:
        pass


# 设置头像
def avatar(client, server, msg):
    pass


# 设置
def set(client, server, msg):
    pass


# 查看此人名片
def details(client, server, msg):
    pass


# 关注
def focus(client, server, msg):
    pass


# 最后发言
def last(client, server, msg):
    pass


# 屏弊
def shield(client, server, msg):
    pass


# 禁言
def banned(client, server, msg):

    res = chathandler.add_mute(api['url'] + api['set_mute'], msg)
    #发给管理员
    server.send_message(client,res)
    r = json.loads(res)

    # 禁言成功，通知被禁言者
    if r['code'] == 1:
        send_message_client(client,server,res)

# 发言
def say(client, server, msg):

    if msg['username'] in illegal_Name:
        server.send_message(client, '请先登录~~~')
    else:
        for cli in webSocket_List:
            if cli['username'] == msg['username']:
                # 发言
                res = chathandler.say(api['url'] + api['set_record'], msg)
                if msg['to_username'] == 'All':
                    # 群发消息
                    server.send_message_to_all(res)
                else:
                    # 私聊  暂未处理
                    server.send_message_to_all(res)
                if is_console_show == 'ON':
                    print(res.decode('utf-8'))
                break


def login(client, server, msg):
    # 登录
    res = chathandler.login(api['url'] + api['login'], msg)
    # 发送登录信息
    server.send_message(client, res)
    res = json.loads(res)
    # 群发登录消息
    if res['code'] == 1:
        List = {}
        List['client'] = client
        List['username'] = msg['username']
        List['data'] = res['data']
        List['room_id'] = msg['room_id']
        webSocket_List.append(List)

        server.send_message_to_all(json.dumps(res))

        # 聊天记录
        log = chathandler.record(api['url'] + api['get_history'], 10, msg['room_id'])
        server.send_message(client, log)

        # 清除禁止
        if msg['username'] in illegal_Name:
            illegal_Name.remove(msg['username'])

    else:
        illegal_Name.append(msg['username'])
        # 登录失败并强制下线
        client_left(client, server)


# 计数
# def get_count():
#     while True:
#         time.sleep(5)
#         count = len(webSocket_List)
#         print("当前Web连接数：(%d)" % count)

# 读取配置
def getConfigApi():
    api = {}
    con = config.Config(config_file)
    api['url'] = con.get('API', 'url')
    api['login'] = con.get('API', 'login')
    api['api_username'] = con.get('API', 'api_username')
    api['api_password'] = con.get('API', 'api_password')
    api['set_record'] = con.get('API', 'set_record')
    api['get_history'] = con.get('API', 'get_history')
    api['get_history_number'] = con.get('API', 'get_history_number')
    api['set_permissions'] = con.get('API', 'set_permissions')
    api['get_user_info'] = con.get('API', 'get_user_info')
    api['get_room'] = con.get('API', 'get_room')
    api['check_user_url'] = con.get('API', 'check_user_url')
    api['set_mute'] = con.get('API', 'set_mute')

    return api


# 取出可用聊天室
def getRoom(url):
    res = requests.get(url)

    res = json.loads(res.content)
    return res['data']
    # print(res)
    # room_dict = {}
    # for ls in res['data']:
    #     room_dict[ls['key']] = ls['id']
    #
    # return room_dict


# 开始
def start_websocket(port):
    webserver = WebsocketServer(int(port), '0.0.0.0')
    webserver.set_fn_new_client(new_client)
    webserver.set_fn_client_left(client_left)
    webserver.set_fn_message_received(message_received)
    webserver.run_forever()


if __name__ == '__main__':

    # 创建LOG文件夹
    path = "log"
    if not os.path.exists(path):
        os.mkdir(path, 777)

    con = config.Config(config_file)
    HOST = con.get('SERVER', 'host')
    PORT = int(con.get('SERVER', 'port'))

    is_write_file = con.get('SERVER', 'is_write_file')
    is_console_show = con.get('SERVER', 'is_console_show')

    api = getConfigApi()
    # 可用聊天室
    # room_dict = getRoom(api['url'] + api['get_room'])
    # for list in room_dict:
    #     port = list.get('port')
    #     t1 = threading.Thread(target=start_websocket, args=(port,))
    #     t1.start()
    chathandler = chathandler.ChatHandler()
    #p = sys.argv[1]
    webserver = WebsocketServer(PORT, HOST)
    webserver.set_fn_new_client(new_client)
    webserver.set_fn_client_left(client_left)
    webserver.set_fn_message_received(message_received)
    webserver.run_forever()
