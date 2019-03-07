#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import json
import requests
from threading import Thread
import time
import os, sys

"""
彩票采集
"""

config_file = 'config/collect.ini'
site_time_file = "config/site.json"
config_json_file = "config/collect.json"


# 采集
class CollectHandler(Thread):
    def __init__(self, icount, lotcode, cycleid, close_time, site, url, dalay, is_write_file, is_console_show):
        """
        :param icount: 线程计数
        :param lotcode: 网站代码
        :param cycleid: 期号
        :param close_time: 时间
        :param site: 网站
        :param url: 采集地址
        :param dalay: 等待时间
        :param is_write_file: 是否写入log
        :param is_console_show: 是否在控制台显示
        """
        super().__init__()
        self.icount = icount
        self.lotcode = lotcode
        self.cycleid = cycleid
        self.close_time = close_time
        self.site = site
        self.url = url
        self.dalay = dalay
        self.is_write_file = is_write_file
        self.is_console_show = is_console_show

    def run(self):
        data = "?site=" + self.site + "&lotcode=" + self.lotcode + "&cycleid=" + self.cycleid + "&stime=" + self.close_time
        url = self.url + data
        # print(url)
        sdata = [{'site': self.site, 'code': self.lotcode, 'cycleid': self.cycleid}]

        try:
            res = requests.get(url)
            print(url)
            if res.status_code == 200:
                if res.text == '0' or res.text.strip() == '':
                    pass
                else:
                    # 采集到数据
                    str_log = time.strftime("%Y-%m-%d %H:%M:%S  ", time.localtime()) + str(sdata) + res.text
                    if self.is_console_show == 'TRUE':
                        print(str_log)
                    if self.is_write_file == 'TRUE':
                        self.write_file(str_log)
            else:
                print('error code：' + res.status_code)
        except:
            pass

    # 写入log
    def write_file(self, data):
        localtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        file = 'log/' + localtime + '_collect.txt'
        with open(file, 'a+') as f:
            f.write(data + '\n')


# 从网站取出
def get_OpenLog():
    from common import config
    config = config.Config(config_file)
    open_url = config.get('SERVER', 'OPEN_URL')
    try:
        # get url
        res = requests.get(open_url)
        return res.content
    except:
        return False


# 装载collect.json
def loadConfig():
    f = open(config_json_file, encoding='utf-8')
    return json.load(f)


# 装载site.json

def loadSiteTime():
    f = open(site_time_file, encoding='utf-8')
    return json.load(f)


# 主
class MainHandler(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:

            data = get_OpenLog()
            json_str = json.loads(data)

            # 读取配置文件
            from common import config
            con = config.Config(config_file)
            collect_url = con.get('SERVER', 'COLLECT_URL')

            dalay_time = con.get('SERVER', 'DALAY')
            is_write_file = con.get('SERVER', 'IS_WRITE_FILE')
            is_console_show = con.get('SERVER', 'IS_CONSOLE_SHOW')
            try:
                task_number = len(json_str)
                if task_number == 0:
                    print(time.strftime("%Y-%m-%d %H:%M:%S  ", time.localtime()) + '  当前无采集任务，等待中...')
                else:
                    s = '并发数：' + str(task_number)
                    print(time.strftime("%Y-%m-%d %H:%M:%S  ", time.localtime()) + s + '  采集进行中...')

                    table = loadConfig()
                    stime = loadSiteTime()

                    icount = 0
                    for s in json_str:
                        # 需要采集
                        lotcode = s.get('lotcode')
                        cycleid = s.get('cycleid')
                        close_time = s.get('close_time')

                        site = table.get(lotcode)
                        if lotcode and site:
                            site = site.split(',')

                            # 开始线程采集
                            for site_str in site:
                                # 没有就设为5
                                dalay = stime.get(site_str, 5)
                                thread = CollectHandler(icount, lotcode, cycleid, close_time, site_str, collect_url, dalay,
                                                        is_write_file, is_console_show)
                                thread.start()
                                # thread.join()
                                icount += 1
            except:
                pass
            # 等待后继续

            time.sleep(int(dalay_time))


if __name__ == '__main__':
    # 创建LOG文件夹
    path = "log"
    if not os.path.exists(path):
        os.mkdir(path, 777)

    thread = MainHandler()
    thread.start()
