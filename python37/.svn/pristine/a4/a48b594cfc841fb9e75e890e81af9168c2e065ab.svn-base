# autobance.py
# coding:utf-8
import os
import time
import random
import urllib
import requests
# import urllib2
import threading


class bncwork(threading.Thread):
    def __init__(self, lotcode, sltime):
        threading.Thread.__init__(self)
        if lotcode == 'all':
            lotcode = ''
            sltime = 15
        self.lotcode = lotcode
        self.sltime = sltime
        self.gurl = 'http://api.uc6969.net/psp/autobalance.php'

    def run(self):
        print('start  for %s whit %s sleep %s' % (self.gurl, self.lotcode, self.sltime))
        while True:
            time.sleep(self.sltime)
            gurl = self.gurl + '?topcode=' + self.lotcode
            data = {}
            print(gurl)
            try:
                requests.get(gurl)
                #msg = gethttp(gurl)
               # print(msg.decode('utf-8'))
            except:
                #print('err')
                pass


if __name__ == "__main__":
    lotlist = ('pks', 'ssg', 'ssh', 'ssx', 'ssc', 'sgx', 'scq', 'stj', 'shn', 'ssn')
    scnn = {}
    for lot in lotlist:
        sltime = random.randint(15, 25)
        scnn[lot] = bncwork(lot, sltime)
        scnn[lot].start()
