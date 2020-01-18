# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 20:46:41 2019

@author: Chen Tian

E-mail: chentianfighting@126.com
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

urllst = ['https://book.douban.com/subject/25697249/',
 'https://book.douban.com/subject/30334375/',
 'https://book.douban.com/subject/1342974/',
 'https://book.douban.com/subject/2375216/',
 'https://book.douban.com/subject/30277178/',
 'https://book.douban.com/subject/27598727/',
 'https://book.douban.com/subject/5972003/',
 'https://book.douban.com/subject/26976311/',
 'https://book.douban.com/subject/27623508/',
 'https://book.douban.com/subject/30400709/',
 'https://book.douban.com/subject/26312905/',
 'https://book.douban.com/subject/26689802/',
 'https://book.douban.com/subject/24846641/',
 'https://book.douban.com/subject/26952158/',
 'https://book.douban.com/subject/26763759/',
 'https://book.douban.com/subject/26870315/',
 'https://book.douban.com/subject/33374802/',
 'https://book.douban.com/subject/1049180/',
 'https://book.douban.com/subject/30270114/',
 'https://book.douban.com/subject/26772174/',
 'https://book.douban.com/subject/1704739/',
 'https://book.douban.com/subject/1901416/',
 'https://book.douban.com/subject/27026325/',
 'https://book.douban.com/subject/30352361/',
 'https://book.douban.com/subject/3662001/',
 'https://book.douban.com/subject/10601552/',
 'https://book.douban.com/subject/26854494/',
 'https://book.douban.com/subject/3171429/',
 'https://book.douban.com/subject/26854520/',
 'https://book.douban.com/subject/30180492/',
 'https://book.douban.com/subject/1563501/',
 'https://book.douban.com/subject/27616459/',
 'https://book.douban.com/subject/4007145/',
 'https://book.douban.com/subject/2368858/',
 'https://book.douban.com/subject/3417439/',
 'https://book.douban.com/subject/1918359/',
 'https://book.douban.com/subject/26289726/',
 'https://book.douban.com/subject/26928785/',
 'https://book.douban.com/subject/1394347/',
 'https://book.douban.com/subject/25913083/',
 'https://book.douban.com/subject/3172128/',
 'https://book.douban.com/subject/27096715/',
 'https://book.douban.com/subject/1066894/',
 'https://book.douban.com/subject/2679108/',
 'https://book.douban.com/subject/30255019/',
 'https://book.douban.com/subject/5957593/',
 'https://book.douban.com/subject/1959906/',
 'https://book.douban.com/subject/3324937/',
 'https://book.douban.com/subject/3836028/',
 'https://book.douban.com/subject/1394855/',
 'https://book.douban.com/subject/30368115/',
 'https://book.douban.com/subject/1026278/',
 'https://book.douban.com/subject/4319558/',
 'https://book.douban.com/subject/6843464/',
 'https://book.douban.com/subject/25807354/',
 'https://book.douban.com/subject/26266109/',
 'https://book.douban.com/subject/10299917/',
 'https://book.douban.com/subject/1075743/',
 'https://book.douban.com/subject/26012244/',
 'https://book.douban.com/subject/4732687/',
 'https://book.douban.com/subject/25774694/',
 'https://book.douban.com/subject/2157167/',
 'https://book.douban.com/subject/4115076/',
 'https://book.douban.com/subject/26954403/',
 'https://book.douban.com/subject/25717499/',
 'https://book.douban.com/subject/26807037/',
 'https://book.douban.com/subject/25774853/',
 'https://book.douban.com/subject/20278047/',
 'https://book.douban.com/subject/24751251/',
 'https://book.douban.com/subject/26389380/',
 'https://book.douban.com/subject/1035146/',
 'https://book.douban.com/subject/26209238/',
 'https://book.douban.com/subject/4934772/',
 'https://book.douban.com/subject/27094149/',
 'https://book.douban.com/subject/26111126/',
 'https://book.douban.com/subject/24857903/',
 'https://book.douban.com/subject/26873229/',
 'https://book.douban.com/subject/1461751/',
 'https://book.douban.com/subject/1453569/',
 'https://book.douban.com/subject/30327383/',
 'https://book.douban.com/subject/3894806/',
 'https://book.douban.com/subject/2510363/',
 'https://book.douban.com/subject/33396671/',
 'https://book.douban.com/subject/7065245/',
 'https://book.douban.com/subject/6397149/',
 'https://book.douban.com/subject/25923467/',
 'https://book.douban.com/subject/26754382/',
 'https://book.douban.com/subject/1724394/',
 'https://book.douban.com/subject/26701925/',
 'https://book.douban.com/subject/4760262/',
 'https://book.douban.com/subject/33429534/',
 'https://book.douban.com/subject/1437899/',
 'https://book.douban.com/subject/30142689/',
 'https://book.douban.com/subject/33386755/',
 'https://book.douban.com/subject/26972523/',
 'https://book.douban.com/subject/2077064/',
 'https://book.douban.com/subject/30246276/',
 'https://book.douban.com/subject/6017467/',
 'https://book.douban.com/subject/10834452/',
 'https://book.douban.com/subject/30536349/']

def get_data(u):
    ri = requests.get(url=u)
    soupi = BeautifulSoup(ri.text, 'lxml')
    infors = soupi.find('div', id="info").text
    dic = {}
    dic['书名'] = soupi.find('div', id="wrapper").h1.text.replace('\n','')
    s = re.sub(r' +', '',infors)
    #s1 = re.sub(r'\s+','',infors) # 会把\n也替换掉
    lst = re.findall(r'\n.+:.*\n.+?',s)
    for i in lst:
        i = i.replace('\n','')
        dic[i.split(':')[0]] = i.split(':')[1]
        # 匹配简单字段
    dj = re.search(r'定价:\D*([.\d]+)\D*',s)
    if dj:
        dic['定价'] = dj.group(1)
    zz = re.search(r'作者:([\s\S]+)\n出版社',s)
    if zz:
        dic['作者'] = zz.group(1).replace('\n','')
    yz = re.search(r'译者:([\s\S]+)\n出版年',s)
    if yz:
        dic['译者'] = yz.group(1).replace('\n','')
    
    return dic



if __name__ == "__main__":
    datalst = []
    errorlst = []
    for ui in urllst:
        try:
            datalst.append(get_data(ui))
            print("数据采集成功，总共采集%i条数据" % len(datalst))
        except:
            errorlst.append(ui)
        print('数据采集失败，数据网址为：',ui)
            
    datadf = pd.DataFrame(datalst)
    