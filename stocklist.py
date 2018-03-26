#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: stocklist.py
# version: v3
# discription: 下载股票代码并载入股票到sl.stock，drop当日停牌

from stock import stock
from log import log

import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
from concurrent.futures import ThreadPoolExecutor
import json
import time


class stocklist():
    def __init__(self):
        self.list = []
        self.sha = []
        self.sza = []
        self.szzx = []
        self.szcy = []
        self.stock = []
        self.get_list()
        self.__load()
    # 载入列表
    def get_list(self):
        message = '尝试从文件导入股票代码'
        log.stocklist(message)
        try:
            self.list = self.get_list_from_txt()
        except:
            self.dl_list()
    def get_list_from_txt(self):
        with open('database/stocklist.txt', 'r') as f:
            data = f.read()
        li = json.loads(data)
        message = '文件导入%s支股票代码' % len(li)
        log.stocklist(message)
        return li
    def __save_list_to_txt(self):
        data = json.dumps(self.list)
        if os.path.exists('database') == False:
            os.makedirs('database')
        with open("database/stocklist.txt","w") as f:
            f.write(data)
        message = '保存%s支股票代码到文件' % len(self.list)
        log.stocklist(message)
    def dl_list(self):
        message = '从网络下载股票代码'
        log.stocklist(message)
        start_time = datetime.now()
        self.list = self.get_sha() + self.get_sza() + self.get_szzx() + self.get_szcy()
        self.list = list(set(self.list))
        end_time = datetime.now()
        timedelsta = (end_time - start_time).seconds
        message = '成功导入%s支股票代码，耗时%s秒。' % (len(self.list), timedelsta)
        log.stocklist(message)
        self.__save_list_to_txt()
    # 上海A股
    def get_sha(self):
        self.sha.clear()
        start_time = datetime.now()
        url = 'http://query.sse.com.cn/security/stock/getStockListData2.do?&stockType=1&pageHelp.beginPage=1&pageHelp.pageSize=2000'
        header = {
    	  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
    	  'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/'
    	  }
        with requests.session() as s:
            s.headers['connection'] = 'close'
            r = None
            while r == None:
                try:
                    r = s.get(url, timeout=20, headers = header)
                except:
                    pass
        stock_data = r.json()['pageHelp']['data']
        for i in stock_data:
            code = i['SECURITY_CODE_A']
            self.sha.append(code)
        end_time = datetime.now()   
        timedelsta = (end_time - start_time).seconds
        message = '从 上海A股 导入%s支股票代码，耗时%s秒。' % (len(self.sha), timedelsta)
        log.stocklist(message)
        return(self.sha)
    # 深圳A股
    def get_sza(self):
        self.sza.clear()
        start_time = datetime.now()
        index_url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab2&tab2PAGENO=1'
        with requests.session() as s:
            s.headers['connection'] = 'close'
            r = None
            while r == None:
                try:
                    r = s.get(index_url)
                except:
                    pass
        index_html = r.content
        index_soup = BeautifulSoup(index_html, "html.parser")
        index = int(index_soup.select('td')[-3].text.split()[1][1:-1])
        message = '正在获取 深A 代码列表，一共%s页。' % (index+1)
        #log.stocklist(message)
        print(message)
        with ThreadPoolExecutor(max_workers=50) as executor:
            executor.map(self.get_sza_page, range(index))
        end_time = datetime.now()
        timedelsta = (end_time - start_time).seconds
        message = '从 深圳A股 导入%s支股票代码，耗时%s秒。' % (len(self.sza), timedelsta)
        log.stocklist(message)
        return(self.sza)
    def get_sza_page(self, page_num):
        page_num = page_num + 1
        url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab2&tab2PAGENO=%s' % page_num
        with requests.session() as s:
            s.headers['connection'] = 'close'
            r = None
            while r == None:
                try:
                    r = s.get(url, timeout=10)
                except:
                    #print('Error!------------------------------------')
                    #message = '载入第%d页码失败' % page_num
                    #log.stocklist(message)
                    #print(message)
                    pass
        html = r.content
        soup = BeautifulSoup(html, "html.parser")
        source = soup.select('tr[bgcolor="#ffffff"]')
        source1 = soup.select('tr[bgcolor="#F8F8F8"]')
        source += source1
        for i in source:
            code = i.select('td')[2].text
            self.sza.append(code)
        #print(page_num)
    # 深圳中小板
    def get_szzx(self):
        self.szzx.clear()
        start_time = datetime.now()
        index_url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab5&tab5PAGENO=1'
        with requests.session() as s:
            s.headers['connection'] = 'close'
            r = None
            while r == None:
                try:
                    r = s.get(index_url)
                except:
                    pass
        index_html = r.content
        index_soup = BeautifulSoup(index_html, "html.parser")
        index = int(index_soup.select('td')[-3].text.split()[1][1:-1])
        message = '正在获取 深圳中小板 代码列表，一共%s页。' % (index+1)
        #log.stocklist(message)
        print(message)
        with ThreadPoolExecutor(max_workers=50) as executor:
            executor.map(self.get_szzx_page, range(index))
        end_time = datetime.now()
        timedelsta = (end_time - start_time).seconds
        message = '从 深圳中小板 导入%s支股票代码，耗时%s秒。' % (len(self.szzx), timedelsta)
        log.stocklist(message)
        return(self.szzx)
    def get_szzx_page(self, page_num):
        page_num = page_num + 1
        url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab5&tab5PAGENO=%s' % page_num
        with requests.session() as s:
            s.headers['connection'] = 'close'
            r = None
            while r == None:
                try:
                    r = s.get(url, timeout=10)
                except:
                    #message = '载入第%d页码失败' % page_num
                    #log.stocklist(message)
                    #print(message)
                    pass
        html = r.content
        soup = BeautifulSoup(html, "html.parser")
        source = soup.select('tr[bgcolor="#ffffff"]')
        source1 = soup.select('tr[bgcolor="#F8F8F8"]')
        source += source1
        for i in source:
            code = i.a.u.text
            self.szzx.append(code)
    # 深圳创业板
    def get_szcy(self):
        self.szcy.clear()
        start_time = datetime.now()
        index_url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab6&tab6PAGENO=1'
        with requests.session() as s:
            s.headers['connection'] = 'close'
            r = None
            while r == None:
                try:
                    r = s.get(index_url)
                except:
                    pass
        index_html = r.content
        index_soup = BeautifulSoup(index_html, "html.parser")
        index = int(index_soup.select('td')[-3].text.split()[1][1:-1])
        message = '正在获取 深圳创业板 代码列表，一共%s页。' % (index+1)
        #log.stocklist(message)
        print(message)
        with ThreadPoolExecutor(max_workers=50) as executor:
            executor.map(self.get_szcy_page, range(index))
        end_time = datetime.now()
        timedelsta = (end_time - start_time).seconds
        message = '从 深圳创业板 导入%s支股票代码，耗时%s秒。' % (len(self.szcy), timedelsta)
        log.stocklist(message)
        return(self.szcy)
    def get_szcy_page(self, page_num):
        page_num = page_num + 1
        url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab6&tab6PAGENO=%s' % page_num
        with requests.session() as s:
            s.headers['connection'] = 'close'
            r = None
            while r == None:
                try:
                    r = s.get(url, timeout=10)
                except:
                    #message = '载入第%d页码失败' % page_num
                    #log.stocklist(message)
                    #print(message)
                    pass
        html = r.content
        soup = BeautifulSoup(html, "html.parser")
        source = soup.select('tr[bgcolor="#ffffff"]')
        source1 = soup.select('tr[bgcolor="#F8F8F8"]')
        source += source1
        for i in source:
            code = i.a.u.text
            self.szcy.append(code)
    # 载入股票
    def __load(self):
        self.stock.clear()
        message = '尝试加载%s支股票' % len(self.list)
        log.stocklist(message)
        start_time = datetime.now()
        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(self.add, self.list)
        self.__drop()
        end_time = datetime.now()
        timedelsta = (end_time - start_time).seconds
        message = '成功加载%s支股票，耗时%s秒。' % (len(self.list), timedelsta)
        log.stocklist(message)
    def __drop(self):
        c = 0
        for i in self.stock:
            if i.status == False:
                self.stock.remove(i)
                c += 1
        message = '移除%s个停牌股票' % c
        log.stocklist(message)
    def add(self, i):
        a = stock(i)
        self.stock.append(a)
        #print(i)
    def help(self):
        print('''sl.list\nsl.sha\nsl.sza\nsl.szzx\nsl.szcy\nsl.get_sha()\nsl.get_sza()\nsl.get_szzx()\nsl.get_szcy()\n
            ''')


sl = stocklist()

if __name__ != '__main__':
    pass



