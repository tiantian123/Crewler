# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 22:18:21 2019

@author: Chen Tian

E-mail: chentianfighting@126.com
"""
from selenium import webdriver
import time

brower = webdriver.Chrome()
start = time.time()
# 访问网址
brower.get('https://book.douban.com/subject/1043815/')
h1 = brower.find_element_by_tag_name('h1').text
ifo = brower.find_element_by_id('info').text
score = brower.find_element_by_xpath('//*[@id="interest_sectl"]/div/div[2]/strong').text
comment = brower.find_element_by_xpath('//*[@id="interest_sectl"]/div/div[2]/div/div[2]/span/a/span').text
dic = {}
dic['书名'] = h1
dic['其他信息'] = ifo
dic['评分'] = score
dic['评论人数'] = comment
print(dic)
end = time.time()
print('总共花费了%.2f秒' % (end - start))


