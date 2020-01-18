# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 08:19:21 2019

@author: Chen Tian

E-mail: chentianfighting@126.com
"""
import pandas as pd
from bs4 import BeautifulSoup
import pymongo
import re
import requests
import warnings
warnings.filterwarnings('ignore')

def get_url(ui, d_h,d_c):
    '''
    视频页面url采集】
    u：起始网址
    d_h：user-agent信息
    d_c：cookies信息
    结果：得到一个视频页面的list
    '''
    ri = requests.get(url=ui)
    soupi = BeautifulSoup(ri.text,'lxml')
    lis = soupi.find('ul',class_="video-list clearfix").find_all('li')
    lst = []
    for i in lis:
        lst.append('https:' + i.a['href'])
    #print(lst[0])
    return lst

def get_data(ui, d_h, d_c, table):
    '''
    视频页面数据采集 / cid信息 / 弹幕xml数据采集】
    ui：视频页面网址
    d_h：user-agent信息
    d_c：cookies信息
    table：mongo集合对象
    '''
    ri = requests.get(url=ui,headers=d_h, cookies=d_c)
    soupi = BeautifulSoup(ri.text,'lxml')
    name = soupi.h1['title']
    time = re.search(r'(20.*\d)',soupi.find('div',class_="video-data").text).group(1)
    cid = re.search(r'"cid":(\d*)', ri.text).group(1)
    cid_url = 'https://comment.bilibili.com/%s.xml' % cid
    
    r2 = requests.get(url=cid_url)
    r2.encoding = r2.apparent_encoding #解决页面乱码问题
    dmlst = re.findall(r'<d.*?/d>', r2.text)
    n = 0
    for dm in dmlst:
        dic = {}
        dic['标题'] = name
        dic['发布时间'] = time
        dic['cid'] = cid
        dic['弹幕'] = re.search(r'>(.*)</d>',dm).group(1)
        dic['其他信息'] = re.search(r'p="(.*)"', dm).group(1)
        #print(dic)
        table.insert_one(dic)
        n += 1
    return n
  
if __name__ == "__main__":
    dic_h = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    cookies = "_uuid=FF32462E-8C22-D5C1-484E-23D934FEB06975943infoc; buvid3=79452841-31B9-43C3-8A36-7DEB4272D59E190972infoc; arrange=matrix; LIVE_BUVID=AUTO1915690249771318; CURRENT_FNVAL=16; sid=l3jv2j3t; stardustvideo=1; rpdid=|(RlllJ~YkY0J'ulYm|klk)u; DedeUserID=471769741; DedeUserID__ckMd5=26b8133841348aa7; SESSDATA=35be5083%2C1571617667%2C9b1cfb91; bili_jct=b90f2cc20806d662dc7f93b2496f16bd"
    dic_c = {}
    for i in cookies.split(';'):
        dic_c[i.split('=')[0]] = i.split('=')[1]
        # 获取header信息
    
    # 设置初始网址
    u1 = 'https://search.bilibili.com/all?keyword=蔡徐坤'
    lst = get_url(u1,dic_h,dic_c)
    # 设置数据库集合
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myclient["blibli"]
    datatable = db['弹幕信息']
    errorlst = []
    count = 0
    get_data(lst[0],dic_h, dic_c, datatable)
    for u in lst:
        try:
            count += get_data(u,dic_h, dic_c, datatable)
            print('数据采集成功，总共采集%i条数据' % count)
        except:
            errorlst.append(u)
            print('数据采集失败，数据网址为：', u)
        #for i in lst:
        
    
    