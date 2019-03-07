#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import requests
import time
from common import config
import threading
import json

def collect():
    while True:
        url = ""
        try:
            res = requests.get(url)

            #print(time.strftime("%Y-%m-%d %H:%M:%S  ", time.localtime()) + 'runing...')
        except:
            pass
        time.sleep(1)


if __name__ == "__main__":
    count = 0
    while count < 50:
        print(count)
        count = count + 1
        t = threading.Thread(target=collect)
        t.start()

