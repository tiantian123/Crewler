# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 07:03:02 2019

@author: Chen Tian

E-mail: chentianfighting@126.com
"""
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pymongo
import re
import time
import random
import warnings
warnings.filterwarnings('ignore')
# 不发出警告

def login(u, username, password):
    '''
    【登陆函数】
    u: 起始网址
    username: 用户名
    password: 密码
    '''
    brower.get(u)
    brower.find_element_by_xpath('//*[@id="changeCityBox"]/p[1]/a').click()
    brower.find_element_by_xpath('//*[@id="lg_tbar"]/div/div[2]/div/a[1]').click()
    username = brower.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[1]/div/div[1]/form/div[1]/div/input')
    password = brower.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[1]/div/div[1]/form/div[2]/div/input')
    # 找到input 标签
    username.clear()
    password.clear()
    username.send_keys('15602408859')
    password.send_keys('@tiantian520')
    # 输入账号密码
    brower.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[2]/div[2]/div[2]').click()
    # 遇到验证码时，手动或者调用百度的智能API
    print('成功登陆，返回目前网址：', brower.current_url)

def get_urls(n):
    '''
    【分页网页url采集】函数
    按“数据挖掘”关键字进行搜索，得到的网址：
    https://www.lagou.com/shanghai-zhaopin/shujuwajue/2/?filterOption=2
    n：页数参数
    结果：得到一个分页网页的list
    '''
    lst = []
    for i in range(1,n+1):
        lst.append('https://www.lagou.com/shanghai-zhaopin/shujuwajue/%d/?filterOption=%d'%(i,i))
    return lst

def get_data(ui, table):
    '''
    【访问页面 + 采集岗位信息】函数
    ui: 数据页面网址
    table: mongo集合对象
    '''
    brower.get(ui)
    # 访问网页
    ul = brower.find_element_by_xpath('//*[@id="s_position_list"]/ul')
    lis = ul.find_elements_by_tag_name('li')
    # 获取所有li 标签
    n = 0
    for li in lis:
        dic = {}
        dic['岗位名称'] = li.find_element_by_tag_name('h3').text
        dic['发布时间'] = li.find_element_by_class_name("format-time").text
        info1 = li.find_element_by_class_name("li_b_l").text
        info1 = re.split(r'[ /]*',info1)
        dic['薪资'] = info1[0]
        dic['经验要求'] = info1[1]
        dic['学历要求'] = info1[2]
        dic['企业名称'] = li.find_element_by_class_name("company_name").text
        info2 = li.find_element_by_class_name('industry').text.split(' / ')
        dic['行业'] = info2[0]
        dic['融资情况'] = info2[1]
        dic['企业规模'] = info2[2]
        table.insert_one(dic)
        n += 1
        #print(dic)
    return n
    

    
if __name__ == "__main__":
    brower = webdriver.Chrome()
     # 启动
    login('https://www.lagou.com/','15602408859', '@tiantian520')
    
    urllst = get_urls(10)
    
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myclient['拉勾网']
    datatable = db['拉勾网数据采集_上海数据挖掘']
    
    #get_data(urllst[0],datatable)
    # 设置数据库集合
    errorlst = []
    datacount = 0
    for u in urllst:
        try:
            datacount += get_data(u,datatable)
            print('成功采集%i条数据' % datacount)
            sleeptime = random.randint(1,5)
            print('sleep...', sleeptime)
            time.sleep(sleeptime)
        except:
            errorlst.append(u)
            print('数据采集失败, 数据网址为:',u)
        
    
    
    
    
    