# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 07:44:50 2019

@author: Chen Tian
豆瓣搜索爬虫代码.py
E-mail: chentianfighting@126.com
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pymongo
import re
import time
import warnings
warnings.filterwarnings('ignore')
# 不发出警告
start = time.time()
'''
1、获取书籍信息页面url selenium
'''
urllst = ['https://book.douban.com/subject_search?search_text=%E6%95%B0%E6%8D%AE&cat=1001',
'https://book.douban.com/subject_search?search_text=%E6%95%B0%E6%8D%AE&cat=1001&start=15',
'https://book.douban.com/subject_search?search_text=%E6%95%B0%E6%8D%AE&cat=1001&start=30',
'https://book.douban.com/subject_search?search_text=%E6%95%B0%E6%8D%AE&cat=1001&start=45',
'https://book.douban.com/subject_search?search_text=%E6%95%B0%E6%8D%AE&cat=1001&start=60']
# 页面网址列表

brower = webdriver.Chrome()
# 启动测试器
dataurls = []
for url in urllst:
    brower.get(url)
    # 访问网页
    divs = brower.find_elements_by_class_name('item-root') # 注意elements 的单复数
    for div in divs:
        url = div.find_element_by_tag_name('a').get_attribute('href')
        dataurls.append(url)
        print('成功识别%i条数据网址' % len(dataurls))
print(dataurls)

'''
2、每个书籍url链接的详细数据采集
requests+bs
'''
myclient = pymongo.MongoClient('mongodb://localhost:27017')
db = myclient['豆瓣数据采集']
datatable = db['豆瓣搜索数据爬虫']
n = 1
 #设置数据库集合
 
errorlst = []
for u in dataurls[1:]:
    try:
        ri = requests.get(url=u)
        soupi = BeautifulSoup(ri.text,'lxml')
        # 访问并解析网址
        dic = {}
        dic['书名'] = soupi.h1.text.replace('\n','')
        infor1 = re.findall(r'[\d.]+',soupi.find('div',class_='rating_self clearfix').text)
        dic['评分'] = infor1[0]
        dic['评价人数'] = infor1[1]
        # 书名、评分、评价人数匹配
        info2 = soupi.find('div',id="info").text
        s1 = re.sub(r' +','',info2) #正则替换，将空格替换掉
        lst = re.findall(r'\n.+:.+\n',s1)
        for i in lst:
            i = i.replace('\n','')
            dic[i.split(':')[0]] = i.split(':')[1]
            #匹配简单字段
        zz = re.search(r'作者:([\s\S]+)\n出版社',s1) #[\s\S] 为除\n之外的字符
        if zz:
            dic['作者'] = zz.group(1).replace('\n','')
            # 匹配作者信息
        yz = re.search(r'译者:([\s\S]+)\n出版年', s1)
        if yz:
            dic['译者'] = yz.group(1).replace('\n','')
            # 匹配译者信息
        dj = re.search(r'定价:\D*([.\d]+)\D*',s1)
        if dj:
            dic['定价'] = dj.group(1)
            # 匹配定价信息
        datatable.insert_one(dic) # 数据入库
        print('成功采集%i条数据'%n)
        n += 1
    except:
        print('网页采集失败，网址为：', u)
        errorlst.append(u)
end = time.time()

print('总耗时：', end-start)
