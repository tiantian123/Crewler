# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 23:01:49 2019

@author: Chen Tian

E-mail: chentianfighting@126.com
"""
import requests
from bs4 import BeautifulSoup
import pymongo
import time
import re
import random
import warnings
warnings.filterwarnings('ignore')

def url_extract(database,table,field):
    '''
    【数据网页url提取】函数
    database：数据库
    table：源数据mongo集合对象
    field：url字段
    '''
    dlst = table.find()
    lst = []
    for i in dlst:
        lst.append(i[field])
    return lst

def get_proxies(p_User,p_Pass,p_Host,p_Port):
    '''
    【生成动态代理ip】函数
    p_Host、p_Port: 设置代理服务器
    p_User、p_Pass: 设置代理隧道验证信息
    '''
    p = "http://%(user)s:%(pass)s@%(host)s:%(port)s"%{
            'host':p_Host,
            'port':p_Port,
            'user':p_User,
            'pass':p_Pass
            }
    ips = {
            'http':p,
            'https':p
            }
    return ips


'''
for i in range(1,10):
    print(requests.get(url="http://icanhazip.com/",
                       proxies=ip_dic).text)
'''   
    

def get_data2(ui, d_h, ips, table):
    '''
    数据采集及mongo入库】函数
    ui：数据信息网页
    d_h：user-agent信息
    ips：代理设置
    table：mongo集合对象
    '''
    ri = requests.get(url=ui,headers=d_h, proxies=ips)
        #访问网页
    soupi = BeautifulSoup(ri.text, 'lxml')
    dic = {}
    dic['标题'] = soupi.h1.text
    price = soupi.find('div',class_="price ").text
    dic['总价_万'] = re.search(r'(\d+)万',price).group(1)
    dic['单价_元'] = re.search(r'(\d+)元',price).group(1)
    info1_lis = soupi.find('div',class_="base").find('div',class_="content").find_all('li')
    for li in info1_lis:
        st = re.split(r'<.+?>',str(li))
        dic[st[2]] = st[3].replace('\n','')
    info2_lis = soupi.find('div',class_="transaction").find('div',class_="content").find_all('li')
    for li in info2_lis:
        st = re.split(r'<.+?>',str(li))
        dic[st[2]] = st[3].replace('\n','')
    position = re.search(r"resblockPosition:'([\d.]+),([\d.]+)'",ri.text)
    dic['lng'] = position.group(1)
    dic['lat'] = position.group(2)
    table.insert_one(dic)

if __name__ == '__main__':
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    # 链接数据库
    dic_h= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    
    ip_dic = get_proxies('HYPHY98J015A67MD','C6BF078FCCA47FA4',
            'http-dyn.abuyun.com','9020')
    # 生成代理ip
    
    db = myclient['链家']
    datatabel = db['长沙岳麓区二手房']
    datatabel2 = db['长沙岳麓区二手房03']
    datatabel2.delete_many({})
    urllst = url_extract(db,datatabel,'链接')
    errorlst = []
    count = 1
    for ui in urllst:
        #time.sleep(random.randint(1,5)) # 随机等待1-5秒
        try:
            get_data2(ui,dic_h,ip_dic,datatabel2 )
            print('数据采集成功，总共采集%i条数据' % count)
            count += 1
        except:
            errorlst.append(ui)
            print("数据采集失败， 数据网址为：" ,ui)
    