# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 07:47:46 2019

@author: Chen Tian

E-mail: chentianfighting@126.com
"""
import requests
ul = 'https://book.douban.com/tag/%E7%BB%8F%E5%85%B8'
r = requests.get(url=ul)
print(r)
print(type(r))