# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 07:58:17 2019

@author: Chen Tian

E-mail: chentianfighting@126.com
"""
from selenium import webdriver
import time

# selenium 模拟网页登陆
brower = webdriver.Chrome()
brower.get('https://book.douban.com/')
login = brower.find_element_by_xpath('//*[@id="db-global-nav"]/div/div[1]/a')
login.click()
brower.find_element_by_xpath('//*[@id="account"]/div[2]/div[2]/div/div[1]/ul[1]/li[2]').click()
# 选择密码登陆

username = brower.find_element_by_xpath('//*[@id="username"]')
password = brower.find_element_by_xpath('//*[@id="password"]')
username.clear()
password.clear()
username.send_keys('15602408859')
password.send_keys('tiantian520')

brower.find_element_by_xpath('//*[@id="account"]/div[2]/div[2]/div/div[2]/div[1]/div[4]/a').click()
print(brower.current_url)