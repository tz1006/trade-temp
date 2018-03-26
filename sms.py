#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: worklist.py
# version: v2
# description: sms.py

from log import log

import nexmo
import time
#from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


class sms():
    sleep = 2
    number = 16018666656
    key = 'd1258708'
    secret = 'No1secret'
    def __init__(self, phone):
        self.phone = phone
        self.list = []
        self._login()
        self.start()
    def _login(self):
        self._client = nexmo.Client(key=self.key, secret=self.secret)
        message = '登录短信客户端'
        #print(message)
        log.sms(message)
    def start(self):
        message = '开启发送短信'
        #print(message)
        log.sms(message)
        pool = ThreadPoolExecutor(max_workers=1)
        pool.submit(self.starter)
    def starter(self):
        self.status = True
        while self.status == True:
            if len(self.list) == 0:
                time.sleep(2)
            else:
                text = self.list[0]
                self._send_sms(text)
                self.list.remove(text)
    def stop(self):
        self.status = False
        message = '停止发送短信'
        #print(message)
        log.sms(message)
    def send(self, text):
        self.list.append(text)
    def _send_sms(self, text):
        c = 0
        result = None
        while result != '0':
            #print(c)
            if c == 5:
                status = '失败'
                break
            result = self._client.send_message({
            'from': self.number,
            'to': self.phone,
            'text': text,
            'type': 'unicode'
            })['messages'][0]['status']
            status = '成功'
            c += 1
        message = '发送%s： %s ' % (status, text)
        #print(message)
        sms.log(message)
    def help(self):
        print('''sms.list\nsms.send(number, text)\n/log
            ''')


sms = sms(16267318573)

if __name__ != '__main__':
    #print('sms = sms(16267318573)')
    pass


#sms = sms(16267318573)
#sms.send('001')
#sms.send('002')
#sms.send('003')
#sms.send('004')
#sms.send('005')



