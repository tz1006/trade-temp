#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# filename: log.py
# version: v2
# description: 日志系统

from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import os
import time

class logging():
    def __init__(self):
        self.__check_dir()
        self.__start()
    def __check_dir(self):
        if os.path.exists('log') == False:
            os.makedirs('log')
    def __start(self):
        pool = ThreadPoolExecutor(max_workers=1)
        pool.submit(self.write)
    def write(self):
        self.list = []
        while True:
            if len(self.list) == 0:
                time.sleep(5)
            else:
                filename = self.list[0][0]
                message = self.list[0][1]
                with open('log/%s.log' % filename , 'a') as f:
                    f.write(message)
                self.list.remove(self.list[0])
    def sms(self, text):
        message = '%s  %s\n' % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), text)
        print(text)
        json = ('sms', message)
        self.list.append(json)
    def stocklist(self, text):
        message = '%s  %s\n' % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), text)
        print(text)
        json = ('stocklist', message)
        self.list.append(json)
    def worklist(self, text):
        message = '%s  %s\n' % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), text)
        print(text)
        json = ['worklist', message]
        self.list.append(json)
    # temp
    def suspend(self, text):
        message = '%s  %s\n' % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), text)
        print(text)
        json = ['suspend', message]
        self.list.append(json)



log = logging()

if __name__ != '__main__':
    #print('loggggggggging')
    pass
