#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import time
import requests
import json


class ChatHandler(object):
    def __init__(self):
        pass

    # 登录
    def login(self, url, data):
        # check_url = check_url +  '?username=' + data['username']
        # res = requests.get(check_url)
        send_data = {
            'username': data['username'],
            'room_id': data['room_id']
        }
        res = requests.post(url, data=send_data)

        return res.content

    # 发言
    def say(self, url, data):
        data['createtime'] = time.time()
        res = requests.post(url, data=data)
        return res.content

    # 聊天记录
    def record(self, url, number, room_id):
        url = url + '?number=' + str(number) + '&room_id=' + str(room_id)
        res = requests.get(url)

        return res.content

    # 用户信息
    def user_info(self, url, username):
        url = url + '?username=' + username
        res = requests.get(url)

        return res.content

    # 禁言
    def get_mute(self):
        pass

    # 移除禁言
    def remove_mute(self):
        pass

    # 添加禁言
    def add_mute(self, url, data):
        res = requests.post(url, data=data)
        return res.content

    # 管理员
    def get_admin(self):
        pass

    # 删除管理员
    def remove_admin(self):
        pass

    # 添加管理员
    def add_admin(self):
        pass

    # 黑名单
    def get_black_list(self):
        pass

    # 删除黑名单
    def remove_black_list(self):
        pass

    # 添加黑名单
    def add_black_list(self):
        pass

    # 踢人
    def kicking(self):
        pass

    # 添加好友
    def add_friends(self):
        pass

    # 删除好友
    def remove_friends(self):
        pass

    # 获取好友
    def get_friends(self):
        pass

    # get token
    def get_token(self, url, username, password):
        url = url + '?username=' + username + '&password=' + password
        res = requests.get(url)

        return res.content
