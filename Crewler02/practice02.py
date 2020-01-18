# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 06:42:23 2019

@author: Chen Tian

E-mail: chentianfighting@126.com
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

urllst = ['https://book.douban.com/tag/%E7%94%B5%E5%BD%B1?start=0&type=T',
 'https://book.douban.com/tag/%E7%94%B5%E5%BD%B1?start=20&type=T',
 'https://book.douban.com/tag/%E7%94%B5%E5%BD%B1?start=40&type=T',
 'https://book.douban.com/tag/%E7%94%B5%E5%BD%B1?start=60&type=T',
 'https://book.douban.com/tag/%E7%94%B5%E5%BD%B1?start=80&type=T']    
     # 添加网址

def get_data(ui):
    ri = requests.get(ui)
    soupi = BeautifulSoup(ri.text,'lxml')
    lis = soupi.find('ul',class_="subject-list").find_all('li')
    lst = []
    
    for li in lis:
        dic = {}
        dic['书名'] = re.sub(r'\s+','',li.h2.text)
        infors = re.sub(r'\s+','',li.find('div',class_="pub").text)
        #print(infors)
        dj = re.search(r'.*/([.\d]*)\D*',infors) #re.search(r'.*/(.\d+)\D*',infors)不能匹配到小数点
        if dj:
            #print(dj.group())
            dic['定价'] = dj.group(1)
        nf = re.search(r'.*/([-\d]*)/',infors)
        if nf:
            dic['年份'] = nf.group(1)
        lst.append(dic)    
    return dic

if __name__ == "__main__":
    datalst = []
    errorlst = []
    for u in urllst:
        try:
            datalst.append(get_data(urllst[0]))
            print('数据采集成功，总共采集%i条数据' % len(datalst))
        except:
            errorlst.append(u)
            print('数据采集失败，数据网址为：',u)
    df = pd.DataFrame(datalst)