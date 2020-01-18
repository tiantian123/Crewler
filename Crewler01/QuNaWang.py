# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 07:11:19 2019

@author: Chen Tian

E-mail: chentianfighting@126.com
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

def get_urls(city, n):
    '''
    【分页网页url采集】函数
    city: 城市对应的编码
    n： 网页参数
    return: 存放对应城市的网址
    '''
    lst = []
    ui = 'https://travel.qunar.com/p-cs299878-%s-jingdian-1-' % city
    for i in range(n):
        lst.append(ui + str(i+1))
    return lst

def get_data(ui):
    '''
    【数据采集】函数
    ui：数据信息网页
    d_h：user-agent信息
    d_c：cookies信息
    return:
    '''
    
    ri = requests.get(url=ui)
    soupi = BeautifulSoup(ri.text,'lxml')
    lis = soupi.find('ul',class_="list_item clrfix").find_all('li')
    lst = []
    for li in lis:
        dic = {}
        dic['景点名称'] = li.find('span',class_='cn_tit').text
        
        dic['评分'] = li.find('span',class_='total_star').span['style']
        dic['排名'] = li.find('span',class_="ranking_sum").text
        dic['简介'] = li.find('div',class_="desbox").text
        dic['攻略提到数量'] = li.find('div',class_="strategy_sum").text
        dic['点评数量'] = li.find('div',class_="comment_sum").text
        #dic['多少比例驴友来过'] = li.find('div',class_="txtbox clrfix").find('div',class_="comment_sum").text
        dic['多少比例驴友来过'] = li.find('div',class_="txtbox clrfix").find('span',class_="comment_sum").text
        #print(dic['评分'],dic['多少比例驴友来过'])
        dic['经度'] = li['data-lng']
        dic['纬度'] = li['data-lat']
        
        lst.append(dic)
    
    return lst


if __name__ == '__main__':
    urllst = get_urls('shanghai',20)
    datalst=[]
    errorlst = []
    for u in urllst:
        try:
            datalst.extend(get_data(u))
            print('数据采集成功，总共采集%i条数据' % len(datalst))
        except:
            errorlst.append(u)
            print("数据采集失败，数据网址为：", u)
    datadf = pd.DataFrame(datalst)
    datadf['经度'] = datadf['经度'].astype('float')
    datadf['纬度'] = datadf['纬度'].astype('float')
    datadf['攻略提到数量'] = datadf['攻略提到数量'].astype('int')
    datadf['评分'] = datadf['评分'].str.split(':').str[-1].str.replace('%','').astype('int')
    datadf['多少比例驴友来过'] = datadf['多少比例驴友来过'].str.split('%').str[0].astype('float')/100
    datadf['排名'] = datadf[datadf['排名']!='']['排名'].str.split('第').str[-1].astype('int')
        # 数据清洗
    
    datadf.to_excel('去哪网-上海景点排名.xlsx')
    
    
    
    