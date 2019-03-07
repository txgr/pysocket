#!/usr/bin/python
# -*- coding: UTF-8 -*-

import memcache
import json


class Ckmemcached():
    def __init__(self, isDebug=True):
        self.mc = memcache.Client(['127.0.0.1:11211'], debug=isDebug)

    def getKey(self, key=''):
        return self.mc.get(key)

    def setKey(self, key='', value=''):
        self.mc.set(key, value)

    def delete(self,key = ''):
        self.delete(key)

if __name__ == '__main__':
    ck = Ckmemcached()
    ck.setKey('11', '{"retCode":0,"retMsg":"成功"}')
    s = ck.getKey('11')
    print(s)
    jv = json.loads(s)
    print(jv)
