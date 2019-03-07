#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import threading
from common import config

threads = []

host = ''
username = ''
password = ''
lotcode = ''
rows = ''
threads_number = 0

"""
并发测试
"""
def start(url):
    headers = header()
    get_url = 'http://' + url
    xsrf_url = session.get(get_url, headers=headers).text
    BeautifulSoup(xsrf_url, 'html.parser')

    post_data = {
        'username': username,
        'password': password,
        'last_webos': 'Pc IE: 8.0',
        'hascode': '',
    }
    r = session.post(get_url + '/index.php?controller=web_login&action=login', data=post_data,
                     headers=headers)

    str1 = str(r.content)

    i = str1.find('/index.php?')
    t = str1.find('";</script>')
    s = str1[i:t]
    url = get_url + s
    xsrf_url = session.get(url, headers=headers).text
    BeautifulSoup(xsrf_url, "html.parser")
    url = get_url + '/index.php?controller=dsn_index'
    xsrf_url = session.get(url, headers=headers).text
    BeautifulSoup(xsrf_url, "html.parser")

    headers = header_json()
    post_data = {
        'lotcode': lotcode,
        'rows': rows
    }
    url = get_url + '/index.php?controller=Mob_CreateOrderM&action=Suborder'

    thread = {}
    threads = []
    for i in range(int(threads_number)):
        thread[i] = start_Thread(i, url, post_data, headers)

        threads.append(thread[i])

    for t in threads:
        t.start()


class start_Thread(threading.Thread):
    def __init__(self, counter, url, post_data, headers):
        threading.Thread.__init__(self)
        self.counter = counter
        self.url = url
        self.post_data = post_data
        self.headers = headers

    def run(self):
        print('线程：%s 开始' % (self.counter))
        s = time.time()
        r = session.post(self.url, data=self.post_data, headers=self.headers)
        t = time.time() - s
        print('线程：%s 用时： %s' % (self.counter, t))


# 头部
def header():
    header = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Host": host,
        'Accept-Language': 'zh-cn',
        "Accept-Encoding": 'gzip, deflate',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1'
    }
    return header


def header_json():
    header = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"),
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Host": host,
        'Accept-Language': 'zh-cn',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        "Accept-Encoding": 'gzip, deflate',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1'
    }
    return header


session = requests.session()
if __name__ == "__main__":
    con = config.Config('config\ConcurrentTest.ini')
    host = con.get('SERVER', 'host')
    username = con.get('SERVER', 'username')
    password = con.get('SERVER', 'password')
    lotcode = con.get('SERVER', 'lotcode')
    threads_number = con.get('SERVER', 'threads_number')
    rows = con.get('SERVER', 'rows')

    start(host)
