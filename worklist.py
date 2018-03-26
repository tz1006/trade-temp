#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: worklist.py
# version: v2
# description: worklist

#from datetime import datetime
from log import log
from stocklist import sl
from concurrent.futures import ThreadPoolExecutor

import sqlite3
import os
from datetime import datetime
from pytz import timezone

class worklist():
    def __init__(self):
        self.list = []
        self.__li = []
        self.stock = sl.stock[:]
    def wave_start(self, w):
        print('start')
        pool = ThreadPoolExecutor(max_workers=1)
        pool.submit(self.wave, w)
    def wave_stop(self):
        self.__wave_status == False
        print('wave stopped')
    def wave(self, w):
        wave_list = []
        self.__wave_status = True
        while self.__wave_status == True:
            self.wave_checker(w)
            for i in self.__li:
                if i not in wave_list:
                    buy_stock(i)
                    message = '%s(%s)涨幅超过%s%%, 现价%s' %(i.name, i.code, w, i.price()[0])
                    log.worklist(message)
                    sms.send(message)
                    wave_list.append(i)
            print('finish')
            time.sleep(5)
    def wave_checker(self, w):
        self.__li.clear()
        start_time = datetime.now()
        with ThreadPoolExecutor(max_workers=10000) as executor:
            for i in self.stock:
                executor.submit(self.check_wave, i, w)
        end_time = datetime.now()
        timedelsta = (end_time - start_time).seconds
        message = '找到%s个涨幅大于%s的股票，耗时%s秒。' % (len(self.__li), w, timedelsta)
        print(message)
        #return self.__li
    def check_wave(self, instance, w):
        wave = instance.wave()[0]
        if 8 > wave > w:
        	self.__li.append(instance)
        else:
            pass


# 在数据库'KDJ'中建立表 'test'/ TIME/ CODE/ NAME/ BS/ PRICE/ WAVE/ MARKET
def create_form():
    if os.path.exists('database') == False:
        os.makedirs('database')
    #date = datetime.now(timezone('Asia/Shanghai')).strftime('\"%y-%m-%d\"')
    conn = sqlite3.connect('database/transaction.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS TEST
        (TIME TEXT,
        CODE   TEXT,
        NAME  TEXT,
        BS  TEXT,
        PRICE  INT,
        WAVE  INT,
        MARKET   TEXT);''')
    conn.commit()
    conn.close()


# code, name, bs, price, wave, market
def buy_stock(stock):
    time = datetime.now(timezone('Asia/Shanghai')).isoformat(' ')
    code = stock.code
    name = stock.name
    bs = '买入'
    price = stock.price()[0]
    wave = stock.wave()[0]
    market = '-'
    #formname = datetime.now(timezone('Asia/Shanghai')).strftime('\"%y-%m-%d\"')
    conn = sqlite3.connect('database/transaction.db')
    c = conn.cursor()
    #print(code, name, price, average, time)
    c.execute("INSERT OR IGNORE INTO TEST (TIME, CODE, NAME, BS, PRICE, WAVE, MARKET) VALUES (?, ?, ?, ?, ?, ?, ?)", (time, code, name, bs, price, wave, market))
    conn.commit()
    conn.close()
    message = '买入股票%s'
    print('写入 %s 数据成功！' % code)



create_form()
wl = worklist()
wl.wave_start(5.5)

if __name__ == '__main__':
    import code
    code.interact(banner = "", local = locals())


