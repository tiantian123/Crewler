# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 08:06:35 2019

@author: Chen Tian

E-mail: chentianfighting@126.com
"""
import requests
from bs4 import BeautifulSoup
import pymongo
import re
import time
import random
from selenium import webdriver
import warnings
warnings.filterwarnings('ignore')
# 不发出警告

def get_url(city_url,n):
    '''
    【分页网页url获取】函数
    city_url: 不同城市起始网址
    n：页数
    '''
    lst = []
    for i in range(n):
        lst.append(city_url+'/pg%d/' % (i+1))
    return lst

def get_data(ui,d_h,table):
    '''
    【数据采集及mongo入库】函数
    ui: 数据信息网页
    d_h: user-agent信息
    table: mongo集合对象
    '''
    ri = requests.get(url=ui,headers=d_h)
    #print(ri)
    # 访问网页
    soupi = BeautifulSoup(ri.text,'lxml')
    # 解析网页
    lis = soupi.find('ul',class_="sellListContent").find_all('li')
    n = 0
    for li in lis:
        dic = {}
        dic['标题'] = li.find('div',class_='title').text
        info1 = li.find('div',class_='houseInfo').text.split('|')
        dic['小区'] = info1[0]
        dic['户型'] = info1[1]
        dic['面积'] = info1[2]
        dic['朝向'] = info1[3]
        dic['装修'] = info1[4]
        dic['价格'] = li.find('div', class_="totalPrice").text
        dic['单价'] = li.find('div',class_="unitPrice").text
        #print(dic)
        info2 = li.find('div',class_="positionInfo").text
        dic['房屋信息'] = info2
        info3 = li.find('div',class_="followInfo").text
        dic['关注人数'] = re.search(r'(\d+)人关注',info3).group(1)
        dic['发布时间'] = re.search(r'(.+)发布',info3).group(1)
        dic['链接'] = li.find('a')['href']
        table.insert_one(dic) #数据入库
        n += 1
    return n

if __name__ == '__main__':
    urllst = get_url('https://cs.lianjia.com/ershoufang/yuelu/',15)
    # 数据分页网址获取
    #h_dic = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    h_dic = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    db = myclient['链家']
    datatable = db['长沙岳麓区二手房']
    datatable.delete_many({})
    # 设置数据库集合
    
    errorlst = []
    count = 0
    for u in urllst:
        time.sleep(random.randint(1,5)) # 随机等待1-5秒
        try:
            count += get_data(u,h_dic,datatable)
            print('数据采集成功，总共采集%i条数据' % count)
        except:
            errorlst.append(u)
            print('数据采集失败，数据网址为：',u)
            # 采集数据
            



    
        
        