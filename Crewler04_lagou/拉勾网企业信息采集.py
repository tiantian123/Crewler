# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 06:19:16 2019

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

def login(u,username,password):
    '''
     【登陆】函数
    u：起始网址
    username：用户名
    password：密码
    '''
    brower.get(u)
    #brower.find_element_by_xpath('//*[@id="changeCityBox"]/p[1]/a').click()
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
    return brower.current_url

def get_data(ui,table,page_n):
    '''
    【访问页面 + 采集岗位信息 - 翻页】
    ui：数据页面网址
    table：mongo集合对象
    page_n：翻页次数
    '''
    brower.get(ui)
    n = 0
    for p in range(page_n):
        ul = brower.find_element_by_xpath('//*[@id="company_list"]/ul')
        lis = ul.find_elements_by_tag_name('li')
        
        for i in range(len(lis)):
            dic = {}
            dic['企业名称'] =  lis[i].find_element_by_xpath('//*[@id="company_list"]/ul/li[%d]/div[1]/h3/a' % (i+1)).text
            info1 = lis[i].find_element_by_xpath('//*[@id="company_list"]/ul/li[%d]/div[1]/h4[1]'%(i+1)).text.split('/')
            dic['行业'] = info1[0]
            dic['融资情况'] = info1[1]
            dic['企业规模'] = info1[2]
            dic['企业简介'] = lis[i].find_element_by_xpath('//*[@id="company_list"]/ul/li[%d]/div[1]/h4[2]'%(i+1)).text
            dic['面试评价'] = lis[i].find_element_by_xpath('//*[@id="company_list"]/ul/li[%d]/div[2]/a[1]/p[1]'%(i+1)).text
            dic['在招职位'] = lis[i].find_element_by_xpath('//*[@id="company_list"]/ul/li[%d]/div[2]/a[2]/p[1]'%(i+1)).text
            dic['简历处理率'] = lis[i].find_element_by_xpath('//*[@id="company_list"]/ul/li[%d]/div[2]/a[3]/p[1]'%(i+1)).text
            '''
            info2 = lis[i].find_element_by_xpath('//*[@id="company_list"]/ul/li[%d]/div[2]'%i).text.split('\n')
            dic['面试评价'] = info2[0]
            dic['在招职位'] = info2[2]
            dic['简历处理率'] = info2[4]
            print(info2)
            '''
            table.insert_one(dic)
            n += 1
        brower.find_element_by_xpath('//*[@id="company_list"]/div/div/span[6]').click()
        sleeptime = random.randint(1,5)
        print('成功采集%d条数据，等待sleep...' %n, sleeptime)
        time.sleep(sleeptime)
    #return lis


if __name__ == "__main__":
    brower = webdriver.Chrome()
    # 开启浏览器
    ul = login('https://www.lagou.com/gongsi/','15602408859', '@tiantian520')
    # 登陆
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    db = myclient['拉勾网']
    datatable = db['拉勾网企业信息采集']
    
    get_data(ul,datatable,10)
    
    

